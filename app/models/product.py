from app import db
from datetime import datetime


class Category(db.Model):
    """Categorías de productos."""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con productos
    products = db.relationship('Product', backref='category', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    """Productos de la tienda."""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(50), unique=True, nullable=True, index=True)
    
    # Imágenes (almacena JSON con lista de nombres de archivo)
    image_main = db.Column(db.String(255), nullable=True)  # Imagen principal
    images = db.Column(db.JSON, nullable=True)  # Lista de imágenes adicionales
    
    # Costos de producción (almacena JSON con estructura de costos)
    costos = db.Column(db.JSON, nullable=True)  # Costos de amigurumis

    # Categoría
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True, index=True)
    
    # Estado
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    @property
    def price_display(self):
        """Retorna el precio formateado con símbolo de euro."""
        return f"€{self.price}"
    
    @property
    def is_in_stock(self):
        """Verifica si hay stock disponible."""
        return self.stock > 0
    
    def get_main_image(self):
        """Obtiene la imagen principal o la primera de la lista."""
        if self.image_main:
            return self.image_main
        if self.images and len(self.images) > 0:
            return self.images[0]
        return None
    
    def get_all_images(self):
        """Obtiene todas las imágenes (principal + adicionales)."""
        all_images = []
        if self.image_main:
            all_images.append(self.image_main)
        if self.images:
            all_images.extend([img for img in self.images if img != self.image_main])
        return all_images
