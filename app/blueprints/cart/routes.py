from flask import render_template, jsonify, request
from . import cart_bp
from .services import CartService

@cart_bp.route('/', methods=['GET'])
def view_cart():
    cart_items = CartService.get_cart_items()
    total = CartService.calculate_total()
    return render_template('cart/view.html', items=cart_items, total=total)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)
    CartService.add_item(product_id, quantity)
    return jsonify({'success': True})

@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    CartService.remove_item(item_id)
    return jsonify({'success': True})