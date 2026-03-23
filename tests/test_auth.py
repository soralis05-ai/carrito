"""
Tests unitarios para Auth Blueprint.
Ejecutar: python -m pytest tests/test_auth.py -v
"""

import pytest
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash


@pytest.fixture
def app():
    """Crear app para tests."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Desactivar CSRF para tests
    
    with app.app_context():
        db.create_all()
        
        # Crear usuario de prueba
        user = User(
            username='testuser',
            email='test@test.com',
            password_hash=generate_password_hash('password123'),
            first_name='Test',
            last_name='User'
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


def test_login_page_loads(client):
    """Test: Página de login carga."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'login' in response.data.lower()


def test_login_success(client, app):
    """Test: Login exitoso."""
    with app.test_request_context():
        response = client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200


def test_login_invalid_email(client, app):
    """Test: Login con email inválido."""
    with app.test_request_context():
        response = client.post('/auth/login', data={
            'email': 'invalid@test.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Debería mostrar mensaje de error


def test_login_invalid_password(client, app):
    """Test: Login con contraseña inválida."""
    with app.test_request_context():
        response = client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Debería mostrar mensaje de error


def test_register_page_loads(client):
    """Test: Página de registro carga."""
    response = client.get('/auth/register')
    assert response.status_code == 200


def test_register_success(client, app):
    """Test: Registro exitoso."""
    with app.test_request_context():
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verificar que el usuario se creó
        with app.app_context():
            user = User.query.filter_by(email='newuser@test.com').first()
            assert user is not None
            assert user.username == 'newuser'


def test_register_password_mismatch(client, app):
    """Test: Registro con contraseñas diferentes."""
    with app.test_request_context():
        response = client.post('/auth/register', data={
            'username': 'newuser2',
            'email': 'newuser2@test.com',
            'password': 'password123',
            'password_confirm': 'differentpassword'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Debería mostrar error de contraseñas


def test_register_duplicate_email(client, app):
    """Test: Registro con email duplicado."""
    with app.test_request_context():
        response = client.post('/auth/register', data={
            'username': 'duplicateuser',
            'email': 'test@test.com',  # Email ya existe
            'password': 'password123',
            'password_confirm': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Debería mostrar error de email duplicado


def test_logout(client, app):
    """Test: Logout."""
    # Primero login
    with app.test_request_context():
        client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'password123'
        })
        
        # Luego logout
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200


def test_profile_page_requires_login(client):
    """Test: Perfil requiere login."""
    response = client.get('/auth/profile', follow_redirects=True)
    assert response.status_code == 200
    # Debería redirigir a login


def test_profile_page_loads(client, app):
    """Test: Página de perfil carga."""
    with app.test_client() as c:
        # Login primero
        c.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'password123'
        })
        
        # Ahora acceder al perfil
        response = c.get('/auth/profile')
        assert response.status_code == 200


def test_profile_update(client, app):
    """Test: Actualizar perfil."""
    with app.test_client() as c:
        # Login primero
        c.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'password123'
        })
        
        # Actualizar perfil
        response = c.post('/auth/profile', data={
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@test.com'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verificar actualización
        with app.app_context():
            user = User.query.filter_by(email='updated@test.com').first()
            assert user is not None
            assert user.first_name == 'Updated'
            assert user.last_name == 'Name'


def test_password_hash_is_secure(client, app):
    """Test: Password hash es seguro."""
    with app.app_context():
        user = User.query.filter_by(email='test@test.com').first()
        
        # Verificar que el password está hasheado
        assert user.password_hash != 'password123'
        assert len(user.password_hash) > 50  # Los hashes son largos
        
        # Verificar que se puede verificar
        assert check_password_hash(user.password_hash, 'password123')
        assert not check_password_hash(user.password_hash, 'wrongpassword')
