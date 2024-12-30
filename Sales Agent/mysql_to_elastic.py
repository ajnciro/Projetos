# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 17:26:57 2024

@author:    Ciro
            ciro@mail.org        
"""

import mysql.connector
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import Document
from llama_index.core import StorageContext
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from elasticsearch import AsyncElasticsearch
from config import ELASTIC_HOST, ELASTIC_USER, ELASTIC_PASSWORD, db_config
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')

# Configurações do Elastic Vector Store
ELASTIC_CONFIG = {
    'hosts': [ELASTIC_HOST],
    'user': ELASTIC_USER,
    'password': ELASTIC_PASSWORD,
    'index_name': 'loja_1'
}

# Função para obter dados do MySQL
def fetch_products():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT SKU, NOMEPROD, DESCPROD FROM produtos"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return rows

# Inicializa o Elastic Vector Store
def initialize_elastic_vector_store():
    es_client = AsyncElasticsearch(
        hosts=ELASTIC_CONFIG['hosts'],
        basic_auth=(ELASTIC_CONFIG['user'], ELASTIC_CONFIG['password']),
        verify_certs=False
    )
    vector_store = ElasticsearchStore(
        es_client=es_client,
        index_name=ELASTIC_CONFIG['index_name']
    )
    return vector_store

# Cria índice a partir dos produtos e salva no Elastic Vector Store
def create_and_store_index(products, vector_store):
    documents = [
        Document(
            text=f"{product['NOMEPROD']}: {product['DESCPROD']}",
            doc_id=str(product['SKU'])
        )
        for product in products
    ]

    # Cria o índice
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

# Main: Integrar MySQL com Elastic Vector Store usando LlamaIndex
def main():
    print("Fetching products from MySQL...")
    products = fetch_products()
    print(f"Fetched {len(products)} products.")

    print("Initializing Elastic Vector Store...")
    vector_store = initialize_elastic_vector_store()

    print("Creating and storing index...")
    create_and_store_index(products, vector_store)
    print("Indexing complete.")

if __name__ == "__main__":
    main()