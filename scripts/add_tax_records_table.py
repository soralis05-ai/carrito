"""
Migración: Crea tabla product_tax_records para registros de costos e impuestos.

Ejecutar con:
    python scripts/add_tax_records_table.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.product_tax_record import ProductTaxRecord

def migrate():
    """Crear tabla de registros de impuestos."""
    app = create_app()

    with app.app_context():
        try:
            # Crear tablas
            db.create_all()

            # Verificar que la tabla existe
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()

            if 'product_tax_records' in tables:
                print("✅ Tabla product_tax_records creada exitosamente!")
                print("\nColumnas:")
                columns = inspector.get_columns('product_tax_records')
                for col in columns:
                    print(f"   - {col['name']} ({col['type']})")
                print("\n✅ Migración completada!")
                return True
            else:
                print("❌ Error: La tabla no se creó correctamente")
                print(f"   Tablas existentes: {tables}")
                return False

        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False


if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)
