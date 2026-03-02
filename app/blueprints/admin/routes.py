import os
import uuid
from flask import render_template, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from . import admin_bp
from .forms import ProductUploadForm
from app.utils.image_processor import process_image, validate_image


@admin_bp.route('/')
def dashboard():
    """Panel principal de administración."""
    return render_template('admin/dashboard.html')


@admin_bp.route('/products/upload', methods=['GET', 'POST'])
def upload_product():
    """Subir nuevo producto con imagenes."""
    form = ProductUploadForm()
    
    if form.validate_on_submit():
        # Lista para almacenar nombres de imágenes
        image_filenames = []
        
        # Procesar todas las imágenes subidas
        image_fields = ['image', 'image2', 'image3', 'image4', 'image5']
        
        for field_name in image_fields:
            image_file = getattr(form, field_name).data
            if image_file:
                # Validar formato
                if not validate_image(image_file.filename):
                    flash(f'Formato no soportado: {image_file.filename}', 'danger')
                    continue
                
                # Generar nombre único para la imagen
                original_filename = secure_filename(image_file.filename)
                extension = os.path.splitext(original_filename)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}"
                
                # Guardar en carpeta de productos
                upload_folder = os.path.join(
                    current_app.root_path, 
                    'static', 
                    'img', 
                    'productos'
                )
                os.makedirs(upload_folder, exist_ok=True)
                
                # Ruta temporal para el archivo original
                temp_path = os.path.join(upload_folder, f"{unique_filename}_temp{extension}")
                image_file.save(temp_path)
                
                # Procesar imagen con el utilitario
                output_base = os.path.join(upload_folder, unique_filename)
                result = process_image(
                    temp_path, 
                    output_base,
                    max_size=(800, 800),
                    output_format='WEBP',
                    quality=85
                )
                
                # Eliminar archivo temporal
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                if result['success']:
                    # Guardar solo el nombre del archivo principal (sin extensión)
                    image_filenames.append(os.path.basename(result['path']))
                else:
                    flash(f'Error procesando imagen: {result["error"]}', 'danger')
        
        if image_filenames:
            flash(f'Producto "{form.name.data}" guardado exitosamente con {len(image_filenames)} imagen(es)!', 'success')
            return redirect(url_for('admin.upload_product'))
    
    return render_template('admin/upload_product.html', form=form)


@admin_bp.route('/products')
def list_products():
    """Listar productos para administración."""
    from app.blueprints.products.services import ProductsService
    products = ProductsService.get_all()
    return render_template('admin/list_products.html', products=products)
