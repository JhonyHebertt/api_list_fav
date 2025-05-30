from extensions import db

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255))
    image = db.Column(db.String(500))
    price = db.Column(db.Float)

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('product_id', 'client_id', name='uq_product_client'),
    )
