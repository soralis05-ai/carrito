"""
Migración: Agrega tablas para portfolio (portfolio_info y portfolio_items).

Ejecutar con:
    python scripts/add_portfolio_tables.py
"""

import sys
import os

# Agregar el directorio padre al path para importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.portfolio_info import PortfolioInfo
from app.models.portfolio_item import PortfolioItem


def migrate():
    """Crear tablas del portfolio."""
    app = create_app()

    with app.app_context():
        try:
            # Crear tablas
            db.create_all()

            # Verificar que las tablas existen
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()

            if 'portfolio_info' in tables and 'portfolio_items' in tables:
                print("✅ Tablas del portfolio creadas exitosamente!")
                print("   - portfolio_info")
                print("   - portfolio_items")

                # Crear registro por defecto si no existe
                existing_info = PortfolioInfo.query.first()
                if not existing_info:
                    default_info = PortfolioInfo(
                        name='Almapunt',
                        title='Artesanía y Productos Únicos',
                        bio='Somos una tienda especializada en productos artesanales y únicos. Cada pieza está seleccionada con cuidado para ofrecer calidad y originalidad a nuestros clientes.',
                        email='soralis05@gmail.com',
                        phone=''
                    )
                    db.session.add(default_info)
                    db.session.commit()
                    print("   - Registro por defecto de portfolio_info creado")

                print("\n✅ Migración completada!")
                return True
            else:
                print("❌ Error: Las tablas no se crearon correctamente")
                print(f"   Tablas existentes: {tables}")
                return False

        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            db.session.rollback()
            return False


if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)
