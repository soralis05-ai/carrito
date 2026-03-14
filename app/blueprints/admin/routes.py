import os
import uuid
from flask import render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required
from werkzeug.utils import secure_filename
from . import admin_bp
from .forms import ProductUploadForm, ProductEditForm
from app.utils.decorators import admin_required
from app.utils.image_processor import process_image, validate_image
from app import db
from app.models import Product, Category


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Panel principal de administración."""
    # Contar productos, categorías
    product_count = Product.query.count()
    category_count = Category.query.count()

    return render_template('admin/dashboard.html',
                         product_count=product_count,
                         category_count=category_count)


@admin_bp.route('/tax-calculator')
@login_required
@admin_required
def tax_calculator():
    """Calculadora de impuestos para autónomos."""
    return render_template('admin/tax_calculator.html')


def _process_uploaded_images(form, existing_images=None):
    """Procesar imágenes subidas y retornar lista de nombres."""
    image_filenames = list(existing_images) if existing_images else []
    
    image_fields = ['image', 'image2', 'image3', 'image4', 'image5']
    upload_folder = os.path.join(current_app.root_path, 'static', 'img', 'productos')
    os.makedirs(upload_folder, exist_ok=True)
    
    for field_name in image_fields:
        image_file = getattr(form, field_name).data
        if image_file:
            if not validate_image(image_file.filename):
                flash(f'Formato no soportado: {image_file.filename}', 'danger')
                continue
            
            original_filename = secure_filename(image_file.filename)
            extension = os.path.splitext(original_filename)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}"
            
            temp_path = os.path.join(upload_folder, f"{unique_filename}_temp{extension}")
            image_file.save(temp_path)
            
            output_base = os.path.join(upload_folder, unique_filename)
            result = process_image(
                temp_path,
                output_base,
                max_size=(800, 800),
                output_format='WEBP',
                quality=85
            )
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            if result['success']:
                image_filenames.append(os.path.basename(result['path']))
            else:
                flash(f'Error procesando imagen: {result["error"]}', 'danger')
    
    return image_filenames


@admin_bp.route('/products/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_product():
    """Subir nuevo producto con imagenes."""
    form = ProductUploadForm()
    
    # Cargar categorías para el select
    categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
    form.category_id.choices = [(0, '-- Sin categoría --')] + [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        # Procesar imágenes
        image_filenames = _process_uploaded_images(form)
        
        if not image_filenames:
            flash('Error: No se pudieron procesar las imágenes', 'danger')
            return render_template('admin/upload_product.html', form=form)
        
        # Generar SKU automático si no se proporciona
        sku = form.sku.data
        if not sku:
            sku = f"PRD-{uuid.uuid4().hex[:8].upper()}"
        
        # Generar slug automático desde el nombre
        slug = form.name.data.lower().replace(' ', '-').replace('_', '-')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        # Crear producto
        product = Product(
            name=form.name.data,
            slug=slug,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            sku=sku,
            category_id=form.category_id.data if form.category_id.data > 0 else None,
            is_featured=form.is_featured.data,
            is_active=form.is_active.data,
            image_main=image_filenames[0],
            images=image_filenames if len(image_filenames) > 1 else None
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash(f'Producto "{form.name.data}" guardado exitosamente con {len(image_filenames)} imagen(es)!', 'success')
        return redirect(url_for('admin.list_products'))
    
    return render_template('admin/upload_product.html', form=form)


@admin_bp.route('/products')
@login_required
@admin_required
def list_products():
    """Listar productos para administración."""
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/list_products.html', products=products)


@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    """Editar producto existente."""
    product = Product.query.get_or_404(product_id)
    form = ProductEditForm()

    # Cargar categorías
    categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
    form.category_id.choices = [(0, '-- Sin categoría --')] + [(c.id, c.name) for c in categories]

    if request.method == 'GET':
        # Precargar datos básicos del producto en el formulario
        form.name.data = product.name
        form.description.data = product.description
        form.price.data = float(product.price) if product.price else 0
        form.stock.data = product.stock or 0
        form.sku.data = product.sku or ''
        form.category_id.data = product.category_id or 0
        form.is_featured.data = product.is_featured or False
        form.is_active.data = product.is_active or True

        # Precargar costos si existen
        if product.costos:
            costos = product.costos
            # Lana
            form.lana_costo_rollo.data = float(costos.get('lana_costo_rollo') or 0)
            form.lana_peso_rollo.data = float(costos.get('lana_peso_rollo') or 0)
            form.lana_peso_usado.data = float(costos.get('lana_peso_usado') or 0)
            # Relleno
            form.relleno_costo_bolsa.data = float(costos.get('relleno_costo_bolsa') or 0)
            form.relleno_peso_bolsa.data = float(costos.get('relleno_peso_bolsa') or 0)
            form.relleno_peso_usado.data = float(costos.get('relleno_peso_usado') or 0)
            # Ojos
            form.ojos_usar.data = bool(costos.get('ojos_usar'))
            form.ojos_costo_unitario.data = float(costos.get('ojos_costo_unitario') or 0)
            form.ojos_cantidad.data = float(costos.get('ojos_cantidad') or 0)
            # Mano de obra
            form.mano_obra_usar.data = bool(costos.get('mano_obra_usar'))
            form.mano_obra_costo_hora.data = float(costos.get('mano_obra_costo_hora') or 0)
            form.mano_obra_horas.data = float(costos.get('mano_obra_horas') or 0)
            # Utilidad
            form.utilidad_usar.data = bool(costos.get('utilidad_usar'))
            form.utilidad_porcentaje.data = float(costos.get('utilidad_porcentaje') or 0)

    if form.validate_on_submit():
        # Validar que el precio no sea 0 o inválido
        if not form.price.data or float(form.price.data) <= 0:
            flash('Error: El precio de venta no puede ser 0. Complete los campos de costos para calcular el precio.', 'danger')
            return render_template('admin/edit_product.html', form=form, product=product)

        # Validar que al menos algunos costos estén completos si es amigurumi
        costos_data = {
            'lana_costo_rollo': form.lana_costo_rollo.data or 0,
            'lana_peso_rollo': form.lana_peso_rollo.data or 0,
            'lana_peso_usado': form.lana_peso_usado.data or 0,
            'relleno_costo_bolsa': form.relleno_costo_bolsa.data or 0,
            'relleno_peso_bolsa': form.relleno_peso_bolsa.data or 0,
            'relleno_peso_usado': form.relleno_peso_usado.data or 0,
            'ojos_usar': form.ojos_usar.data or False,
            'ojos_costo_unitario': form.ojos_costo_unitario.data or 0,
            'ojos_cantidad': form.ojos_cantidad.data or 0,
            'mano_obra_usar': form.mano_obra_usar.data or False,
            'mano_obra_costo_hora': form.mano_obra_costo_hora.data or 0,
            'mano_obra_horas': form.mano_obra_horas.data or 0,
            'utilidad_usar': form.utilidad_usar.data or False,
            'utilidad_porcentaje': form.utilidad_porcentaje.data or 0
        }

        # Verificar si hay costos de materiales (lana o relleno)
        tiene_materiales = (
            costos_data['lana_costo_rollo'] > 0 or
            costos_data['relleno_costo_bolsa'] > 0
        )

        if not tiene_materiales and float(form.price.data) <= 0:
            flash('Error: Debe ingresar al menos los costos de materiales (lana/relleno) o establecer un precio manualmente.', 'danger')
            return render_template('admin/edit_product.html', form=form, product=product)

        # Generar slug automático desde el nombre
        slug = form.name.data.lower().replace(' ', '-').replace('_', '-')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        # Guardar costos en JSON
        costos_data = {
            'lana_costo_rollo': form.lana_costo_rollo.data or 0,
            'lana_peso_rollo': form.lana_peso_rollo.data or 0,
            'lana_peso_usado': form.lana_peso_usado.data or 0,
            'relleno_costo_bolsa': form.relleno_costo_bolsa.data or 0,
            'relleno_peso_bolsa': form.relleno_peso_bolsa.data or 0,
            'relleno_peso_usado': form.relleno_peso_usado.data or 0,
            'ojos_usar': form.ojos_usar.data or False,
            'ojos_costo_unitario': form.ojos_costo_unitario.data or 0,
            'ojos_cantidad': form.ojos_cantidad.data or 0,
            'mano_obra_usar': form.mano_obra_usar.data or False,
            'mano_obra_costo_hora': form.mano_obra_costo_hora.data or 0,
            'mano_obra_horas': form.mano_obra_horas.data or 0,
            'utilidad_usar': form.utilidad_usar.data or False,
            'utilidad_porcentaje': form.utilidad_porcentaje.data or 0
        }

        # Actualizar datos básicos
        product.name = form.name.data
        product.slug = slug
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.sku = form.sku.data or product.sku
        product.category_id = form.category_id.data if form.category_id.data > 0 else None
        product.is_featured = form.is_featured.data
        product.is_active = form.is_active.data
        product.costos = costos_data

        # Verificar si se subieron nuevas imágenes
        images_uploaded = any([
            form.image.data, form.image2.data, form.image3.data,
            form.image4.data, form.image5.data
        ])

        if images_uploaded:
            # Procesar nuevas imágenes
            existing_images = product.get_all_images()
            image_filenames = _process_uploaded_images(form, existing_images)

            if image_filenames:
                product.image_main = image_filenames[0]
                product.images = image_filenames[1:] if len(image_filenames) > 1 else None
        # Si no se subieron imágenes, mantener las existentes (no hacer nada)

        db.session.commit()

        flash(f'Producto "{product.name}" actualizado exitosamente!', 'success')
        return redirect(url_for('admin.list_products'))

    return render_template('admin/edit_product.html', form=form, product=product)


@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    """Eliminar producto."""
    product = Product.query.get_or_404(product_id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        flash(f'Producto "{product.name}" eliminado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    
    return redirect(url_for('admin.list_products'))


# ============================================
# GESTIÓN DE CATEGORÍAS
# ============================================

@admin_bp.route('/categories')
@login_required
@admin_required
def list_categories():
    """Listar todas las categorías."""
    categories = Category.query.order_by(Category.id.asc()).all()
    return render_template('admin/list_categories.html', categories=categories)


@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_category():
    """Crear nueva categoría."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        slug = request.form.get('slug', '').strip()
        description = request.form.get('description', '').strip()
        is_active = request.form.get('is_active', False)
        
        # Validaciones
        if not name:
            flash('El nombre de la categoría es requerido', 'danger')
            return redirect(url_for('admin.create_category'))
        
        # Generar slug si no se proporciona
        if not slug:
            slug = name.lower().replace(' ', '-').replace('_', '-')
        
        # Verificar si ya existe
        if Category.query.filter_by(slug=slug).first():
            flash(f'La categoría con slug "{slug}" ya existe', 'danger')
            return redirect(url_for('admin.create_category'))
        
        # Crear categoría
        category = Category(
            name=name,
            slug=slug,
            description=description if description else None,
            is_active=is_active == 'on'
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash(f'Categoría "{name}" creada exitosamente!', 'success')
        return redirect(url_for('admin.list_categories'))
    
    return render_template('admin/create_category.html')


@admin_bp.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    """Editar categoría existente."""
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        slug = request.form.get('slug', '').strip()
        description = request.form.get('description', '').strip()
        is_active = request.form.get('is_active', False)
        
        # Validaciones
        if not name:
            flash('El nombre de la categoría es requerido', 'danger')
            return redirect(url_for('admin.edit_category', category_id=category_id))
        
        # Generar slug si no se proporciona
        if not slug:
            slug = name.lower().replace(' ', '-').replace('_', '-')
        
        # Verificar si el slug ya existe en otra categoría
        existing = Category.query.filter_by(slug=slug).first()
        if existing and existing.id != category_id:
            flash(f'La categoría con slug "{slug}" ya existe', 'danger')
            return redirect(url_for('admin.edit_category', category_id=category_id))
        
        # Actualizar
        category.name = name
        category.slug = slug
        category.description = description if description else None
        category.is_active = is_active == 'on'
        
        db.session.commit()
        
        flash(f'Categoría "{name}" actualizada exitosamente!', 'success')
        return redirect(url_for('admin.list_categories'))
    
    return render_template('admin/edit_category.html', category=category)


@admin_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    """Eliminar categoría."""
    category = Category.query.get_or_404(category_id)
    
    # Verificar si tiene productos asociados
    product_count = category.products.count()
    if product_count > 0:
        flash(f'No se puede eliminar: hay {product_count} producto(s) en esta categoría', 'danger')
        return redirect(url_for('admin.list_categories'))
    
    try:
        db.session.delete(category)
        db.session.commit()
        flash(f'Categoría "{category.name}" eliminada exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    
    return redirect(url_for('admin.list_categories'))
