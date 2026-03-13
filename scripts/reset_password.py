"""
Script para resetear contraseña por email.
Uso: python scripts/reset_password.py [email] [nueva_password]

Ejemplos:
  python scripts/reset_password.py soralis05@gmail.com nueva123
  python scripts/reset_password.py  (interactivo)
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def reset_password(email=None, password=None):
    """Resetear contraseña de un usuario por email."""
    app = create_app()

    with app.app_context():
        print("="*60)
        print("  RESETEAR CONTRASEÑA")
        print("="*60)
        print()

        # Listar todos los usuarios
        users = User.query.all()
        
        if not users:
            print("[ERROR] No hay usuarios en la base de datos")
            return

        print("Usuarios existentes:")
        print("-"*60)
        print(f"  {'ID':<4} {'Username':<15} {'Email':<30} {'Admin':<6}")
        print("-"*60)
        for user in users:
            admin_str = "SI" if user.is_admin else "NO"
            print(f"  {user.id:<4} {user.username:<15} {user.email:<30} {admin_str:<6}")
        print("-"*60)
        print()

        # Si no se pasa email por argumento, pedir interactivamente
        if not email:
            email = input("Email del usuario: ").strip()

        user = User.query.filter_by(email=email).first()

        if not user:
            print(f"[ERROR] No se encontró usuario con email: {email}")
            return

        print(f"Usuario encontrado: {user.username} ({user.email})")
        print(f"Es administrador: {'SI' if user.is_admin else 'NO'}")
        print()

        # Pedir nueva contraseña si no se pasó por argumento
        if not password:
            password = input("Nueva contraseña: ").strip()
            if not password:
                print("[ERROR] La contraseña no puede estar vacía")
                return

        # Validar longitud
        if len(password) < 6:
            print("[ERROR] La contraseña debe tener al menos 6 caracteres")
            return

        # Actualizar contraseña
        user.password_hash = generate_password_hash(password)
        db.session.commit()

        print()
        print("="*60)
        print("[OK] Contraseña actualizada exitosamente")
        print("="*60)
        print(f"  Usuario: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Nueva contraseña: {password}")
        print("="*60)
        print()
        print("Ahora puedes iniciar sesión en: /auth/login")
        print("="*60)


if __name__ == '__main__':
    try:
        # Si se pasan argumentos por línea de comandos
        if len(sys.argv) >= 3:
            email = sys.argv[1]
            password = sys.argv[2]
            reset_password(email, password)
        else:
            reset_password()
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
