from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import   create_access_token
from models.clientes import Client

ns = Namespace("auth", description="Autenticação")

login_model = ns.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

@ns.route("/login")
class LoginResource(Resource):
    @ns.expect(login_model)
    def post(self):
        
        data = request.get_json()
        client = Client.query.filter_by(email=data["email"]).first()
        if not client or not client.check_password(data["password"]):
            return {"message": "Credenciais inválidas"}, 401

        identity = str(client.id)
        return {
            "access_token": create_access_token(identity=identity)
        }, 200
