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
```

## Execução 
```
python run.py
```