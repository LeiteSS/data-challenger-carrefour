import pprint

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from modules import mongoDb
from modules import fileToDic as fd
from modules import apiKeys as api
from modules import mongoEnv
from modules import TwitterClient as tc
from modules import TwitterAuth as ta

countries = {}
file = open("input/WOEID.txt")
countries = fd.dictionary(file, countries)

consumer_key = api.key['consumer_key']
consumer_secret = api.key['consumer_secret']
access_token = api.key['access_token']
access_token_secret = api.key['access_token_secret']
bearer_token = api.key['bearer_token']

search_url = "https://api.twitter.com/1.1/trends/place.json"

query_params = {'id': countries['BRAZIL'], 'exclude': 'hashtags'}


username = mongoEnv.key_mongo['mongo_username']
pwd = mongoEnv.key_mongo['mongo_password']

def main():
  # Se autenticando ao Twitter API e se conectando ao endpoint
  oauth = ta.TwitterAuth(bearer_token)
  top_trends = oauth.connect_to_endpoint(search_url, query_params)
  print("-----------------------------RESPONSE JSON-------------------------------------")
  print(top_trends)
  print("-----------------------------FIM RESPONSE JSON---------------------------------")

  '''
  1. Conectando ao mongodb
  2. Criando o banco de dados
  3. criando a collection
  4. Persistindo o RESPONSE JSON no bd
  '''
  mongo_client = mongoDb.connect_to_mongo(username, pwd, '27017')
  database = mongoDb.create_db(mongo_client, 'tweets_db')
  collection = database['top_trends']

  for trend in top_trends:
    trend_id = collection.insert_one(trend).inserted_id
  
  print("---------------------------------DOCUMENTO PERSISTIDO-----------------------------------------")
  pprint.pprint(collection.find_one())
  print("---------------------------------FIM DOCUMENTO PERSISTIDO--------------------------------------")

  '''
  1. Extrai as trends, pois está não a unica informação que o Response JSON traz
  2. Converte a lista com trends em Dataframe
  3. Muda o nome dos campos do Dataframe
  4. Trata do Valores Not A Number
  5. Qual o volume de tweets usando o nome como indicador
  6. Visualizando os graficos e os salvando na pasta graphs
  '''
  trends = []
  for item in top_trends:
    trends = item['trends']
  
  df = pd.DataFrame(trends)

  df_trends = df.rename(
    columns={
        'name': 'Nome', 
        'url': 'URI', 
        'promoted_content': 'Patrocinado', 
        'query': 'Hashtag', 
        'tweet_volume': 'Volume'
    }
  )

  df_trends["Volume"].fillna(0, inplace=True)

  # Volume acima de 0
  top = df_trends[df_trends["Volume"] > 0].sort_values("Volume")
  top.plot(x="Nome", y=["Volume"], kind="bar", figsize=(10,5))
  plt.title('Top Trendings do Twitter')
  plt.savefig('graphs/grafico1.png')

   # Talvez seja preciso mudar o ultimo valor (0.0, 5.0, 45), (0.0, 5.0, 46) ou conforme o valor que o df_trends.shape retornar, pois depende do dia e hora
  x = np.linspace(0.0, 5.0, 4)
  fig, ax = plt.subplots(figsize=(15, 9))
  fig.subplots_adjust(bottom=0.15, left=0.2)
  plt.plot(x, df_trends["Volume"], marker='o')
  plt.title('Top Trendings do Twitter', fontsize=14)
  plt.xlabel('Dados', fontsize=14)
  plt.ylabel('Volume', fontsize=14)
  plt.grid(True)
  plt.savefig('graphs/grafico2.png')
  plt.show()

  top = df_trends[df_trends["Volume"] > 0].sort_values("Volume")
  top.plot(x="Nome", y="Volume", kind='line', figsize=(15,9))
  plt.savefig('graphs/grafico3.png')

  '''
  Se conectar ao twitter para poder obter os tweets dado uma query e realizar a
  analise de sentimento
  '''
  twitter_client = tc.TwitterClient(consumer_key, consumer_secret, access_token, access_token_secret)

  for index, row in df_trends.iterrows():
    print("-------------------------------------------ANALISE DE SENTIMENTOS--------------------------------------------------------------")
    print("O que está sendo comentado no top trendings: " + row['Nome'])
    tweets = twitter_client.get_tweets(query = row['Hashtag'], count = 200)
    
    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positivo']
    
    print("Porcentagem de tweets positivos: {} %".format(100*len(positive_tweets)/len(tweets)))
    
    negatives_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negativo']
    
    print("Porcentagem de tweets negativos: {} %".format(100*len(negatives_tweets)/len(tweets)))
    
    print("Porcentagem de tweets neutros: {} % \
        ".format(100*(len(tweets) -(len( negatives_tweets )+len( positive_tweets)))/len(tweets)))
    
    print("\n\nTweets positivos:")
    for tweet in positive_tweets[:10]:
        print(tweet['text'])
        
    print("\n\nTweets negativos:")
    for tweet in negatives_tweets[:10]:
        print(tweet['text'])
    print("--------------------------------------------FIM ANALISE DE SENTIMENTOS-------------------------------------------------------")

if __name__ == "__main__":
  main()



