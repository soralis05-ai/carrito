from app import db
from datetime import datetime


class PortfolioItem(db.Model):
    """Items del portfolio (imágenes destacadas)."""
    __tablename__ = 'portfolio_items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    image = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, default=999, index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PortfolioItem {self.title}>'

    def to_dict(self):
        """Convierte el objeto a diccionario."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'order': self.order,
            'is_active': self.is_active
        }

    @classmethod
    def get_all_active(cls):
        """Obtiene todos los items activos ordenados."""
        return cls.query.filter_by(is_active=True).order_by(cls.order).all()
