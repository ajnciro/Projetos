"""Alimentação de um DB NoSQL com os verbetes para consulta eficiente dos valores"""

import f

from pymongo import MongoClient
conn = MongoClient('localhost', 27017)

import sqlite3
conn2 = sqlite3.connect(r'forca.db')  
c = conn2.cursor()

db = conn.forca_ia
collection = db.verbetes

i = 0
nonetype = type(collection.find_one({"palavra": ""}))
c.execute("SELECT * FROM verbetes")
for linha in c.fetchall():
    if type(collection.find_one({"palavra": linha[1]})) == nonetype:
        post = {"palavra": linha[1], "tamanho": linha[2], "descricao": linha[3], "fill_word":f.fill_word(linha[1]) }
        collection.insert_one(post)
        i+=1
        print (i)