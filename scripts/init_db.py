"""
Script para inicializar la base de datos con datos de ejemplo.
Ejecutar: python scripts/init_db.py
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Product, Category, CartItem, Order, OrderItem
from datetime import datetime
import json

def init_db():
    """Inicializar base de datos con datos de ejemplo."""
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas
        print("Creando tablas en la base de datos...")
        db.create_all()
        print("[OK] Tablas creadas exitosamente")
        
        # Verificar si ya hay datos
        if Category.query.first():
            print("\n[AVISO] La base de datos ya tiene datos. Deseas borrarlos y comenzar de nuevo?")
            response = input("Escribe 'SI' para confirmar: ")
            if response != 'SI':
                print("Operacion cancelada.")
                return
            
            # Borrar todos los datos
            print("\nEliminando datos existentes...")
            db.drop_all()
            db.create_all()
            print("[OK] Base de datos limpiada")
        
        # Crear categorías
        print("\nCreando categorias...")
        categorias = [
            {'name': 'Peluches', 'slug': 'peluches', 'description': 'Peluches artesanales unicos'},
            {'name': 'Accesorios', 'slug': 'accesorios', 'description': 'Accesorios y complementos'},
            {'name': 'Hogar', 'slug': 'hogar', 'description': 'Articulos para el hogar'},
            {'name': 'Papeleria', 'slug': 'papeleria', 'description': 'Articulos de papeleria creativa'},
        ]
        
        for cat in categorias:
            category = Category(**cat)
            db.session.add(category)
            print(f"  [OK] Categoria: {category.name}")
        
        db.session.commit()
        
        # Crear productos de ejemplo
        print("\nCreando productos de ejemplo...")
        productos = [
            {
                'name': 'Conejito 1',
                'slug': 'conejito-1',
                'description': 'Adorable conejito de peluche suave y acogedor. Perfecto para regalar o decorar tu habitacion.',
                'price': 19.99,
                'stock': 10,
                'sku': 'CON-001',
                'image_main': 'conejito1.jpg',
                'images': ['conejito1.jpg'],
                'category_id': 1,
                'is_featured': True
            },
            {
                'name': 'Conejito 2',
                'slug': 'conejito-2',
                'description': 'Conejito esponjoso con detalles unicos. Ideal para ninos y amantes de los animales.',
                'price': 19.99,
                'stock': 8,
                'sku': 'CON-002',
                'image_main': 'conejito2.jpg',
                'images': ['conejito2.jpg'],
                'category_id': 1,
                'is_featured': False
            },
            {
                'name': 'Dino 1',
                'slug': 'dino-1',
                'description': 'Divertido dinosaurio de peluche. Ideal para ninos curiosos y fans de los dinosaurios.',
                'price': 22.99,
                'stock': 5,
                'sku': 'DIN-001',
                'image_main': 'dino1.jpg',
                'images': ['dino1.jpg'],
                'category_id': 1,
                'is_featured': True
            },
            {
                'name': 'Monedero 1',
                'slug': 'monedero-1',
                'description': 'Monedero compacto y elegante. Ideal para llevar tus monedas y pequenas pertenencias.',
                'price': 12.99,
                'stock': 15,
                'sku': 'MON-001',
                'image_main': 'monedero1.jpg',
                'images': ['monedero1.jpg'],
                'category_id': 2,
                'is_featured': False
            },
            {
                'name': 'Posavasos 1',
                'slug': 'posavasos-1',
                'description': 'Posavasos decorativo que protege tus muebles. Diseno elegante y facil de limpiar.',
                'price': 8.99,
                'stock': 20,
                'sku': 'POS-001',
                'image_main': 'posavasos1.jpg',
                'images': ['posavasos1.jpg'],
                'category_id': 3,
                'is_featured': False
            },
            {
                'name': 'Forro Cuaderno 1',
                'slug': 'forro-cuaderno-1',
                'description': 'Forro protector para cuadernos con diseno atractivo. Mantiene tus apuntes seguros y con estilo.',
                'price': 9.99,
                'stock': 25,
                'sku': 'FOR-001',
                'image_main': 'forrocuaderno1.jpg',
                'images': ['forrocuaderno1.jpg'],
                'category_id': 4,
                'is_featured': False
            },
        ]
        
        for prod in productos:
            product = Product(**prod)
            db.session.add(product)
            print(f"  [OK] Producto: {product.name} - EUR {product.price}")
        
        db.session.commit()
        
        # Crear usuario admin de ejemplo
        print("\nCreando usuario admin de ejemplo...")
        admin = User(
            username='admin',
            email='admin@almapunt.es',
            password_hash='pbkdf2:sha256:260000$tempsalt$hashplaceholder',
            first_name='Admin',
            last_name='Almapunt',
            is_admin=True
        )
        db.session.add(admin)
        print("  [OK] Usuario admin creado (username: admin, email: admin@almapunt.es)")
        
        db.session.commit()
        
        # Resumen
        print("\n" + "="*50)
        print("[EXITO] BASE DE DATOS INICIALIZADA EXITOSAMENTE")
        print("="*50)
        print(f"  Categorias: {Category.query.count()}")
        print(f"  Productos: {Product.query.count()}")
        print(f"  Usuarios: {User.query.count()}")
        print("="*50)
        print("\nArchivo DB: app.db (en la raiz del proyecto)")
        print("\nPara usar en produccion (Hetzner):")
        print("  1. Copiar app.db al servidor")
        print("  2. O ejecutar este script en el servidor")
        print("="*50)


if __name__ == '__main__':
    try:
        init_db()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
