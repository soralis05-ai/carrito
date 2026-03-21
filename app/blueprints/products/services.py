from app.models import Product


class ProductsService:
    """Servicio de productos usando base de datos."""
    
    @staticmethod
    def get_all(limit=None, category_id=None, featured_only=False):
        """
        Obtener todos los productos.
        
        Args:
            limit: Límite de resultados (None para todos)
            category_id: Filtrar por categoría
            featured_only: Solo productos destacados
        
        Returns:
            Lista de productos (dict format para compatibilidad)
        """
        query = Product.query.filter_by(is_active=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if featured_only:
            query = query.filter_by(is_featured=True)
        
        query = query.order_by(Product.name)
        
        if limit:
            query = query.limit(limit)
        
        products = query.all()
        return [ProductsService._to_dict(p) for p in products]
    
    @staticmethod
    def get_by_id(product_id):
        """Obtener producto por ID (solo activos)."""
        product = Product.query.filter_by(id=product_id, is_active=True).first()
        if product:
            return ProductsService._to_dict(product)
        return None
    
    @staticmethod
    def get_by_slug(slug):
        """Obtener producto por slug (solo activos)."""
        product = Product.query.filter_by(slug=slug, is_active=True).first()
        if product:
            return ProductsService._to_dict(product)
        return None
    
    @staticmethod
    def search(query_text):
        """Buscar productos por nombre o descripción."""
        products = Product.query.filter(
            Product.is_active == True,
            Product.name.ilike(f'%{query_text}%')
        ).all()
        return [ProductsService._to_dict(p) for p in products]
    
    @staticmethod
    def _to_dict(product):
        """Convertir modelo Product a diccionario (para compatibilidad con templates)."""
        return {
            'id': product.id,
            'name': product.name,
            'slug': product.slug,
            'description': product.description,
            'price': f"{product.price}€",
            'price_numeric': float(product.price),
            'image': product.get_main_image() or 'placeholder.jpg',
            'images': product.get_all_images() or [product.get_main_image()],
            'stock': product.stock,
            'is_in_stock': product.is_in_stock,
            'is_featured': product.is_featured,
            'category_id': product.category_id,
            'category': product.category.name if product.category else None,
            'sku': product.sku,
        }
    
    @staticmethod
    def get_featured(limit=4):
        """Obtener productos destacados."""
        return ProductsService.get_all(limit=limit, featured_only=True)
    
    @staticmethod
    def get_related(product_id, limit=4):
        """Obtener productos relacionados (misma categoría, solo activos)."""
        product = Product.query.filter_by(id=product_id, is_active=True).first()
        if not product or not product.category_id:
            return []

        related = Product.query.filter(
            Product.is_active == True,
            Product.category_id == product.category_id,
            Product.id != product_id
        ).limit(limit).all()

        return [ProductsService._to_dict(p) for p in related]
