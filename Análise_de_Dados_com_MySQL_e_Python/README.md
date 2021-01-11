# Análise do DB de uma loja simples com Python

Este projeto se refere a uma análise preliminar do banco de dados de uma loja simples utilizando algumas ferramentas de Data Science.

No primeiro momento, foi criado um comércio fictício automatizado com Python para manipular um banco de dados MySQL.

O DER do banco e o script com o design que se julgou necessário e suficiente estão na pasta Banco de Dados, de acordo com a imagem:

[![DER](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/Banco%20de%20Dados/DER_LojaSimples.png "DER")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/Banco%20de%20Dados/DER_LojaSimples.pnghttp:// "DER")

A automatização da das transações é feita a partir do script em "fluxo_loja_toCSV.py" que faz o start do DB por meio do programa em  "start_loja_db", como uma importação de módulo, e exporta as tabelas MySQL para CSV dentro da pasta CSVLoja.

```python
import mysql.connector
import numpy as np

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database = "lojasimples"
)
mycursor = mydb.cursor(buffered=True)
```

E atenção aos parâmetros do banco de dados.

Esses dois programas por si só realizam as transações necessárias, inserem os preços dos produtos, as vendas por cliente, departamento, manipulam o orçamento dos clientes etc., mas contam com alguns poucos triggers inseridos no script sql para ajudar na manipulação do banco.

A rotina em "fluxo_loja_toCSV.py" (que depende da importação de "start_loja_db"), realiza, essencialmente, um conjunto compras de 3 produtos distintos por clientes, com no máximo 4 unidades de cada. Essa compra depende de um orçamento preestabelecido de 30% da remuneração do indivíduo, tudo gerado pseudoaleatoriamente. Se o valor da compra não estiver dentro do orçamento, ela não será realizada. A cada 5 ciclos de compras (pode-se entender como 1 compra por semana, 5 semanas seguidas) bem-sucedidas ou malsucedidas, o orçamento é restaurado ao padrão.

Tanto o preço dos produtos, como a remuneração e orçamento, e as quantidades compradas, e a reposição de estoque são inseridos com gerador de pseudoaleatórios em intervalos determinados.

A cada 2000 ciclos de transações de 5 "semanas" cada, com 50 clientes comprando 250 produtos distintos de 15 departamentos diferentes, um arquivo de valores separados por vírgula CSV é gerado e exportado, então ocorre um incremento no valor do lucro percentual dos produtos.

[![DF](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/0.png "DF")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/0.pnghttp:// "DF")

No princípio, este lucro começa em 10% com relação ao custo que a loja tem para adquirir o produto e varia até 81% de 1 em 1%.

[![PairPlot](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/1.png "PairPlot")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/1.pnghttp:// "PairPlot")

A rotina em "fluxo_loja_toCSV2.py" (que depende da importação de "start_loja_db"), faz o mesmo trabalho, porém com o lucro percentual variando de 10 em 10% até 300%, a fim de se obter um alcance de dados maior. E exporta os mesmos para CSVLoja2.

Essas duas rotinas correspondem ao notebooks Jupyter "1_Loja_DF.ipynb" e "2_Loja_DF.ipynb"

[![PairPlot](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/2.png "PairPlot")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/2.pnghttp:// "PairPlot")

Já o script em "fluxo_loja_toCSV_Optm.py" (o qual depende da importação de "start_loja_db_Optm.py"), refere-se ao conjunto de transações na loja quando o lucro estabelecido que um produto deve obter não é constante e igual ao dos demais, mas ajustado de acordos com as otimizações vistas em "3_Loja_DF.ipynb", que, no fim, tratar-se-ia de um modelo de otimização do negócio em si.

Dentro de "3_Loja_DF.ipynb" há referências a procedimentos realizados em Wolfram Mathematica (ajuste de distribuição log-normal e função racional), cujos notebooks foram exportados para PDF para fins de eventual impossibilidade na leitura dos códigos.

[![Fit](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/3.png "Fit")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/3.pnghttp:// "Fit")
--
[![Mathematica](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/4.png "Mathematica")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/4.pnghttp:// "Mathematica")

De modo geral, como conclusão sobre a análise dos dados gerados pela loja fictícia automatizada, estão as observações:

- Lucros excessivos diminuem a quantidade de vendas e lucro absoluto total;

- Também diminuem o custo médio por departamento, provavelmente como consequência da não necessária frequência de reposição do estoque por menos vendas;

- Lucros percentuais demasiado pequenos também não sustem o lucro final de um comércio;

- Ajustes individuais dos lucros por produto, de acordo com o preço de custo, são mais eficientes que uma mesma margem para todos os itens, para a maioria das faixas de lucro percentual observadas (para mais que 75% dos casos).

[![Plot](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/5.png "Plot")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/5.pnghttp:// "Plot")

# Uma SVM para otimização das transações

SVMs (Support-Vector Machines) são algoritmos de aprendizagem baseados num hiperplano de separação entre duas categorias distintas, o qual, mapeado por uma combinação linear definida, visa encontrar regiões de clara separação entre as categorias. São particularmente úteis na detecção de outliers.

Esses algoritmos de aprendizagem foram aplicados aos dados gerados pelas transações da loja a fim de tentar obter valores ótimos na cobrança de lucros sobre os produtos, além de otimizar o fluxo de entrada no estoque.

Dos arquivos anteriores, verificou-se que existem regiões ótimas de lucro percentual, a depender do valor do produto. Também que, apensar inclusive do ajuste linear, sempre haverá itens com lucros finais negativos (prejuízo), o que interfere negativamente no balanço de geral do pequeno comércio automatizado.

Por esses motivos, além de o número de vendas sofrer com a margem de lucro, se pensou ser necessário algum tipo de otimização dessas margens, além de tentar reduzir o custo final com aquisição de mercadorias.

Fez-se o uso, no primeiro momento, de uma SVM que aprendesse quais margens de lucro seriam ótimas para cada valor de produto, com o intuito de maximizar o lucro final do mesmo.

Por lucro, neste caso, definiu-se qualquer valor final >5000, neste caso. Este lucro foi o parâmetro alvo que a aprendizagem da SVM deveria alcançar ajustando a margem de lucro necessária para cada valor.

Como descrito no notebook "3_svm_plots.ipynb", apenas utilizando esse parâmetro como alvo, o objetivo da máquina não foi cumprindo, nem sequer alcançando a otimização feita pelo modelo de regressão linear anteriormente colocado. Como segue:

[![SVM1](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/6.png "SVM1")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/6.png "SVM1")

Em que o triângulo vermelho representa o lucro alcançado pelas transações suportadas pela SVM, e os pontos verdes os demais das outras faixas de lucro percentual fixo.

Após, observando que não necessariamente o lucro não era grande pelo volume de vendas ou pelo preço específico dos item, mas também com uma contribuição negativa dos custos da loja, implementou uma máquina que levasse em conta uma reposição mínima de estoque dado o próprio valor de item, porém com esses dois parâmetros atuando de forma disjunta. Como se nota:

[![SVM2](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/7.png "SVM2")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/7.png "SVM2")

A eficiência do modelo também não foi suficiente, conseguindo também apenas lucros mediados.

Uma melhor solução surgiu quando, como parâmetro alvo do aprendizado da SVM foi colocado uma intersecção (ou produto) entre os conjuntos de valores de lucro final e o de vendas, fazendo a máquina atuar de modo a otimizar simultaneamente tanto os parâmetros de lucro percentual, como os de reposição do estoque. A função de determinação do lucro mais adequado para cada custo de item foi a seguinte:

```python
def max_lucro_min_aq(varcusto):
    """" Determina o máximo lucro predefino com o mínimo 
    custo acumulado por estoque de produto. O argumento 
    será o custo de aquisição do produto. Como ambas as 
    condições devem ser satisfeitas simultaneamente, 
    pode-se começar a busca pela condição a partir do 
    maior lucro e o mínimo custo estará contido"""
        
    x = 390
    while x>1:
        aqui = 1
        while aqui<150:
            cond = model.predict(pd.DataFrame(data={'prodCusto': [varcusto], 'lucroPercent': [x], 'aquiMed': [aqui]}))[0]
            if cond!=False:     #A precisão do modelo foi maior para detectar falsos (não-lucros) do que verdadeiros
                return [x,aqui]
                break
            aqui+=1
        x-=1
        if x == 1:
                return [1,1]
```

O conjunto de dados de treino e teste foi gerado pelas transações em "fluxo_loja_toCSV_SVM2.py", após um conjunto de amostras com lucro percentual variando entre 0 e 390%, de 10 em 10%. Dados suficiente para conseguir boa precisão em verdadeiros negativos, do que surge a condição no trecho de código acima.

Todos os dados obtidos estão na pasta supramencionada, e resultado que segue:

[![SVM3](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/8.png "SVM3")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/8.png "SVM3")

mostra que de fato o ajuste nos valores foi eficiente, consegue maior lucro percentual que todos os testes anteriores, e ainda sem itens com valores negativos.

A citar os valores negativos, foi possível concluir que nos dois casos mencionados anteriormente, apesar da ineficiência da máquina em atingir elevados lucros totais, ela foi bastante eficiente em conseguir que diversos produtos que teriam prejuízo não tiverem, tendo esta boa utilidade observada.

Naturalmente, as grandezas estatísticas geradas nas SVMs são semelhantes, como é possível observar neste comparativo dos custos gerados automaticamente para o conjuntos de dados para a SVM1 (apenas o Lucro como alvo) e SVM3 (lucro e estoque como alvos):

[![Relatorio](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/Relatorio.png "Relatorio")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/Relatorio.png "Relatorio")

--
[![Relatorio](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/Relatorio4.png "Relatorio")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/Relatorio4.png "Relatorio")

Porém, a distribuição de lucros por produto é mais concentrada nas regiões de maiores valores para a última, enquanto para a primeira existe um pico por volta da condição de >5000:

[![Relatorio](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/Relatorio7.png "Relatorio")](https://github.com/ajnciro/Projetos/blob/main/Análise_de_Dados_com_MySQL_e_Python/.ipynb_checkpoints/Relatorio7.png "Relatorio")

Assim, com o uso de uma SVM, foi possível otimizar as transações de uma loja simples, ajustando os lucros corretos individualmente para cada produto, bem com a taxa de reposição do estoque, conseguindo a maior margem com o mínimo de custo.