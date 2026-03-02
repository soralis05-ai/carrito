from flask import Blueprint

# Blueprint para portfolio personal
portfolio_bp = Blueprint('portfolio', __name__, template_folder='templates')

from . import routes  # noqa: F401
