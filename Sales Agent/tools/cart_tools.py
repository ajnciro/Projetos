# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 17:26:15 2024

@author:    Ciro
            ciro@mail.org        
"""

from config import db_config
import mysql.connector

cart_dict = {}

def add_to_cart(from_number: str, item_info: str) -> str:
    """
    Adiciona itens ao carrinho do usuário. Se a quantidade for negativa, remove itens do carrinho.
    """
    if from_number not in cart_dict:
        cart_dict[from_number] = {}
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    items = item_info.split(',')
    updated_items = []
    for item in items:
        sku_qty = item.strip().split(':')
        if len(sku_qty) == 2:
            identifier = sku_qty[0].strip()
            try:
                qty = int(sku_qty[1].strip())
            except ValueError:
                continue
            # Tenta encontrar o produto pelo SKU
            cursor.execute("SELECT * FROM produtos WHERE SKU = %s", (identifier,))
            product = cursor.fetchone()
            if not product:
                # Se não encontrar, tenta pelo nome do produto
                cursor.execute("SELECT * FROM produtos WHERE NOMEPROD = %s", (identifier,))
                product = cursor.fetchone()
            if product:
                sku = product['SKU']
                if sku in cart_dict[from_number]:
                    # Atualiza a quantidade existente
                    cart_dict[from_number][sku]['quantidade'] += qty
                    # Remove o item se a quantidade for zero ou negativa
                    if cart_dict[from_number][sku]['quantidade'] <= 0:
                        del cart_dict[from_number][sku]
                        updated_items.append(f"{product['NOMEPROD']} removido do carrinho")
                    else:
                        updated_items.append(f"{product['NOMEPROD']} quantidade atualizada para {cart_dict[from_number][sku]['quantidade']}")
                else:
                    # Adiciona novo item se a quantidade for positiva
                    if qty > 0:
                        cart_dict[from_number][sku] = {'produto': product, 'quantidade': qty}
                        updated_items.append(f"{product['NOMEPROD']} x {qty} adicionado ao carrinho")
                    else:
                        updated_items.append(f"{product['NOMEPROD']} não está no carrinho para ser removido")
    conn.close()
    if updated_items:
        return f"Carrinho atualizado: {', '.join(updated_items)}."
    else:
        return "Nenhum item válido foi adicionado ao carrinho."

def view_cart(from_number: str) -> str:
    """
    Retorna o conteúdo atual do carrinho do usuário.
    """
    if from_number not in cart_dict or not cart_dict[from_number]:
        return "Seu carrinho está vazio."
    cart_items = []
    total = 0.0
    for sku, item in cart_dict[from_number].items():
        produto = item['produto']
        quantidade = item['quantidade']
        subtotal = float(produto['VALORPROD']) * quantidade
        total += subtotal
        cart_items.append(f"{produto['NOMEPROD']} x {quantidade} = R${subtotal:.2f}")
    return f"Seu carrinho:\n" + "\n".join(cart_items) + f"\nTotal: R${total:.2f}"