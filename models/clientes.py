from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column("password", db.String(256), nullable=False)

    favorites = db.relationship("Favorite", backref="client", cascade="all, delete-orphan")

    @property
    def password(self):
        raise AttributeError("Senha não pode ser lida diretamente")

    @password.setter
    def password(self, plain_password):
        self._password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self._password, plain_password)