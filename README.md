# Data Challenge Carrefour
**Objetivo:** Desenvolver uma aplicação para monitorar o top trendings do **Twitter**. Devendo ser possivel, visualizar o volume de cada *hashtag* que foi subida.

## Antes de começar
Na pasta `docker` está o arquivo `docker-compose.yml` para subir o banco de dados **NoSQL** **MongoDb**. 

O arquivo `App.ipynb` é o arquivo principal do projeto e na pasta `modules` é onde se encontra os arquivos **Python** que serão usado para se conectar ao banco, converter arquivo de texto em dicionario e Realizar a analise de sentimentos usando os tweets que estão no top trending . Além disso, foi criado um arquivo `.env` para armazer as minhas chaves do **Twitter API** do qual estão lidas usando o `dotenv` e armazenadas em um dicionario.


O arquivo `main.py` foi usado para apresentar no video, porém ele é direto e objetivo em relação ao `App.ipynb` que possui as fontes que eu usei para concluir o desafio e algumas explições.

Esse repositorio possui *branches* que representam o desenvolvimento de cada funcionalidade, inclusive duas funcionalidades extras que são: Twitter Client e desenvolver um resumão do que foi feito através do `main.py`.

