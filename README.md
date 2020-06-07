# flood-control-api

Projeto para desenvolvimento de API do projeto da disciplina de TIS-V. 

## Instalação do Ambiente
```
virtualenv --python python3.7 env
source env/bin/activate
```
```
pip install -r requirements.txt
```

## Variáveis de ambiente 
Para execução da API, as seguintes variáveis de ambiente devem ser configuradas:
```
DB_USER --> user do banco;
DB_PASS --> senha do banco ;
DB_IP --> host do banco;
DB --> nome schema;
TOKEN_SECRET --> segredo do token jwt;
TWITTER_ACCESS_TOKEN --> Twitter API Access token;
TWITTER_ACCESS_TOKEN_SECRET --> Twitter API Access token secret;
TWITTER_CONSUMER_KEY --> Twitter API key;
TWITTER_CONSUMER_SECRET --> Twitter API secret key;
```

## Execução 
```
python run.py
```


## Testes unitários 
```
coverage run --omit="tests/*,env/*" -m unittest discover
coverage report -m 
```