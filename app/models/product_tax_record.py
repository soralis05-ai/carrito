from typing import Optional
from app import db
from datetime import datetime, timezone


class ProductTaxRecord(db.Model):
    """Registro de costos e impuestos por producto."""
    __tablename__ = 'product_tax_records'

    id = db.Column(db.Integer, primary_key=True)

    # Información del producto
    product_name = db.Column(db.String(200), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=True, index=True)

    # Costos de producción
    material_cost = db.Column(db.Numeric(10, 2), default=0)
    material_iva_percent = db.Column(db.Integer, default=21)
    labor_cost = db.Column(db.Numeric(10, 2), default=0)

    # Utilidad
    profit_percent = db.Column(db.Integer, default=20)
    profit_amount = db.Column(db.Numeric(10, 2), default=0)

    # Cálculos derivados
    material_base = db.Column(db.Numeric(10, 2), default=0)
    material_iva = db.Column(db.Numeric(10, 2), default=0)
    cost_total = db.Column(db.Numeric(10, 2), default=0)
    base_price = db.Column(db.Numeric(10, 2), default=0)

    # Impuestos
    iva_repercutido = db.Column(db.Numeric(10, 2), default=0)
    iva_soportado = db.Column(db.Numeric(10, 2), default=0)
    iva_ingresar = db.Column(db.Numeric(10, 2), default=0)
    irpf_percent = db.Column(db.Integer, default=15)
    irpf_amount = db.Column(db.Numeric(10, 2), default=0)

    # Precio final
    sale_price = db.Column(db.Numeric(10, 2), default=0)
    net_profit = db.Column(db.Numeric(10, 2), default=0)

    # Datos fiscales
    autonomo_fee = db.Column(db.Numeric(10, 2), default=80)
    monthly_units = db.Column(db.Integer, default=10)

    # Fechas
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Estado
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self) -> str:
        return f'<ProductTaxRecord {self.product_name}>'

    def to_dict(self) -> dict:
        """Convertir a diccionario."""
        return {
            'id': self.id,
            'product_name': self.product_name,
            'category': self.category,
            'material_cost': float(self.material_cost),
            'material_iva_percent': self.material_iva_percent,
            'labor_cost': float(self.labor_cost),
            'profit_percent': self.profit_percent,
            'profit_amount': float(self.profit_amount),
            'cost_total': float(self.cost_total),
            'base_price': float(self.base_price),
            'iva_repercutido': float(self.iva_repercutido),
            'iva_soportado': float(self.iva_soportado),
            'iva_ingresar': float(self.iva_ingresar),
            'irpf_percent': self.irpf_percent,
            'irpf_amount': float(self.irpf_amount),
            'sale_price': float(self.sale_price),
            'net_profit': float(self.net_profit),
            'created_at': self.created_at.strftime('%d/%m/%Y') if self.created_at else None,
        }
