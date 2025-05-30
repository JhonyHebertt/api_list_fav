import requests
from flask import request 
from flask_restx import Namespace, Resource, fields, reqparse
from models.favoritos import Favorite
from models.clientes import Client
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

fv = Namespace("favoritos", description="Favoritos de clientes")

model_favorito = fv.model("Favorite", {
    "id": fields.Integer(readOnly=True),
    "product_id": fields.Integer(required=True),
    "title": fields.String,
    "image": fields.String,
    "price": fields.Float,
    "client_id": fields.Integer,
})

pagination_args = reqparse.RequestParser()
pagination_args.add_argument('page', type=int, required=False, default=1, help='Número da página', location='args')
pagination_args.add_argument('per_page', type=int, required=False, default=10, help='Itens por página', location='args')


model_paginated_favoritos = fv.model("PaginatedFavoritos", {
    "page": fields.Integer(description="Número da página atual"),
    "per_page": fields.Integer(description="Número de itens por página"),
    "total_pages": fields.Integer(description="Número total de páginas"),
    "total_items": fields.Integer(description="Número total de itens encontrados"),
    "items": fields.List(fields.Nested(model_favorito), description="Lista de favoritos na página atual")    
})

@fv.route("/<int:client_id>")
@fv.param("client_id", "ID do cliente")
class Favoritos(Resource):
    @jwt_required()
    @fv.expect(pagination_args)  
    @fv.marshal_with(model_paginated_favoritos) 
    def get(self, client_id):
        current_user = int(get_jwt_identity())
        if current_user != client_id:
            fv.abort(403, "Acesso negado")
            
        client = Client.query.get_or_404(client_id)
        if not client:
            fv.abort(404, f"Cliente com id {client_id} não encontrado")

        args = pagination_args.parse_args() 
        page = args['page']
        per_page = args['per_page']
        
        pagination = Favorite.query.filter_by(client_id=client_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_pages": pagination.pages,
            "total_items": pagination.total,
            "items": pagination.items            
        }

    @jwt_required()
    @fv.expect(model_favorito)
    @fv.marshal_with(model_favorito)
    def post(self, client_id):
        client = Client.query.get(client_id)
        if not client:
            fv.abort(404, f"Cliente com id {client_id} não encontrado")

        data = request.get_json() 
        product_id = data.get("product_id") 

        if not product_id:
            fv.abort(400, "ID do produto é obrigatório")

        exists = Favorite.query.filter_by(client_id=client_id, product_id=product_id).first()
        if exists:
            fv.abort(400, "Produto já está nos favoritos")

        try:
            response = requests.get(f"https://fakestoreapi.com/products/{product_id}")
            response.raise_for_status() 
            
           
            if not response.content:
                 fv.abort(404, "Produto não encontrado na API externa (resposta vazia)!")

            product = response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                fv.abort(404, f"Produto com ID {product_id} não encontrado na API externa.")
            else:
                fv.abort(e.response.status_code, f"Erro ao buscar produto na API externa: {e}")
        except ValueError:
            fv.abort(502, "Resposta inesperada (formato JSON inválido) da API externa")
        except requests.exceptions.RequestException as e:
            fv.abort(503, f"Erro de comunicação com a API externa: {e}")


        fav = Favorite()
        fav.product_id = product.get("id")
        fav.title = product.get("title")
        fav.image = product.get("image")
        fav.price = product.get("price")
        fav.client_id = client_id
        
        db.session.add(fav)
        db.session.commit()
        return fav, 201

@fv.route("/<int:client_id>/<int:product_id>")
@fv.param("client_id", "ID do cliente")
@fv.param("product_id", "ID do produto")
class DeletarFavorito(Resource):
    @jwt_required()
    @fv.response(200, "Produto removido dos favoritos") 
    @fv.response(404, "Favorito não encontrado")
    def delete(self, client_id, product_id):
        current_user = int(get_jwt_identity()) 

        if current_user != client_id:
             fv.abort(403, "Acesso negado para deletar favoritos de outro cliente.")

        favorite = Favorite.query.filter_by(client_id=client_id, product_id=product_id).first()
        if not favorite:
            fv.abort(404, "Favorito não encontrado")
        
        db.session.delete(favorite)
        db.session.commit()
        return {"message": "Produto removido dos favoritos"}, 200