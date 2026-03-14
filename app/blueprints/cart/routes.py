from flask import render_template, jsonify, request, session
from flask_login import current_user
from . import cart_bp
from .services import CartService
import uuid

def get_or_create_session_id():
    """Obtener o crear ID de sesión para carritos de invitados."""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

@cart_bp.route('/', methods=['GET'])
def view_cart():
    """Ver carrito de compras."""
    user_id = current_user.id if current_user.is_authenticated else None
    session_id = get_or_create_session_id() if not user_id else None
    
    cart_items = CartService.get_cart_items(user_id=user_id, session_id=session_id)
    total = CartService.calculate_total(user_id=user_id, session_id=session_id)
    
    return render_template('cart/view.html', items=cart_items, total=total)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    """Añadir producto al carrito."""
    user_id = current_user.id if current_user.is_authenticated else None
    session_id = get_or_create_session_id() if not user_id else None
    
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({'success': False, 'error': 'Product ID required'}), 400
    
    CartService.add_item(product_id, quantity, user_id=user_id, session_id=session_id)
    
    # Actualizar contador en sesión
    session['cart_count'] = CartService.count_items(user_id=user_id, session_id=session_id)
    
    return jsonify({'success': True, 'cart_count': session['cart_count']})

@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    """Eliminar item del carrito."""
    user_id = current_user.id if current_user.is_authenticated else None
    
    CartService.remove_item(item_id, user_id=user_id)
    
    # Actualizar contador en sesión
    session_id = get_or_create_session_id() if not user_id else None
    session['cart_count'] = CartService.count_items(user_id=user_id, session_id=session_id)
    
    return jsonify({'success': True, 'cart_count': session['cart_count']})

@cart_bp.route('/count')
def get_cart_count():
    """Obtener cantidad de items en el carrito."""
    user_id = current_user.id if current_user.is_authenticated else None
    session_id = get_or_create_session_id() if not user_id else None
    
    count = CartService.count_items(user_id=user_id, session_id=session_id)
    session['cart_count'] = count
    
    return jsonify({'count': count})