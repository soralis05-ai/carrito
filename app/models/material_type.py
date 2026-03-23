from typing import Optional
from app import db
from datetime import datetime, timezone


class MaterialType(db.Model):
    """Tipos de materiales para amigurumis."""
    __tablename__ = 'material_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    default_cost = db.Column(db.Numeric(10, 2), default=0)  # Costo por defecto
    default_weight = db.Column(db.Integer, default=50)  # Peso por defecto en gramos
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f'<MaterialType {self.name}>'

    def to_dict(self) -> dict:
        """Convertir a diccionario."""
        return {
            'id': self.id,
            'name': self.name,
            'default_cost': float(self.default_cost) if self.default_cost else 0,
            'default_weight': self.default_weight,
            'description': self.description,
            'is_active': self.is_active
        }
