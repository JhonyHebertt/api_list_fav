# API de Favoritos

API RESTful para gerenciamento de clientes, produtos e favoritos, desenvolvida com Flask, Flask-RESTX, SQLAlchemy e JWT.

## Requisitos

- Python 3.10+
- PostgreSQL

## Instalação

```bash
git clone https://github.com/seuusuario/list_fav.git
cd list_fav
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

## Migrações

```bash
flask db init
flask db migrate
flask db upgrade
```

## Execução

```bash
python main.py
```

Acesse a documentação interativa em: [http://localhost:5000/docs](http://localhost:5000/docs)

## Endpoints

- `/auth` - Autenticação
- `/clientes` - Gerenciamento de clientes
- `/favoritos` - Favoritos dos clientes
- `/produtos` - Produtos