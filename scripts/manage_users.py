"""
Script para gestionar usuarios (listar/eliminar).
Ejecutar: python scripts/manage_users.py
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User

def list_users():
    """Listar todos los usuarios."""
    app = create_app()
    
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("No hay usuarios en la base de datos")
            return
        
        print("="*70)
        print(f"  {'ID':<4} {'Username':<20} {'Email':<30} {'Admin':<6}")
        print("="*70)
        
        for user in users:
            admin_str = "SI" if user.is_admin else "NO"
            print(f"  {user.id:<4} {user.username:<20} {user.email:<30} {admin_str:<6}")
        
        print("="*70)
        print(f"Total: {len(users)} usuario(s)")
        print("="*70)


def delete_user():
    """Eliminar usuario por ID o email."""
    app = create_app()
    
    with app.app_context():
        print("="*50)
        print("  ELIMINAR USUARIO")
        print("="*50)
        print()
        
        # Primero listar
        list_users()
        print()
        
        # Pedir criterio de busqueda
        print("¿Como quieres buscar el usuario?")
        print("  1. Por ID")
        print("  2. Por Email")
        opcion = input("Opcion (1-2): ").strip()
        
        user = None
        
        if opcion == '1':
            user_id = input("ID del usuario: ").strip()
            if user_id.isdigit():
                user = User.query.get(int(user_id))
        elif opcion == '2':
            email = input("Email del usuario: ").strip()
            user = User.query.filter_by(email=email).first()
        
        if not user:
            print("[ERROR] Usuario no encontrado")
            return
        
        # Mostrar datos
        print()
        print("="*50)
        print(f"  Usuario a eliminar:")
        print(f"    ID: {user.id}")
        print(f"    Username: {user.username}")
        print(f"    Email: {user.email}")
        print(f"    Admin: {'SI' if user.is_admin else 'NO'}")
        print("="*50)
        print()
        
        # Confirmar
        confirm = input("¿Estas seguro de eliminar este usuario? (SI/no): ").strip()
        
        if confirm.upper() != 'SI':
            print("Operacion cancelada")
            return
        
        # Eliminar
        db.session.delete(user)
        db.session.commit()
        
        print()
        print("[OK] Usuario eliminado exitosamente")
        print("="*50)


def make_admin():
    """Convertir usuario en administrador."""
    app = create_app()
    
    with app.app_context():
        print("="*50)
        print("  CONVERTIR USUARIO EN ADMINISTRADOR")
        print("="*50)
        print()
        
        # Listar usuarios
        list_users()
        print()
        
        email = input("Email del usuario a hacer admin: ").strip()
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print("[ERROR] Usuario no encontrado")
            return
        
        if user.is_admin:
            print(f"[INFO] El usuario '{user.username}' ya es administrador")
            return
        
        # Confirmar
        print()
        print(f"Usuario: {user.username} ({user.email})")
        confirm = input("¿Convertir en administrador? (SI/no): ").strip()
        
        if confirm.upper() != 'SI':
            print("Operacion cancelada")
            return
        
        # Convertir
        user.is_admin = True
        db.session.commit()
        
        print()
        print("[OK] Usuario convertido en administrador exitosamente")
        print("="*50)


def main():
    """Menu principal."""
    while True:
        print()
        print("="*50)
        print("  GESTION DE USUARIOS")
        print("="*50)
        print()
        print("  1. Listar usuarios")
        print("  2. Eliminar usuario")
        print("  3. Convertir usuario en admin")
        print("  4. Salir")
        print()
        
        opcion = input("Opcion (1-4): ").strip()
        
        if opcion == '1':
            list_users()
        elif opcion == '2':
            delete_user()
        elif opcion == '3':
            make_admin()
        elif opcion == '4':
            print("¡Hasta luego!")
            break
        else:
            print("Opcion no valida")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperacion cancelada por el usuario")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
