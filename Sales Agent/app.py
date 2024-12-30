# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 17:26:07 2024

@author:    Ciro
            ciro@mail.org        
"""

from flask import Flask, request, Response
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains.llm_math.base import LLMMathChain

# Importações das configurações e ferramentas
from tools.database_tools import get_client_info_function, add_client_info_function
from tools.retrieval_tools import hybrid_query_products
from tools.cart_tools import add_to_cart, view_cart
from tools.transcription_tools import transcribe_audio

app = Flask(__name__)

# Dicionários globais para memória de conversação e carrinho
memory_dict = {}
cart_dict = {}

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    # Extrai a mensagem e o número do cliente
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '').replace("whatsapp:", "")

    # Verifica se a mensagem é de voz
    num_media = int(request.values.get('NumMedia', 0))
    if num_media > 0:
        media_url = request.values.get('MediaUrl0', '')
        media_type = request.values.get('MediaContentType0', '')
        if 'audio' in media_type:
            # Transcreve o áudio
            incoming_msg = transcribe_audio(media_url)
            if 'Erro' in incoming_msg:
                result = incoming_msg
                return send_whatsapp_response(result)
        else:
            result = "Desculpe, só consigo processar mensagens de áudio."
            return send_whatsapp_response(result)

    # Verifica se o usuário já possui memória de conversa
    if from_number not in memory_dict:
        memory_dict[from_number] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    memory = memory_dict[from_number]

    # Inicializa o LLM
    llm = ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0.0)

    # Funções que encapsulam o número de telefone
    def get_client_info_tool(input: str = "") -> str:
        return get_client_info_function(from_number)

    def add_client_info_tool(client_info: str) -> str:
        return add_client_info_function(client_info, from_number)

    def add_to_cart_tool(item_info: str) -> str:
        return add_to_cart(from_number, item_info)

    def view_cart_tool(input: str = "") -> str:
        return view_cart(from_number)

    # Ferramenta para calcular o total do carrinho
    llm_math_chain = LLMMathChain(llm=llm, verbose=True)

    tools = [
        Tool(
            name="get_client_info",
            func=get_client_info_tool,
            description="Usado para obter informações do cliente com base no número de telefone (não requer entrada)."
        ),
        Tool(
            name="add_client_info",
            func=add_client_info_tool,
            description="Usado para adicionar um novo cliente ao banco de dados. Forneça as informações do cliente no formato 'Nome: ..., Sobrenome: ..., Endereço: ...'."
        ),
        # Tool(
        #     name="get_available_products",
        #     func=get_available_products,
        #     description="Usado para listar todos os produtos disponíveis."
        # ),
        Tool(
            name="hybrid_query_products",
            func=hybrid_query_products,
            description="Usado para buscar produtos específicos com base em consultas do cliente usando uma pesquisa híbrida semântica e léxica."
        ),
        Tool(
            name="add_to_cart",
            func=add_to_cart_tool,
            description="Usado para adicionar ou remover itens do carrinho. Forneça os itens no formato 'SKU1:quantidade1, SKU2:quantidade2' ou 'NomeProduto1:quantidade1, NomeProduto2:quantidade2'. Para remover itens, use quantidades negativas."
        ),
        Tool(
            name="view_cart",
            func=view_cart_tool,
            description="Usado para visualizar os itens atuais no carrinho."
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="Útil para quando você precisa resolver problemas matemáticos."
        )
    ]

    # Configuração do agente
    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={
            "system_message": f"""
                Você é um agente de vendas experiente fornecendo serviço via WhatsApp. Sempre responda em Português e tente chamar seu cliente pelo primeiro nome.

                - O número de telefone do cliente é '{from_number}'.
                - Use 'get_client_info' para obter informações do cliente.
                - Se as informações do cliente não estiverem disponíveis, peça gentilmente seu nome, sobrenome e endereço, então use 'add_client_info' para registrá-lo.
                - Trate o cliente pelo primeiro nome após a identificação.
                - Use 'hybrid_query_products' para buscar produtos com base nas consultas do cliente.
                - Use 'add_to_cart' para adicionar ou remover itens do pedido. Forneça os itens no formato 'SKU1:quantidade1, SKU2:quantidade2' ou 'NomeProduto1:quantidade1, NomeProduto2:quantidade2'. Para remover itens, use quantidades negativas.
                - Forneça um resumo detalhado do pedido sempre que itens forem adicionados ou o cliente estiver pronto para finalizar a compra. Inclua nomes dos produtos, quantidades, preços individuais e o valor total do pedido.
                - Use 'view_cart' para mostrar os itens atuais do carrinho.
                - Use a ferramenta 'Calculator' para calcular o valor total do pedido.
                - Aceite pagamentos via PIX, dinheiro e cartão na entrega.
                - Sempre foque em efetuar a venda durante a interação.
                - Ao fornecer informações ou listas de produtos, formate o texto em uma tabela simples para maior clareza.
                - Ao finalizar um pedido ou um carrinho parcial, discrimine a lista de produtos e seus valores.
                - Importante: limite-se ao contexto de vendas e produtos aos quais possui acesso.
                """,
                "human_message": "{input}"
            }
    )

    try:
        # Executa o agente com a mensagem recebida
        result = agent_chain.run(input=incoming_msg)
    except Exception as e:
        print(f"Erro: {e}")
        result = "Desculpe, ocorreu um erro ao processar sua solicitação."

    # Envia a resposta
    return send_whatsapp_response(result)

def send_whatsapp_response(message):
    # Formata a resposta usando o Twilio's MessagingResponse
    from twilio.twiml.messaging_response import MessagingResponse
    response = MessagingResponse()
    response.message(str(message))
    return Response(str(response), mimetype='application/xml')

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
