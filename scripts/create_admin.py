"""
Script para crear usuario administrador.
Ejecutar: python scripts/create_admin.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin():
    """Crear o actualizar usuario administrador."""
    app = create_app()

    with app.app_context():
        # Verificar si ya existe usuario con este email
        admin = User.query.filter_by(email='soralis05@gmail.com').first()
        
        if admin:
            # Actualizar credenciales
            admin.username = 'SorayaR'
            admin.password_hash = generate_password_hash('Soraya79@')
            admin.first_name = 'Soraya'
            admin.last_name = 'R'
            admin.is_admin = True
            
            db.session.commit()
            
            print("✅ Usuario administrador actualizado exitosamente!")
        else:
            # Crear admin nuevo
            admin = User(
                username='SorayaR',
                email='soralis05@gmail.com',
                password_hash=generate_password_hash('Soraya79@'),
                first_name='Soraya',
                last_name='R',
                is_admin=True
            )

            db.session.add(admin)
            db.session.commit()
            
            print("✅ Usuario administrador creado exitosamente!")
        
        print("\n📋 Credenciales:")
        print("   Email: soralis05@gmail.com")
        print("   Username: SorayaR")
        print("   Password: Soraya79@")
        print("\n✅ ¡Listo para usar!")

        return True

if __name__ == '__main__':
    success = create_admin()
    sys.exit(0 if success else 1)
