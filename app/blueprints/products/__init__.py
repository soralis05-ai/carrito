from flask import Blueprint

# blueprint for product catalog
products_bp = Blueprint('products', __name__, template_folder='templates')

from . import routes  # noqa: F401
