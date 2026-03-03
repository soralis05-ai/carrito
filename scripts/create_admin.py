"""
Script para crear usuario administrador.
Ejecutar: python scripts/create_admin.py
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin():
    """Crear usuario administrador."""
    app = create_app()
    
    with app.app_context():
        print("="*50)
        print("  CREAR USUARIO ADMINISTRADOR")
        print("="*50)
        print()
        
        # Pedir datos
        username = input("Nombre de usuario: ").strip()
        if not username:
            print("[ERROR] El nombre de usuario es requerido")
            return
        
        email = input("Email: ").strip()
        if not email or '@' not in email:
            print("[ERROR] Email inválido")
            return
        
        password = input("Contraseña: ").strip()
        if not password or len(password) < 6:
            print("[ERROR] La contraseña debe tener al menos 6 caracteres")
            return
        
        # Verificar si ya existe
        if User.query.filter_by(username=username).first():
            print(f"[ERROR] El usuario '{username}' ya existe")
            return
        
        if User.query.filter_by(email=email).first():
            print(f"[ERROR] El email '{email}' ya está registrado")
            return
        
        # Crear admin
        admin = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            first_name='Admin',
            is_admin=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print()
        print("="*50)
        print("[EXITO] Administrador creado exitosamente")
        print("="*50)
        print(f"  Usuario: {username}")
        print(f"  Email: {email}")
        print(f"  Rol: Administrador")
        print("="*50)
        print()
        print("Ahora puedes iniciar sesión en: /auth/login")
        print("Y acceder al panel de administración: /admin/")
        print("="*50)


if __name__ == '__main__':
    try:
        create_admin()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
