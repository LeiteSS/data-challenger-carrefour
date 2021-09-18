import pymongo

def connect_to_mongo(username, pwd, port):
  '''
  Método para se conectar no banco de dados usando os paramêtros: nome do usuario, senha e porta do server.
  '''
  m = pymongo.MongoClient("mongodb://{}:{}@localhost:{}".format(username, pwd, port))

  return m

def create_db(mongo_client, db_name):
  '''
  Método para criar um novo banco de dados
  '''
  db = mongo_client[db_name]

  return db
