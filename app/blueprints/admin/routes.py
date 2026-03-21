import os
import uuid
from flask import render_template, redirect, url_for, flash, current_app, request, session
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


@admin_bp.route('/tax-calculator', methods=['GET', 'POST'])
@login_required
@admin_required
def tax_calculator():
    """Calculadora de impuestos para autónomos."""
    from app.models import ProductTaxRecord, Category
    
    # Obtener categorías para el dropdown
    categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
    
    if request.method == 'POST':
        # Guardar registro
        product_name = request.form.get('product_name', '')
        category = request.form.get('category', '')
        material_cost = float(request.form.get('material_cost', 0) or 0)
        material_iva_percent = int(request.form.get('material_iva_percent', 21) or 21)
        labor_cost = float(request.form.get('labor_cost', 0) or 0)
        profit_percent = int(request.form.get('profit_percent', 20) or 20)
        irpf_percent = int(request.form.get('irpf_percent', 15) or 15)
        autonomo_fee = float(request.form.get('autonomo_fee', 80) or 80)
        monthly_units = int(request.form.get('monthly_units', 10) or 10)
        
        # Calcular valores
        material_base = material_cost / (1 + material_iva_percent / 100)
        material_iva = material_cost - material_base
        cost_total = material_base + labor_cost
        profit_amount = cost_total * (profit_percent / 100)
        base_price = cost_total + profit_amount
        iva_repercutido = base_price * 0.21
        iva_ingresar = iva_repercutido - material_iva
        irpf_amount = profit_amount * (irpf_percent / 100)
        sale_price = base_price + iva_repercutido
        net_profit = profit_amount - irpf_amount
        
        # Crear registro
        record = ProductTaxRecord(
            product_name=product_name,
            category=category,
            material_cost=material_cost,
            material_iva_percent=material_iva_percent,
            labor_cost=labor_cost,
            profit_percent=profit_percent,
            profit_amount=profit_amount,
            material_base=material_base,
            material_iva=material_iva,
            cost_total=cost_total,
            base_price=base_price,
            iva_repercutido=iva_repercutido,
            iva_soportado=material_iva,
            iva_ingresar=iva_ingresar,
            irpf_percent=irpf_percent,
            irpf_amount=irpf_amount,
            sale_price=sale_price,
            net_profit=net_profit,
            autonomo_fee=autonomo_fee,
            monthly_units=monthly_units
        )
        
        db.session.add(record)
        db.session.commit()
        
        flash(f'Registro guardado exitosamente: {product_name}', 'success')
        return redirect(url_for('admin.tax_records'))
    
    return render_template('admin/tax_calculator.html', categories=categories)


@admin_bp.route('/tax-records')
@login_required
@admin_required
def tax_records():
    """Listar registros de costos e impuestos."""
    from app.models import ProductTaxRecord
    
    # Obtener categoría desde query params
    category_filter = request.args.get('category', '')
    
    if category_filter:
        records = ProductTaxRecord.query.filter_by(
            category=category_filter, is_active=True
        ).order_by(ProductTaxRecord.created_at.desc()).all()
    else:
        records = ProductTaxRecord.query.filter_by(
            is_active=True
        ).order_by(ProductTaxRecord.created_at.desc()).all()
    
    # Obtener categorías únicas
    categories = db.session.query(
        ProductTaxRecord.category
    ).filter(
        ProductTaxRecord.is_active == True,
        ProductTaxRecord.category != None,
        ProductTaxRecord.category != ''
    ).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('admin/tax_records.html', 
                         records=records, 
                         categories=categories,
                         current_category=category_filter)


@admin_bp.route('/tax-records/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tax_record(record_id):
    """Editar registro de costos e impuestos."""
    from app.models import ProductTaxRecord
    
    record = ProductTaxRecord.query.get_or_404(record_id)
    
    if request.method == 'POST':
        # Actualizar datos
        record.product_name = request.form.get('product_name', '')
        record.category = request.form.get('category', '')
        record.material_cost = float(request.form.get('material_cost', 0) or 0)
        record.material_iva_percent = int(request.form.get('material_iva_percent', 21) or 21)
        record.labor_cost = float(request.form.get('labor_cost', 0) or 0)
        record.profit_percent = int(request.form.get('profit_percent', 20) or 20)
        record.irpf_percent = int(request.form.get('irpf_percent', 15) or 15)
        record.autonomo_fee = float(request.form.get('autonomo_fee', 80) or 80)
        record.monthly_units = int(request.form.get('monthly_units', 10) or 10)
        
        # Recalcular valores
        record.material_base = record.material_cost / (1 + record.material_iva_percent / 100)
        record.material_iva = record.material_cost - record.material_base
        record.cost_total = record.material_base + record.labor_cost
        record.profit_amount = record.cost_total * (record.profit_percent / 100)
        record.base_price = record.cost_total + record.profit_amount
        record.iva_repercutido = record.base_price * 0.21
        record.iva_ingresar = record.iva_repercutido - record.material_iva
        record.irpf_amount = record.profit_amount * (record.irpf_percent / 100)
        record.sale_price = record.base_price + record.iva_repercutido
        record.net_profit = record.profit_amount - record.irpf_amount
        
        db.session.commit()
        flash('Registro actualizado exitosamente', 'success')
        return redirect(url_for('admin.tax_records'))
    
    return render_template('admin/edit_tax_record.html', record=record)


@admin_bp.route('/tax-records/delete/<int:record_id>', methods=['POST'])
@login_required
@admin_required
def delete_tax_record(record_id):
    """Eliminar registro de costos (soft delete)."""
    from app.models import ProductTaxRecord
    
    record = ProductTaxRecord.query.get_or_404(record_id)
    record.is_active = False
    db.session.commit()
    
    flash('Registro eliminado exitosamente', 'info')
    return redirect(url_for('admin.tax_records'))


def _process_uploaded_images(form, existing_images=None):
    """Procesar imágenes subidas y retornar lista de nombres."""
    from app.utils.image_processor import validate_file_size
    
    image_filenames = list(existing_images) if existing_images else []

    image_fields = ['image', 'image2', 'image3', 'image4', 'image5']
    upload_folder = os.path.join(current_app.root_path, 'static', 'img', 'productos')
    os.makedirs(upload_folder, exist_ok=True)

    for field_name in image_fields:
        image_file = getattr(form, field_name).data
        if image_file:
            # Validar formato
            if not validate_image(image_file.filename):
                flash(f'Formato no soportado: {image_file.filename}', 'danger')
                continue
            
            # Validar tamaño
            is_valid_size, error_msg, size_mb = validate_file_size(image_file, max_size_mb=5)
            if not is_valid_size:
                flash(error_msg, 'danger')
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
    from app.models import MaterialType
    
    form = ProductUploadForm()

    # Cargar categorías para el select
    categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
    form.category_id.choices = [(0, '-- Sin categoría --')] + [(c.id, c.name) for c in categories]
    
    # Cargar tipos de materiales para el datalist
    material_types = MaterialType.query.filter_by(is_active=True).order_by(MaterialType.name).all()

    # Obtener imágenes ya guardadas en sesión
    uploaded_images = session.get('temp_images', [])

    # DEBUG: Obtener tipo de material
    tipo_material = request.form.get('tipoLana', '').strip()
    current_app.logger.info(f'🧶 UPLOAD - Tipo material: "{tipo_material}"')

    # Procesar imágenes nuevas SIEMPRE (antes de validar)
    new_images = _process_uploaded_images(form, existing_images=uploaded_images)

    # Actualizar sesión con todas las imágenes
    if new_images:
        session['temp_images'] = new_images
        uploaded_images = new_images

    if form.validate_on_submit():
        # Todas las imágenes ya están en uploaded_images
        all_images = uploaded_images

        if not all_images:
            flash('Error: Debes subir al menos una imagen', 'danger')
            return render_template('admin/upload_product.html', form=form, categories=categories, uploaded_images=uploaded_images, material_types=material_types)

        # Generar SKU automático si no se proporciona
        sku = form.sku.data
        if not sku:
            sku = f"PRD-{uuid.uuid4().hex[:8].upper()}"

        # Generar slug automático desde el nombre
        slug = form.name.data.lower().replace(' ', '-').replace('_', '-')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')

        # Buscar o crear categoría por nombre (case-insensitive)
        category = None
        category_name = request.form.get('category_id', '').strip()
        if category_name:
            # Buscar categoría existente (case-insensitive)
            category = Category.query.filter(
                db.func.lower(Category.name) == category_name.lower()
            ).first()
            
            if not category:
                # Crear nueva categoría si no existe
                category = Category(
                    name=category_name,
                    slug=category_name.lower().replace(' ', '-').replace('_', '-'),
                    is_active=True
                )
                db.session.add(category)
                db.session.flush()  # Obtener ID

        # Crear producto
        product = Product(
            name=form.name.data,
            slug=slug,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            sku=sku,
            category_id=category.id if category else None,
            is_featured=form.is_featured.data,
            is_active=form.is_active.data,
            image_main=all_images[0],
            images=all_images if len(all_images) > 1 else None,
            costos={
                'tipo_material': tipo_material,  # Guardar tipo seleccionado
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
        )

        db.session.add(product)
        db.session.commit()

        # Limpiar imágenes temporales
        session.pop('temp_images', None)

        flash(f'Producto "{form.name.data}" guardado exitosamente con {len(all_images)} imagen(es)!', 'success')
        return redirect(url_for('admin.list_products'))

    # Si hay errores de validación, las imágenes YA están guardadas en sesión
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                if field == 'stock':
                    flash(f'Error: El campo Stock es requerido. Por favor ingresa una cantidad.', 'warning')
                elif field == 'name':
                    flash(f'Error: El nombre del producto es requerido.', 'warning')
                elif field == 'price':
                    flash(f'Error: El precio es requerido.', 'warning')
                elif field == 'description':
                    flash(f'Error: La descripción es requerida.', 'warning')
                break

    return render_template('admin/upload_product.html', form=form, categories=categories, uploaded_images=uploaded_images, material_types=material_types)


@admin_bp.route('/products')
@login_required
@admin_required
def list_products():
    """Listar productos para administración."""
    products = Product.query.order_by(Product.id.asc()).all()
    return render_template('admin/list_products.html', products=products)


@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    """Editar producto existente."""
    from app.models import MaterialType
    
    product = Product.query.get_or_404(product_id)
    form = ProductEditForm(obj=product)  # Cargar datos del producto automáticamente

    # Cargar categorías para el datalist
    categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
    
    # Cargar tipos de materiales para el datalist
    material_types = MaterialType.query.filter_by(is_active=True).order_by(MaterialType.name).all()

    if request.method == 'GET':
        # Precargar categoría como nombre (no ID)
        if product.category:
            form.category_id.data = product.category.name
        
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

    # DEBUG: Mostrar datos recibidos
    current_app.logger.info('=' * 60)
    current_app.logger.info(f'DEBUG: Editando producto ID {product_id}')
    current_app.logger.info(f'Datos recibidos (request.form): {request.form.to_dict()}')
    
    # DEBUG específico para campo "tipo"
    tipo_material = request.form.get('tipoLana', '').strip()
    current_app.logger.info(f'🧶 TIPO MATERIAL RECIBIDO: "{tipo_material}"')
    current_app.logger.info(f'🧶 TIPO MATERIAL (repr): {repr(tipo_material)}')
    current_app.logger.info(f'🧶 TIPO MATERIAL (len): {len(tipo_material)}')
    
    # Verificar si el campo viene en request
    current_app.logger.info(f'📋 "tipoLana" en request.form: {"tipoLana" in request.form}')
    current_app.logger.info(f'📋 Claves en request.form: {list(request.form.keys())}')
    
    if form.validate_on_submit():
        current_app.logger.info('✅ Formulario válido')
        
        # DEBUG: Verificar qué datos del formulario se están guardando
        current_app.logger.info(f'Form data - lana_costo_rollo: {form.lana_costo_rollo.data}')
        current_app.logger.info(f'Form data - lana_peso_rollo: {form.lana_peso_rollo.data}')
        current_app.logger.info(f'Form data - lana_peso_usado: {form.lana_peso_usado.data}')
        current_app.logger.info(f'Campo tipoLana (datalist): "{tipo_material}"')
        
        # DEBUG: Verificar costos antes de guardar
        current_app.logger.info('📝 COSTOS ANTES DE GUARDAR:')
        current_app.logger.info(f'  - tipo_material: "{tipo_material}"')
        current_app.logger.info(f'  - lana_costo_rollo: {form.lana_costo_rollo.data}')
        current_app.logger.info(f'  - lana_peso_rollo: {form.lana_peso_rollo.data}')
        current_app.logger.info(f'  - lana_peso_usado: {form.lana_peso_usado.data}')
        
        # Generar slug automático desde el nombre
        slug = form.name.data.lower().replace(' ', '-').replace('_', '-')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')

        # Buscar o crear categoría por nombre (case-insensitive)
        category = None
        category_name = request.form.get('category_id', '').strip()
        current_app.logger.info(f'Categoría recibida: "{category_name}"')
        
        if category_name:
            # Buscar categoría existente (case-insensitive)
            category = Category.query.filter(
                db.func.lower(Category.name) == category_name.lower()
            ).first()
            
            current_app.logger.info(f'Categoría encontrada: {category.name if category else "None"}')

            if not category:
                # Crear nueva categoría si no existe
                category = Category(
                    name=category_name,
                    slug=category_name.lower().replace(' ', '-').replace('_', '-'),
                    is_active=True
                )
                db.session.add(category)
                db.session.flush()  # Obtener ID
                current_app.logger.info(f'✅ Categoría creada: {category.name} (ID: {category.id})')

        # Guardar costos en JSON
        costos_data = {
            'tipo_material': tipo_material,  # Guardar tipo seleccionado del datalist
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
        current_app.logger.info(f'Costos a guardar: {costos_data}')

        # Actualizar datos básicos
        product.name = form.name.data
        product.slug = slug
        product.description = form.description.data
        product.price = form.price.data if form.price.data else product.price
        product.stock = form.stock.data if form.stock.data is not None else product.stock
        product.sku = form.sku.data or product.sku
        # category_id ahora es el nombre, buscar o crear categoría
        product.category_id = category.id if category else None
        product.is_featured = form.is_featured.data
        product.is_active = form.is_active.data
        product.costos = costos_data
        
        # DEBUG: Verificar qué se guardó
        current_app.logger.info('💾 COSTOS GUARDADOS EN BD:')
        current_app.logger.info(f'  - tipo_material: "{costos_data.get("tipo_material")}"')
        current_app.logger.info(f'  - lana_costo_rollo: {costos_data.get("lana_costo_rollo")}')
        current_app.logger.info(f'  - lana_peso_rollo: {costos_data.get("lana_peso_rollo")}')
        current_app.logger.info(f'  - Todos los costos: {costos_data}')
        
        current_app.logger.info(f'Producto actualizado: name={product.name}, price={product.price}, category_id={product.category_id}')

        # Verificar si se subieron nuevas imágenes
        images_uploaded = any([
            form.image.data, form.image2.data, form.image3.data,
            form.image4.data, form.image5.data
        ])

        if images_uploaded:
            current_app.logger.info('📷 Imágenes nuevas subidas')
            # Procesar nuevas imágenes
            existing_images = product.get_all_images()
            image_filenames = _process_uploaded_images(form, existing_images)

            if image_filenames:
                product.image_main = image_filenames[0]
                product.images = image_filenames[1:] if len(image_filenames) > 1 else None
        # Si no se subieron imágenes, mantener las existentes (no hacer nada)

        db.session.commit()
        current_app.logger.info('✅ Producto guardado exitosamente en BD')
        current_app.logger.info('=' * 60)

        flash(f'Producto "{product.name}" actualizado exitosamente!', 'success')
        return redirect(url_for('admin.list_products'))
    else:
        # Debug: mostrar errores de validación
        current_app.logger.error('❌ Formulario NO válido')
        current_app.logger.error(f'Errores: {form.errors}')
        
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error en {field}: {error}', 'danger')
                    current_app.logger.error(f'  - {field}: {error}')
        
        current_app.logger.info('=' * 60)

    return render_template('admin/edit_product.html', form=form, product=product, categories=categories, material_types=material_types)


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


@admin_bp.route('/products/toggle-status/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def toggle_product_status(product_id):
    """Alternar estado activo/inactivo del producto."""
    product = Product.query.get_or_404(product_id)
    
    product.is_active = not product.is_active
    db.session.commit()
    
    if product.is_active:
        flash(f'Producto "{product.name}" publicado exitosamente!', 'success')
    else:
        flash(f'Producto "{product.name}" ocultado de la tienda!', 'info')
    
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


# ============================================
# GESTIÓN DE TIPOS DE MATERIALES
# ============================================

@admin_bp.route('/material-types')
@login_required
@admin_required
def list_material_types():
    """Listar tipos de materiales."""
    from app.models import MaterialType
    material_types = MaterialType.query.order_by(MaterialType.name.asc()).all()
    return render_template('admin/list_material_types.html', material_types=material_types)


@admin_bp.route('/material-types/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_material_type():
    """Crear nuevo tipo de material."""
    from app.models import MaterialType
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        default_cost = float(request.form.get('default_cost', 0) or 0)
        default_weight = int(request.form.get('default_weight', 50) or 50)
        description = request.form.get('description', '').strip()
        is_active = request.form.get('is_active', False)

        # Validaciones
        if not name:
            flash('El nombre del tipo de material es requerido', 'danger')
            return redirect(url_for('admin.create_material_type'))

        # Verificar si ya existe
        if MaterialType.query.filter_by(name=name).first():
            flash(f'El tipo de material "{name}" ya existe', 'danger')
            return redirect(url_for('admin.create_material_type'))

        # Crear tipo de material
        material_type = MaterialType(
            name=name,
            default_cost=default_cost,
            default_weight=default_weight,
            description=description if description else None,
            is_active=is_active == 'on'
        )

        db.session.add(material_type)
        db.session.commit()

        flash(f'Tipo de material "{name}" creado exitosamente!', 'success')
        return redirect(url_for('admin.list_material_types'))

    return render_template('admin/create_material_type.html')


@admin_bp.route('/material-types/edit/<int:type_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_material_type(type_id):
    """Editar tipo de material existente."""
    from app.models import MaterialType
    
    material_type = MaterialType.query.get_or_404(type_id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        default_cost = float(request.form.get('default_cost', 0) or 0)
        default_weight = int(request.form.get('default_weight', 50) or 50)
        description = request.form.get('description', '').strip()
        is_active = request.form.get('is_active', False)

        # Validaciones
        if not name:
            flash('El nombre del tipo de material es requerido', 'danger')
            return redirect(url_for('admin.edit_material_type', type_id=type_id))

        # Verificar si el nombre ya existe en otro tipo
        existing = MaterialType.query.filter_by(name=name).first()
        if existing and existing.id != type_id:
            flash(f'El tipo de material "{name}" ya existe', 'danger')
            return redirect(url_for('admin.edit_material_type', type_id=type_id))

        # Actualizar
        material_type.name = name
        material_type.default_cost = default_cost
        material_type.default_weight = default_weight
        material_type.description = description if description else None
        material_type.is_active = is_active == 'on'

        db.session.commit()

        flash(f'Tipo de material "{name}" actualizado exitosamente!', 'success')
        return redirect(url_for('admin.list_material_types'))

    return render_template('admin/edit_material_type.html', material_type=material_type)


@admin_bp.route('/material-types/delete/<int:type_id>', methods=['POST'])
@login_required
@admin_required
def delete_material_type(type_id):
    """Eliminar tipo de material."""
    from app.models import MaterialType
    
    material_type = MaterialType.query.get_or_404(type_id)

    try:
        db.session.delete(material_type)
        db.session.commit()
        flash(f'Tipo de material "{material_type.name}" eliminado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')

    return redirect(url_for('admin.list_material_types'))
