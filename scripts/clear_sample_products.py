"""
Script para limpiar productos de ejemplo.
Ejecutar: python scripts/clear_sample_products.py
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Product

def clear_products():
    """Eliminar todos los productos."""
    app = create_app()

    with app.app_context():
        products = Product.query.all()
        
        if not products:
            print("No hay productos para eliminar")
            return
        
        print("="*60)
        print(f"  PRODUCTOS A ELIMINAR ({len(products)})")
        print("="*60)
        
        for p in products:
            print(f"  [{p.id}] {p.name} - {p.price}€")
        
        print("="*60)
        print()
        
        confirm = input("¿Estás seguro de eliminar TODOS los productos? (SI/no): ").strip()
        
        if confirm.upper() != 'SI':
            print("Operación cancelada")
            return
        
        for p in products:
            db.session.delete(p)
        
        db.session.commit()
        
        print()
        print("[OK] Todos los productos fueron eliminados")
        print("="*60)


if __name__ == '__main__':
    try:
        clear_products()
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
