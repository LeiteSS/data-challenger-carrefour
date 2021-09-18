'''
Arquivo parecido com os apiKeys

~silas
'''

import os

from dotenv import load_dotenv

load_dotenv()

key_mongo = {
  "mongo_username": os.getenv('MONGO_INITDB_ROOT_USERNAME'),
  "mongo_password": os.getenv('MONGO_INITDB_ROOT_PASSWORD')
}