'''
Usando a biblioteca dotenv e a biblioteca os
salvar os valores da variaveis de ambiente nas 
chaves do dicionario.

A partir das chaves do dicionario é possivel obter
o valor dessa forma: key['consumer_key'], key['access_token_secret'], etc

~silas
'''

import os

from dotenv import load_dotenv

load_dotenv()

key = {
  "consumer_key": os.getenv('TWITTER_API_KEYS'),
  "consumer_secret": os.getenv('TWITTER_API_KEY_SECRET'),
  "access_token":  os.getenv('TWITTER_ACCESS_TOKEN'),
  "access_token_secret": os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
  "bearer_token": os.getenv('TWITTER_BEARER_TOKEN')
}