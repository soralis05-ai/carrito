from typing import Optional
from app.models import CartItem, Product
from app import db


class CartService:
    """Servicio del carrito de compras."""

    @staticmethod
    def get_cart_items(user_id: Optional[int] = None, session_id: Optional[str] = None) -> list[dict]:
        """
        Obtener items del carrito.

        Args:
            user_id: ID del usuario (si está logueado)
            session_id: ID de sesión (para invitados)

        Returns:
            Lista de items del carrito
        """
        query = CartItem.query

        if user_id:
            query = query.filter_by(user_id=user_id)
        elif session_id:
            query = query.filter_by(session_id=session_id)
        else:
            return []

        items = query.all()
        return [CartService._to_dict(item) for item in items]

    @staticmethod
    def add_item(product_id: int, quantity: int = 1, user_id: Optional[int] = None, session_id: Optional[str] = None) -> CartItem:
        """
        Añadir producto al carrito.

        Args:
            product_id: ID del producto
            quantity: Cantidad
            user_id: ID del usuario (opcional)
            session_id: ID de sesión (opcional)

        Returns:
            CartItem creado o actualizado
        """
        # Verificar si ya existe el item
        query = CartItem.query.filter_by(product_id=product_id)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        elif session_id:
            query = query.filter_by(session_id=session_id)
        
        existing_item = query.first()
        
        if existing_item:
            # Actualizar cantidad
            existing_item.quantity += quantity
            existing_item.updated_at = db.func.now()
            db.session.commit()
            return existing_item
        else:
            # Crear nuevo item
            new_item = CartItem(
                product_id=product_id,
                quantity=quantity,
                user_id=user_id,
                session_id=session_id
            )
            db.session.add(new_item)
            db.session.commit()
            return new_item
    
    @staticmethod
    def update_item(item_id: int, quantity: int, user_id: Optional[int] = None) -> bool:
        """
        Actualizar cantidad de un item.

        Args:
            item_id: ID del item
            quantity: Nueva cantidad
            user_id: ID del usuario (para verificar propiedad)

        Returns:
            True si se actualizó, False si no existe
        """
        item = db.session.get(CartItem, item_id)

        if not item:
            return False

        # Verificar que pertenece al usuario
        if user_id and item.user_id != user_id:
            return False

        if quantity <= 0:
            # Eliminar si cantidad es 0
            db.session.delete(item)
        else:
            item.quantity = quantity
            item.updated_at = db.func.now()

        db.session.commit()
        return True

    @staticmethod
    def remove_item(item_id: int, user_id: Optional[int] = None) -> bool:
        """
        Eliminar item del carrito.

        Args:
            item_id: ID del item
            user_id: ID del usuario (para verificar propiedad)

        Returns:
            True si se eliminó, False si no existe
        """
        return CartService.update_item(item_id, 0, user_id)

    @staticmethod
    def clear_cart(user_id: Optional[int] = None, session_id: Optional[str] = None) -> None:
        """
        Vaciar carrito completo.

        Args:
            user_id: ID del usuario
            session_id: ID de sesión
        """
        query = CartItem.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        elif session_id:
            query = query.filter_by(session_id=session_id)
        
        items = query.all()
        for item in items:
            db.session.delete(item)
        
        db.session.commit()
    
    @staticmethod
    def calculate_total(user_id: Optional[int] = None, session_id: Optional[str] = None) -> float:
        """
        Calcular total del carrito.

        Args:
            user_id: ID del usuario
            session_id: ID de sesión

        Returns:
            Total numérico
        """
        items = CartService.get_cart_items(user_id, session_id)
        total = sum(float(item['subtotal']) for item in items)
        return round(total, 2)

    @staticmethod
    def count_items(user_id: Optional[int] = None, session_id: Optional[str] = None) -> int:
        """
        Contar items en el carrito.

        Args:
            user_id: ID del usuario
            session_id: ID de sesión

        Returns:
            Cantidad total de items
        """
        items = CartService.get_cart_items(user_id, session_id)
        return sum(item['quantity'] for item in items)

    @staticmethod
    def _to_dict(cart_item: CartItem) -> dict:
        """Convertir CartItem a diccionario."""
        return {
            'id': cart_item.id,
            'product_id': cart_item.product.id,
            'product_name': cart_item.product.name,
            'product_image': cart_item.product.get_main_image(),
            'product_price': str(cart_item.product.price),
            'quantity': cart_item.quantity,
            'subtotal': str(cart_item.subtotal),
        }
