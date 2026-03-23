from typing import Optional
from app import db
from datetime import datetime, timezone


class PortfolioInfo(db.Model):
    """Información personal del portfolio."""
    __tablename__ = 'portfolio_info'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f'<PortfolioInfo {self.name}>'

    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario."""
        return {
            'name': self.name,
            'title': self.title,
            'bio': self.bio,
            'email': self.email,
            'phone': self.phone
        }

    @classmethod
    def get_or_create(cls) -> 'PortfolioInfo':
        """Obtiene el primer registro o crea uno por defecto."""
        info = cls.query.first()
        if not info:
            info = cls(
                name='Almapunt',
                title='Artesanía y Productos Únicos',
                bio='Somos una tienda especializada en productos artesanales y únicos. Cada pieza está seleccionada con cuidado para ofrecer calidad y originalidad a nuestros clientes.',
                email='soralis05@gmail.com',
                phone=''
            )
            db.session.add(info)
            db.session.commit()
        return info
