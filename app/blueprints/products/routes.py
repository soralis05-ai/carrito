from flask import render_template, abort, current_app
from . import products_bp
from .services import ProductsService

logger = current_app.logger

@products_bp.route('/')
def list():
    products = ProductsService.get_all()
    logger.info(f'Listado de productos: {len(products)} productos')
    return render_template('products/list.html', products=products)

@products_bp.route('/<int:id>')
def detail(id):
    product = ProductsService.get_by_id(id)
    if not product:
        logger.warning(f'Producto no encontrado: ID={id}')
        abort(404)
    logger.info(f'Detalle de producto: {product.get("name")} (ID={id})')
    return render_template('products/detail.html', product=product)
