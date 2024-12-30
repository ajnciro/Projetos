# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 17:26:33 2024

@author:    Ciro
            ciro@mail.org        
"""

from langchain.agents import tool
import mysql.connector
import re
from config import db_config

def get_client_info_function(phone_number: str) -> str:
    """
    Consulta informações do cliente com base no número de telefone.
    """

    phone = phone_number.strip().strip('"').strip("'")
    phone = re.sub(r'\D', '', phone)

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    last_eight_digits = phone[-8:].strip()

    cursor.execute("SELECT * FROM clientes WHERE RIGHT(FONE, 8) = %s", (last_eight_digits,))
    client_info = cursor.fetchone()

    conn.close()
    if client_info:
        return f"Cliente encontrado: {client_info['NOME']} {client_info['SOBRENOME']}, Endereço: {client_info['ENDERECO']}, Telefone: {client_info['FONE']}"
    else:
        return "Cliente não encontrado."

def add_client_info_function(client_info: str, phone_number: str) -> str:
    """
    Insere um novo cliente no banco de dados.
    """
    # Parse client_info, que deve ser uma string no formato 'Nome: ..., Sobrenome: ..., Endereço: ...'
    info = {}
    for item in client_info.split(','):
        key_value = item.strip().split(':')
        if len(key_value) == 2:
            key = key_value[0].strip().lower()
            value = key_value[1].strip()
            info[key] = value
    if 'nome' not in info or 'endereço' not in info:
        return "Informações insuficientes para cadastrar o cliente."
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO clientes (NOME, SOBRENOME, ENDERECO, FONE) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (
            info.get('nome'),
            info.get('sobrenome', ''),
            info.get('endereço'),
            phone_number
        ))
        conn.commit()
        return "Cliente cadastrado com sucesso."
    except Exception as e:
        conn.rollback()
        return f"Erro ao cadastrar cliente: {e}"
    finally:
        conn.close()

@tool
def get_available_products(input: str = "") -> str:
    """
    Consulta e retorna a lista de produtos disponíveis formatada como string.
    """
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    products = cursor.fetchall()
    conn.close()
    if products:
        product_list = "\n".join(
            [f"Produto: {p['NOMEPROD']}, Descrição: {p['DESCPROD']}, Preço: R${p['VALORPROD']}, Estoque: {p['ESTOQUE']}, SKU: {p['SKU']}" for p in products]
        )
        return f"Temos os seguintes produtos disponíveis:\n{product_list}"
    else:
        return "Nenhum produto disponível no momento."