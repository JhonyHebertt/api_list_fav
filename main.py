from flask import Flask
from config import Config
from extensions import db, migrate, jwt, api
from routes.clientes import cl as clients_cl
from routes.favoritos import fv as favorites_fv
from routes.produtos import pd as products_pd
from routes.auth import ns as auth_ns
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Adicione 'Bearer <seu_token>'"
        }
    }

    api.init_app(
        app,
        doc="/docs",
        title="API de Favoritos",
        authorizations=authorizations,
        security="Bearer Auth"
    )
    api.add_namespace(auth_ns)
    api.add_namespace(clients_cl)
    api.add_namespace(favorites_fv)
    api.add_namespace(products_pd)

    return app

app = create_app()

if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
