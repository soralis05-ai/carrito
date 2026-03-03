import os
import uuid
from flask import render_template, redirect, url_for, flash, current_app, session
from werkzeug.utils import secure_filename
from . import portfolio_bp
from .forms import PortfolioItemForm, PortfolioInfoForm
from app.utils.image_processor import process_image, validate_image


# Datos temporales en sesión (en producción usar base de datos)
DEFAULT_PORTFOLIO_INFO = {
    'name': 'Almapunt',
    'title': 'Artesanía y Productos Únicos',
    'bio': 'Somos una tienda especializada en productos artesanales y únicos. Cada pieza está seleccionada con cuidado para ofrecer calidad y originalidad a nuestros clientes.',
    'email': 'soralis05@gmail.com',
    'phone': ''
}


@portfolio_bp.route('/')
def show():
    """Mostrar página pública del portfolio."""
    # Obtener información del portfolio
    portfolio_info = session.get('portfolio_info', DEFAULT_PORTFOLIO_INFO)
    
    # Obtener items del portfolio
    portfolio_items = session.get('portfolio_items', [])
    
    # Ordenar por orden de visualización
    portfolio_items.sort(key=lambda x: int(x.get('order', 999)))
    
    return render_template('portfolio/public.html', 
                         info=portfolio_info, 
                         items=portfolio_items)


@portfolio_bp.route('/admin')
def admin_dashboard():
    """Panel de administración del portfolio."""
    portfolio_info = session.get('portfolio_info', DEFAULT_PORTFOLIO_INFO)
    portfolio_items = session.get('portfolio_items', [])
    portfolio_items.sort(key=lambda x: int(x.get('order', 999)))
    
    return render_template('portfolio/admin/dashboard.html', 
                         info=portfolio_info, 
                         items=portfolio_items)


@portfolio_bp.route('/admin/info', methods=['GET', 'POST'])
def admin_info():
    """Editar información personal del portfolio."""
    form = PortfolioInfoForm()
    
    # Cargar datos existentes
    if not form.is_submitted():
        existing_info = session.get('portfolio_info', DEFAULT_PORTFOLIO_INFO)
        form.name.data = existing_info.get('name', '')
        form.title.data = existing_info.get('title', '')
        form.bio.data = existing_info.get('bio', '')
        form.email.data = existing_info.get('email', '')
        form.phone.data = existing_info.get('phone', '')
    
    if form.validate_on_submit():
        portfolio_info = {
            'name': form.name.data,
            'title': form.title.data,
            'bio': form.bio.data,
            'email': form.email.data,
            'phone': form.phone.data
        }
        session['portfolio_info'] = portfolio_info
        flash('Información del portfolio actualizada exitosamente!', 'success')
        return redirect(url_for('portfolio.admin_dashboard'))
    
    return render_template('portfolio/admin/info.html', form=form)


@portfolio_bp.route('/admin/items')
def admin_items():
    """Listar items del portfolio."""
    portfolio_items = session.get('portfolio_items', [])
    portfolio_items.sort(key=lambda x: int(x.get('order', 999)))
    return render_template('portfolio/admin/items.html', items=portfolio_items)


@portfolio_bp.route('/admin/items/upload', methods=['GET', 'POST'])
def admin_upload():
    """Subir nuevo item al portfolio."""
    form = PortfolioItemForm()
    
    if form.validate_on_submit():
        image_file = form.image.data
        if image_file:
            if not validate_image(image_file.filename):
                flash(f'Formato no soportado: {image_file.filename}', 'danger')
                return render_template('portfolio/admin/upload.html', form=form)
            
            # Generar nombre único
            original_filename = secure_filename(image_file.filename)
            extension = os.path.splitext(original_filename)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}"
            
            # Guardar en carpeta de portfolio
            upload_folder = os.path.join(
                current_app.root_path, 
                'static', 
                'img', 
                'portfolio'
            )
            os.makedirs(upload_folder, exist_ok=True)
            
            # Ruta temporal
            temp_path = os.path.join(upload_folder, f"{unique_filename}_temp{extension}")
            image_file.save(temp_path)
            
            # Procesar imagen
            output_base = os.path.join(upload_folder, unique_filename)
            result = process_image(
                temp_path, 
                output_base,
                max_size=(1200, 1200),
                output_format='WEBP',
                quality=90
            )
            
            # Eliminar temporal
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            if result['success']:
                # Guardar item
                portfolio_item = {
                    'id': uuid.uuid4().hex,
                    'title': form.title.data,
                    'description': form.description.data,
                    'image': os.path.basename(result['path']),
                    'order': form.order.data or '999'
                }
                
                # Obtener items existentes y añadir nuevo
                portfolio_items = session.get('portfolio_items', [])
                portfolio_items.append(portfolio_item)
                session['portfolio_items'] = portfolio_items
                
                flash(f'Item "{form.title.data}" añadido al portfolio exitosamente!', 'success')
                return redirect(url_for('portfolio.admin_items'))
            else:
                flash(f'Error procesando imagen: {result["error"]}', 'danger')
    
    return render_template('portfolio/admin/upload.html', form=form)


@portfolio_bp.route('/admin/items/delete/<item_id>')
def admin_delete(item_id):
    """Eliminar item del portfolio."""
    portfolio_items = session.get('portfolio_items', [])
    portfolio_items = [i for i in portfolio_items if i['id'] != item_id]
    session['portfolio_items'] = portfolio_items
    
    flash('Item eliminado del portfolio', 'info')
    return redirect(url_for('portfolio.admin_items'))
