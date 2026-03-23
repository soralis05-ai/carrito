"""
Tests unitarios para CartService.
Ejecutar: python -m pytest tests/test_cart.py -v
"""

import pytest
from app import create_app, db
from app.models import Product, CartItem, User
from app.blueprints.cart.services import CartService
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Crear app para tests."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        
        # Crear producto de prueba
        product = Product(
            name='Producto Test',
            slug='producto-test',
            price=10.00,
            stock=100
        )
        db.session.add(product)
        
        # Crear usuario de prueba
        user = User(
            username='testuser',
            email='test@test.com',
            password_hash=generate_password_hash('password')
        )
        db.session.add(user)
        
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Crear cliente de test."""
    return app.test_client()


def test_add_item_to_cart(app):
    """Test: Añadir item al carrito."""
    with app.app_context():
        user = User.query.first()
        product = Product.query.first()
        
        # Añadir al carrito
        CartService.add_item(
            product_id=product.id,
            quantity=2,
            user_id=user.id
        )
        
        # Verificar que se añadió
        cart_items = CartService.get_cart_items(user_id=user.id)
        assert len(cart_items) == 1
        assert cart_items[0]['quantity'] == 2
        assert cart_items[0]['product_id'] == product.id


def test_update_cart_item_quantity(app):
    """Test: Actualizar cantidad de item."""
    with app.app_context():
        user = User.query.first()
        product = Product.query.first()
        
        # Añadir y actualizar
        CartService.add_item(product_id=product.id, quantity=2, user_id=user.id)
        cart_item = CartItem.query.first()
        
        CartService.update_item(item_id=cart_item.id, quantity=5, user_id=user.id)
        
        # Verificar actualización
        cart_item = CartItem.query.first()
        assert cart_item.quantity == 5


def test_remove_item_from_cart(app):
    """Test: Eliminar item del carrito."""
    with app.app_context():
        user = User.query.first()
        product = Product.query.first()
        
        # Añadir y eliminar
        CartService.add_item(product_id=product.id, quantity=1, user_id=user.id)
        cart_item = CartItem.query.first()
        
        CartService.remove_item(item_id=cart_item.id, user_id=user.id)
        
        # Verificar que se eliminó
        cart_items = CartService.get_cart_items(user_id=user.id)
        assert len(cart_items) == 0


def test_calculate_cart_total(app):
    """Test: Calcular total del carrito."""
    with app.app_context():
        user = User.query.first()
        product = Product.query.first()
        
        # Añadir 2 productos iguales
        CartService.add_item(product_id=product.id, quantity=2, user_id=user.id)
        
        # Calcular total
        total = CartService.calculate_total(user_id=user.id)
        
        # Verificar total (10.00 * 2 = 20.00)
        assert total == 20.00


def test_count_cart_items(app):
    """Test: Contar items del carrito."""
    with app.app_context():
        user = User.query.first()
        product = Product.query.first()
        
        # Añadir 3 items
        CartService.add_item(product_id=product.id, quantity=3, user_id=user.id)
        
        # Contar items
        count = CartService.count_items(user_id=user.id)
        
        # Verificar cantidad
        assert count == 3


def test_clear_cart(app):
    """Test: Vaciar carrito completo."""
    with app.app_context():
        user = User.query.first()
        product = Product.query.first()
        
        # Añadir múltiples items
        CartService.add_item(product_id=product.id, quantity=1, user_id=user.id)
        CartService.add_item(product_id=product.id, quantity=2, user_id=user.id)
        
        # Vaciar carrito
        CartService.clear_cart(user_id=user.id)
        
        # Verificar que está vacío
        cart_items = CartService.get_cart_items(user_id=user.id)
        assert len(cart_items) == 0
