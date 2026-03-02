from flask import render_template, abort
from . import products_bp
from .services import ProductsService

@products_bp.route('/')
def list():
    products = ProductsService.get_all()
    return render_template('products/list.html', products=products)

@products_bp.route('/<int:id>')
def detail(id):
    product = ProductsService.get_by_id(id)
    if not product:
        abort(404)
    return render_template('products/detail.html', product=product)
