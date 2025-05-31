# API de Produtos Favoritos

API RESTful para gerenciamento de clientes, produtos e favoritos, desenvolvida com Flask, Flask-RESTX, SQLAlchemy e JWT.

## Requisitos

- Python 3.10+
- PostgreSQL

## Instalação

```bash
git clone https://github.com/seuusuario/api_list_fav.git
cd api_list_fav
python -m venv env
env\Scripts\activate  # Windows
# source env/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```
DATABASE_URL=postgresql://postgres:suasenha@localhost:5432/postgres
JWT_SECRET_KEY=sua-chave-secreta
```

## Subindo com Docker

Para construir e iniciar os containers (API + banco de dados):

```bash
docker-compose up --build
```

Acesse a documentação interativa em: [http://localhost:5000/docs](http://localhost:5000/docs)

## Migrações

Dentro do container da API, rode:

```bash
docker-compose exec api_list_fav_app flask db upgrade
```

## Execução local (sem Docker)

```bash
python main.py
```

## Endpoints

- `/auth` - Autenticação
- `/clientes` - Gerenciamento de clientes
- `/favoritos` - Favoritos dos clientes
- `/produtos` - Produtos
