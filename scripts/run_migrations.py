"""
Migración completa para producción.
Ejecuta todas las migraciones pendientes de base de datos.

Uso: python scripts/run_migrations.py
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from sqlalchemy import text


def check_and_migrate():
    """Verificar y ejecutar migraciones pendientes."""
    app = create_app()
    migrations_applied = []

    with app.app_context():
        print("=" * 60)
        print("MIGRACIÓN DE BASE DE DATOS - PRODUCCIÓN")
        print("=" * 60)

        # 1. Verificar columna costos en products
        print("\n[1/2] Verificando columna 'costos' en products...")
        result = db.session.execute(text("PRAGMA table_info(products)")).fetchall()
        column_names = [row[1] for row in result]

        if 'costos' not in column_names:
            print("   ⚠️  Columna 'costos' no existe. Creando...")
            db.session.execute(text("ALTER TABLE products ADD COLUMN costos JSON"))
            db.session.commit()
            migrations_applied.append("costos column in products")
            print("   ✅ Columna 'costos' creada")
        else:
            print("   ✅ Columna 'costos' ya existe")

        # 2. Verificar tablas de portfolio
        print("\n[2/2] Verificando tablas de portfolio...")
        result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
        table_names = [row[0] for row in result]

        if 'portfolio_info' not in table_names:
            print("   ⚠️  Tabla 'portfolio_info' no existe. Creando...")
            db.session.execute(text("""
                CREATE TABLE portfolio_info (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    title VARCHAR(100),
                    bio TEXT,
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    created_at DATETIME,
                    updated_at DATETIME
                )
            """))
            db.session.commit()
            migrations_applied.append("portfolio_info table")
            print("   ✅ Tabla 'portfolio_info' creada")
        else:
            print("   ✅ Tabla 'portfolio_info' ya existe")

        if 'portfolio_items' not in table_names:
            print("   ⚠️  Tabla 'portfolio_items' no existe. Creando...")
            db.session.execute(text("""
                CREATE TABLE portfolio_items (
                    id INTEGER PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    description VARCHAR(500),
                    image VARCHAR(255) NOT NULL,
                    order INTEGER DEFAULT 999,
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME,
                    updated_at DATETIME
                )
            """))
            db.session.commit()
            migrations_applied.append("portfolio_items table")
            print("   ✅ Tabla 'portfolio_items' creada")
        else:
            print("   ✅ Tabla 'portfolio_items' ya existe")

        # Resumen
        print("\n" + "=" * 60)
        if migrations_applied:
            print("✅ MIGRACIONES APLICADAS:")
            for migration in migrations_applied:
                print(f"   - {migration}")
        else:
            print("✅ NO HAY MIGRACIONES PENDIENTES")
        print("=" * 60)

        return migrations_applied


if __name__ == '__main__':
    try:
        check_and_migrate()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
