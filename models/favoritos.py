from extensions import db

class Favorite(db.Model):
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255))
    image = db.Column(db.String(500))
    price = db.Column(db.Float)

    client_id = db.Column(db.Integer, db.ForeignKey('public.client.id'), nullable=False)

    # __table_args__ combinando schema e constraint
    __table_args__ = (
        db.UniqueConstraint('product_id', 'client_id', name='uq_product_client'),
        {'schema': 'public'}  # Garante que a tabela favorite também vá para o schema 'public'
    )