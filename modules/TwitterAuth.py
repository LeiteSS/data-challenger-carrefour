import requests

class TwitterAuth(requests.auth.AuthBase):
  ''''
  Classe para se autenticar e se conectar à url onde será feito a pesquisa

  Fonte: https://copdips.com/2019/04/creating-custom-python-request-auth-class.html
  '''
  def __init__(self, bearer_token):
      self.bearer_token = bearer_token

  def __call__(self, r: requests.Request):
      '''
      A classe Request será chamada autenticar usando o Bearer Token. Por mais que não irá logar no twitter o 
      bearer token "representa uma autorização do Server emitida para o client. 
      Por sua vez, o client deve possuir mecanismos próprios para identificar e validar o Token".

      Fonte: https://www.brunobrito.net.br/jwt-cookies-oauth-bearer/
      '''

      r.headers["Authorization"] = f"Bearer {self.bearer_token}"
      r.headers["User-Agent"] = "v2RecentSearchPyth"

      return r
  
  def connect_to_endpoint(self, url, params):
      '''
      Se conecta a url dada com o parametro(s) dado(s).
      Consultar a documentação para saber o parametros nessario na pesquisa.

      Fonte: https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py
      '''
      response = requests.get(url, auth=self.__call__, params=params)
      print(response.status_code)
      if response.status_code != 200:
          raise Exception(response.status_code, response.text)
        
      return response.json()
