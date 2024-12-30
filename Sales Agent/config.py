# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 17:26:49 2024

@author:    Ciro
            ciro@mail.org        
"""

import os

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASS'),
    'database': os.getenv('SALES_AGENT_DATABASE_NAME')
}

# Configurações do Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER') #'whatsapp:+1...'

# Configurações do Elasticsearch
ELASTIC_HOST = 'https://localhost:9200'
ELASTIC_USER = 'elastic'
ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')

# Chave da API da OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
