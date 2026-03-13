"""
Script para crear usuario administrador (versión no interactiva).

Uso:
  python scripts/create_admin_quick.py username email password

Ejemplo:
  python scripts/create_admin_quick.py admin soralis05@gmail.com mi_password_123
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin_quick(username, email, password):
    """Crear administrador sin interacción."""
    app = create_app()

    with app.app_context():
        print("="*60)
        print("  CREAR ADMINISTRADOR")
        print("="*60)
        print()

        # Validaciones
        if not username or len(username) < 3:
            print("[ERROR] El username debe tener al menos 3 caracteres")
            return False

        if not email or '@' not in email:
            print("[ERROR] Email inválido")
            return False

        if not password or len(password) < 6:
            print("[ERROR] La contraseña debe tener al menos 6 caracteres")
            return False

        # Verificar si ya existe
        if User.query.filter_by(username=username).first():
            print(f"[INFO] El username '{username}' ya existe")
            return False

        if User.query.filter_by(email=email).first():
            print(f"[INFO] El email '{email}' ya está registrado")
            
            # Preguntar si quiere resetear la contraseña
            user = User.query.filter_by(email=email).first()
            print(f"¿Quieres resetear la contraseña de '{user.username}'? (SI/no)")
            
            # En modo no interactivo, solo informamos
            print("[INFO] Usa: python scripts/reset_password.py", email, password)
            return False

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

        print("="*60)
        print("[EXITO] Administrador creado exitosamente")
        print("="*60)
        print(f"  Username: {username}")
        print(f"  Email: {email}")
        print(f"  Contraseña: {password}")
        print(f"  Rol: Administrador")
        print("="*60)
        print()
        print("Login: /auth/login")
        print("Admin:  /admin/")
        print("="*60)
        return True


if __name__ == '__main__':
    try:
        if len(sys.argv) >= 4:
            username = sys.argv[1]
            email = sys.argv[2]
            password = sys.argv[3]
            create_admin_quick(username, email, password)
        else:
            print("Uso: python scripts/create_admin_quick.py username email password")
            print()
            print("Ejemplo:")
            print("  python scripts/create_admin_quick.py admin soralis05@gmail.com mi_password_123")
            sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
