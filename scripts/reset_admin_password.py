"""
Script para resetear la contraseña del administrador.
Ejecutar: python scripts/reset_admin_password.py
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def reset_password():
    """Resetear contraseña del administrador."""
    app = create_app()

    with app.app_context():
        print("="*60)
        print("  RESETEAR CONTRASEÑA DE ADMINISTRADOR")
        print("="*60)
        print()

        # Buscar admin
        admin = User.query.filter_by(is_admin=True).first()

        if not admin:
            print("[ERROR] No se encontró ningún administrador")
            print("Ejecuta: python scripts/create_admin.py")
            return

        # Mostrar info del admin
        print(f"Administrador encontrado:")
        print(f"  Username: {admin.username}")
        print(f"  Email: {admin.email}")
        print()

        # Pedir nueva contraseña
        print("Ingresa la nueva contraseña:")
        password = input("Nueva contraseña: ").strip()
        
        if not password or len(password) < 6:
            print("[ERROR] La contraseña debe tener al menos 6 caracteres")
            return

        password_confirm = input("Confirmar contraseña: ").strip()

        if password != password_confirm:
            print("[ERROR] Las contraseñas no coinciden")
            return

        # Confirmar
        print()
        confirm = input("¿Estás seguro de cambiar la contraseña? (SI/no): ").strip()

        if confirm.upper() != 'SI':
            print("Operación cancelada")
            return

        # Actualizar contraseña
        admin.password_hash = generate_password_hash(password)
        db.session.commit()

        print()
        print("="*60)
        print("[OK] Contraseña actualizada exitosamente")
        print("="*60)
        print(f"  Usuario: {admin.username}")
        print(f"  Email: {admin.email}")
        print(f"  Nueva contraseña: {password}")
        print("="*60)
        print()
        print("Ahora puedes iniciar sesión en: /auth/login")
        print("="*60)


def list_admins():
    """Listar todos los administradores."""
    app = create_app()

    with app.app_context():
        admins = User.query.filter_by(is_admin=True).all()

        if not admins:
            print("No hay administradores en la base de datos")
            return

        print("="*60)
        print(f"  {'ID':<4} {'Username':<20} {'Email':<30}")
        print("="*60)

        for admin in admins:
            print(f"  {admin.id:<4} {admin.username:<20} {admin.email:<30}")

        print("="*60)
        print(f"Total: {len(admins)} administrador(s)")
        print("="*60)


if __name__ == '__main__':
    try:
        # Si se pasa --list como argumento, solo listar
        if len(sys.argv) > 1 and sys.argv[1] == '--list':
            list_admins()
        else:
            reset_password()
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
