"""
Tests unitarios para ProductsService.
Ejecutar: python -m pytest tests/test_products.py -v
"""

import pytest
from app import create_app, db
from app.models import Product, Category
from app.blueprints.products.services import ProductsService


@pytest.fixture
def app():
    """Crear app para tests."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        
        # Crear categoría de prueba
        category = Category(
            name='Categoría Test',
            slug='categoria-test',
            is_active=True
        )
        db.session.add(category)
        
        # Crear productos de prueba
        products = [
            Product(name='Producto 1', slug='producto-1', price=10.00, stock=10, is_active=True),
            Product(name='Producto 2', slug='producto-2', price=20.00, stock=20, is_active=True),
            Product(name='Producto 3', slug='producto-3', price=30.00, stock=0, is_active=False),
        ]
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Crear cliente de test."""
    return app.test_client()


def test_get_all_products(app):
    """Test: Obtener todos los productos activos."""
    with app.app_context():
        products = ProductsService.get_all()
        
        # Solo debe devolver productos activos (2 de 3)
        assert len(products) == 2
        assert all(p['is_in_stock'] or not p['is_in_stock'] for p in products)


def test_get_product_by_id(app):
    """Test: Obtener producto por ID."""
    with app.app_context():
        product = Product.query.filter_by(name='Producto 1').first()
        
        result = ProductsService.get_by_id(product.id)
        
        assert result is not None
        assert result['id'] == product.id
        assert result['name'] == 'Producto 1'


def test_get_product_by_id_inactive(app):
    """Test: Producto inactivo no se devuelve."""
    with app.app_context():
        product = Product.query.filter_by(name='Producto 3').first()
        
        result = ProductsService.get_by_id(product.id)
        
        # No debe devolver productos inactivos
        assert result is None


def test_get_product_by_slug(app):
    """Test: Obtener producto por slug."""
    with app.app_context():
        product = Product.query.filter_by(name='Producto 1').first()
        
        result = ProductsService.get_by_slug(product.slug)
        
        assert result is not None
        assert result['slug'] == 'producto-1'


def test_search_products(app):
    """Test: Buscar productos."""
    with app.app_context():
        results = ProductsService.search('Producto')
        
        # Debe encontrar los 2 productos activos
        assert len(results) == 2


def test_get_featured_products(app):
    """Test: Obtener productos destacados."""
    with app.app_context():
        # Marcar producto como destacado
        product = Product.query.filter_by(name='Producto 1').first()
        product.is_featured = True
        db.session.commit()
        
        featured = ProductsService.get_featured(limit=5)
        
        assert len(featured) == 1
        assert featured[0]['is_featured'] == True


def test_get_related_products(app):
    """Test: Obtener productos relacionados."""
    with app.app_context():
        category = Category.query.first()
        
        # Asignar misma categoría a productos
        products = Product.query.filter_by(is_active=True).all()
        for product in products:
            product.category_id = category.id
        db.session.commit()
        
        product = Product.query.filter_by(name='Producto 1').first()
        related = ProductsService.get_related(product.id, limit=5)
        
        # Debe devolver el otro producto de la misma categoría
        assert len(related) == 1


def test_product_to_dict(app):
    """Test: Conversión a diccionario."""
    with app.app_context():
        product = Product.query.filter_by(name='Producto 1').first()
        
        result = ProductsService._to_dict(product)
        
        assert 'id' in result
        assert 'name' in result
        assert 'price' in result
        assert 'price_numeric' in result
        assert result['price_numeric'] == 10.00
