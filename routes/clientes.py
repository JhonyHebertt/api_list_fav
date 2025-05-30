from flask import request
from flask_restx import Namespace, Resource, fields
from models.clientes import Client
from extensions import db
from http import HTTPStatus
from flask_jwt_extended import jwt_required
import re


cl = Namespace("clientes", description="Operações com clientes")

client_input_model = cl.model("ClientInput", {
    "name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

client_output_model = cl.model("ClientOutput", {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
})

@cl.route("/")
class Cliente(Resource):
    @jwt_required()
    @cl.marshal_list_with(client_output_model)
    def get(self):
        return Client.query.all()

    @cl.expect(client_input_model)
    @cl.marshal_with(client_output_model)
    def post(self):
        data = request.get_json()
        if Client.query.filter_by(email=data["email"]).first():
            cl.abort(400, "E-mail já está em uso")
            
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_regex, data["email"]):
            cl.abort(400, "E-mail inválido")

        client = Client()
        client.name = data["name"]
        client.email = data["email"]
        client.password = data["password"]
        db.session.add(client)
        db.session.commit()
        return client, HTTPStatus.CREATED

@cl.route("/<int:id>")
@cl.param("id", "ID do cliente")
class Clientesid(Resource):
    @jwt_required()
    @cl.marshal_with(client_input_model)
    def get(self, id):
        client = Client.query.get_or_404(id)
        return client
    
    @jwt_required()
    @cl.expect(client_output_model)
    @cl.marshal_with(client_output_model)
    def put(self, id):

        client = Client.query.get_or_404(id)
        data = request.get_json()

        if "email" in data:
            if data["email"] != client.email:
                if Client.query.filter_by(email=data["email"]).first():
                    cl.abort(400, "E-mail já está em uso")
            email_regex = r"[^@]+@[^@]+\.[^@]+"
            if not re.match(email_regex, data["email"]):
                cl.abort(400, "E-mail inválido")
            client.email = data["email"]
            
        client.name = data.get("name", client.name)

        db.session.commit()
        return client

    @jwt_required()
    def delete(self, id):
        """Deletar cliente"""
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return {"message": "Cliente deletado com sucesso"}
