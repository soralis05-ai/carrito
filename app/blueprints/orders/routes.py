from flask import render_template
from . import orders_bp

@orders_bp.route('/checkout')
def checkout():
    return 'checkout placeholder'

@orders_bp.route('/confirmation')
def confirmation():
    return 'confirmation placeholder'
