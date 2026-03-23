from app import db
from datetime import datetime, timezone
from typing import Optional


class CartItem(db.Model):
    """Elementos del carrito de compras."""
    __tablename__ = 'cart_items'

    id: db.Column = db.Column(db.Integer, primary_key=True)
    user_id: db.Column = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    session_id: db.Column = db.Column(db.String(100), nullable=True, index=True)
    product_id: db.Column = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    quantity: db.Column = db.Column(db.Integer, default=1, nullable=False)
    added_at: db.Column = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: db.Column = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f'<CartItem {self.product_id} x {self.quantity}>'

    @property
    def subtotal(self) -> float:
        """Calcula el subtotal del item (precio × cantidad)."""
        return float(self.product.price) * self.quantity

    def to_dict(self) -> dict:
        """Convierte el item a diccionario para JSON."""
        return {
            'id': self.id,
            'product_id': self.product.id,
            'product_name': self.product.name,
            'product_image': self.product.get_main_image(),
            'quantity': self.quantity,
            'price': str(self.product.price),
            'subtotal': str(self.subtotal)
        }
