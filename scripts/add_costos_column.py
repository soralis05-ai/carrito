"""
Script para agregar columna 'costos' a la tabla products.
Ejecutar: python scripts/add_costos_column.py
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from sqlalchemy import text

def add_costos_column():
    """Agregar columna costos a la tabla products."""
    app = create_app()

    with app.app_context():
        # Verificar si la columna ya existe
        result = db.session.execute(text(
            "PRAGMA table_info(products)"
        )).fetchall()
        
        column_names = [row[1] for row in result]
        
        if 'costos' in column_names:
            print("[INFO] La columna 'costos' ya existe en la tabla products")
            return
        
        print("Agregando columna 'costos' a la tabla products...")
        
        # Agregar la columna
        db.session.execute(text(
            "ALTER TABLE products ADD COLUMN costos JSON"
        ))
        
        db.session.commit()
        
        print("[OK] Columna 'costos' agregada exitosamente")
        print("="*60)


if __name__ == '__main__':
    try:
        add_costos_column()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
