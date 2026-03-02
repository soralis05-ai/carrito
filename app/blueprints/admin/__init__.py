from flask import Blueprint

# blueprint for administration
admin_bp = Blueprint('admin', __name__, template_folder='templates')

from . import routes  # noqa: F401
