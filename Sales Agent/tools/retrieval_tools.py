# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 17:26:41 2024

@author:    Ciro
            ciro@mail.org        
"""

from langchain.agents import tool
from elasticsearch import Elasticsearch
from llama_index.embeddings.openai import OpenAIEmbedding
import mysql.connector
from config import ELASTIC_HOST, ELASTIC_USER, ELASTIC_PASSWORD, db_config

embed_model = OpenAIEmbedding(model='text-embedding-3-small')

# Função de busca híbrida com recuperação de dados do MySQL
def hybrid_product_query(query_string, index_name='loja_1', k=60, top_n=10):
    es = Elasticsearch(
        basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
        hosts=[ELASTIC_HOST],
        verify_certs=False, #True se possui certificados válidos
        )

    query_vector = embed_model.get_query_embedding(query_string)

    # Lexical query
    lexical_query = {
        "query": {
            "match": {
                "content": query_string
            }
        },
        "size": top_n
    }

    # Semantic query
    semantic_query = {
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {
                        "query_vector": query_vector
                    }
                }
            }
        },
        "size": top_n
    }

    # Execute queries
    lexical_results = es.search(index=index_name, body=lexical_query, source_excludes=['embedding'])['hits']['hits']
    semantic_results = es.search(index=index_name, body=semantic_query, source_excludes=['embedding'])['hits']['hits']

    # Combine results for RRF
    combined_results = {}
    
    def rrf_score(rank, k):
        return 1.0 / (k + rank)

    # Add lexical results to combined results
    for rank, doc in enumerate(lexical_results):
        doc_id = doc['_id']
        if doc_id not in combined_results:
            combined_results[doc_id] = 0
        combined_results[doc_id] += rrf_score(rank + 1, k)

    # Add semantic results to combined results
    for rank, doc in enumerate(semantic_results):
        doc_id = doc['_id']
        if doc_id not in combined_results:
            combined_results[doc_id] = 0
        combined_results[doc_id] += rrf_score(rank + 1, k)

    # Sort combined results by RRF score
    sorted_results = sorted(combined_results.items(), key=lambda x: x[1], reverse=True)

    # Retrieve full documents
    reranked_docs = []
    for doc_id, score in sorted_results[:top_n]:
        doc = es.get(index=index_name, id=doc_id, source_excludes=['embedding'])
        doc_body = doc.body 
        doc_dict = {'content': doc_body['_source']['content'],'doc_id':doc_body['_source']['metadata']['doc_id']}
        doc_dict['_score'] = score
        reranked_docs.append(doc_dict)

    skus = [d.get('doc_id') for d in reranked_docs]

    # Consulta o banco de dados MySQL para obter informações atualizadas dos produtos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    format_strings = ','.join(['%s'] * len(skus))
    cursor.execute(f"SELECT * FROM produtos WHERE SKU IN ({format_strings})", tuple(skus))
    products = cursor.fetchall()

    conn.close()
    
    # Ordena os produtos na mesma ordem dos SKUs retornados
    sku_to_product = {product['SKU']: product for product in products}
    ordered_products = [sku_to_product[sku] for sku in skus if sku in sku_to_product]
    
    return ordered_products

# Ferramenta para consulta de produtos usando busca híbrida
@tool
def hybrid_query_products(query: str) -> str:
    """
    Usado para buscar produtos específicos com base em consultas do cliente usando uma pesquisa híbrida semântica e lexical.
    """
    results = hybrid_product_query(query_string=query, top_n=5)
    if results:
        product_list = "\n".join(
            [f"Produto: {p['NOMEPROD']}, Descrição: {p['DESCPROD']}, Preço: R${float(p['VALORPROD']):.2f}, Estoque: {p['ESTOQUE']}, SKU: {p['SKU']}" for p in results]
        )
        return f"Encontrei os seguintes produtos:\n{product_list}"
    else:
        return "Não encontrei produtos correspondentes à sua busca."