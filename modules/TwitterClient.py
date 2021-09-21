import os
import re

import tweepy

from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):

  def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
      '''
      Construtor da classe TwitterClient
      '''
      self.consumer_key = consumer_key
      self.consumer_secret = consumer_secret
      self.access_token = access_token
      self.access_token_secret = access_token_secret

      # Tentar autenticação
      try:
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(self.auth)

      except:
        print("Autenticação Falhou!")

  def clean_tweet(self, tweet):
    '''
    Remove links, caracteres especiais usando Regex
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

  def get_sentiment_in_tweet(self, tweet):
    '''
    Utiliza a biblioteca TextBlob para classificar o sentimento em
    determinado tweet.
    '''
    analysis = TextBlob(self.clean_tweet(tweet))

    if analysis.sentiment.polarity > 0:
      return "positivo"
    elif analysis.sentiment.polarity == 0:
      return "neutro"
    else:
      return "negativo"
  
  def get_tweets(self, query, count=10):
    '''
    Função utilizada para obter 10 tweets usando uma query;
    que pode ser uma palavra, nome, frase
    '''
    tweets = []

    try:
      fetched_tweets = self.api.search(q=query, count=count)

      for tweet in fetched_tweets:
        parsed_tweets = {}

        parsed_tweets['text'] = tweet.text
        parsed_tweets['sentiment'] = self.get_sentiment_in_tweet(tweet.text)

        if tweet.retweet_count > 0:
          # Garante que não haverá tweets repetidos
          if parsed_tweets not in tweets:
            tweets.append(parsed_tweets)
        else:
          tweets.append(parsed_tweets)

      return tweets
    except tweepy.TweepError as e:
      print('Error: ' + str(e))



