from flask import Blueprint

# blueprint for orders workflow
orders_bp = Blueprint('orders', __name__, template_folder='templates')

from . import routes  # noqa: F401
