from flask import Blueprint

# blueprint for shopping cart
cart_bp = Blueprint('cart', __name__, template_folder='templates')

from .routes import *