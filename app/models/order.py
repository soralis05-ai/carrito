from app import db
from datetime import datetime


class Order(db.Model):
    """Pedidos de clientes."""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Cliente
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    guest_email = db.Column(db.String(120), nullable=True)  # Para invitados
    
    # Estado del pedido
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'
    
    status = db.Column(db.String(20), default=STATUS_PENDING, index=True)
    
    # Dirección de envío
    shipping_address = db.Column(db.Text, nullable=True)
    shipping_city = db.Column(db.String(100), nullable=True)
    shipping_zip = db.Column(db.String(20), nullable=True)
    shipping_country = db.Column(db.String(100), default='España')
    shipping_phone = db.Column(db.String(20), nullable=True)
    
    # Totales
    subtotal = db.Column(db.Numeric(10, 2), default=0)
    shipping_cost = db.Column(db.Numeric(10, 2), default=0)
    tax = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), default=0)
    
    # Pagos
    payment_method = db.Column(db.String(50), nullable=True)
    payment_status = db.Column(db.String(20), default='pending')
    payment_id = db.Column(db.String(255), nullable=True)  # ID de Stripe/PayPal
    
    # Notas
    notes = db.Column(db.Text, nullable=True)
    
    # Fechas
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    
    # Relación con items
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'
    
    @property
    def total_display(self):
        """Retorna el total formateado con símbolo de euro."""
        return f"€{self.total}"
    
    @property
    def items_count(self):
        """Cantidad total de items en el pedido."""
        return sum(item.quantity for item in self.items)
    
    def generate_order_number(self):
        """Genera número de pedido único."""
        from datetime import datetime
        date_str = datetime.now().strftime('%Y%m%d')
        last_order = Order.query.filter(
            Order.order_number.like(f'PED-{date_str}-%')
        ).order_by(Order.id.desc()).first()
        
        if last_order:
            last_num = int(last_order.order_number.split('-')[-1])
            new_num = last_num + 1
        else:
            new_num = 1
        
        return f'PED-{date_str}-{str(new_num).zfill(4)}'


class OrderItem(db.Model):
    """Items individuales de un pedido."""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    
    # Información del producto al momento de la compra
    product_name = db.Column(db.String(200), nullable=False)
    product_sku = db.Column(db.String(50), nullable=True)
    
    # Cantidad y precio
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.product_name} x {self.quantity}>'
    
    @property
    def total_display(self):
        """Retorna el total formateado con símbolo de euro."""
        return f"€{self.total}"
