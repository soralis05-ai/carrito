import os
import uuid
from flask import render_template, redirect, url_for, flash, current_app, request
from werkzeug.utils import secure_filename
from . import portfolio_bp
from .forms import PortfolioItemForm, PortfolioInfoForm
from app.utils.image_processor import process_image, validate_image
from app import db
from app.models.portfolio_info import PortfolioInfo
from app.models.portfolio_item import PortfolioItem


@portfolio_bp.route('/')
def show():
    """Mostrar página pública del portfolio."""
    # Obtener información del portfolio
    portfolio_info = PortfolioInfo.get_or_create()

    # Obtener items del portfolio activos ordenados
    portfolio_items = PortfolioItem.get_all_active()

    return render_template('portfolio/public.html',
                         info=portfolio_info,
                         items=portfolio_items)


@portfolio_bp.route('/admin')
def admin_dashboard():
    """Panel de administración del portfolio."""
    portfolio_info = PortfolioInfo.get_or_create()
    portfolio_items = PortfolioItem.query.order_by(PortfolioItem.order).all()

    return render_template('portfolio/admin/dashboard.html',
                         info=portfolio_info,
                         items=portfolio_items)


@portfolio_bp.route('/admin/info', methods=['GET', 'POST'])
def admin_info():
    """Editar información personal del portfolio."""
    form = PortfolioInfoForm()

    # Obtener o crear registro de información
    portfolio_info = PortfolioInfo.get_or_create()

    # Cargar datos existentes
    if not form.is_submitted():
        form.name.data = portfolio_info.name
        form.title.data = portfolio_info.title
        form.bio.data = portfolio_info.bio
        form.email.data = portfolio_info.email
        form.phone.data = portfolio_info.phone

    if form.validate_on_submit():
        # Actualizar registro existente
        portfolio_info.name = form.name.data
        portfolio_info.title = form.title.data
        portfolio_info.bio = form.bio.data
        portfolio_info.email = form.email.data
        portfolio_info.phone = form.phone.data

        db.session.commit()

        flash('Información del portfolio actualizada exitosamente!', 'success')
        return redirect(url_for('portfolio.admin_dashboard'))

    return render_template('portfolio/admin/info.html', form=form, info=portfolio_info)


@portfolio_bp.route('/admin/items')
def admin_items():
    """Listar items del portfolio."""
    portfolio_items = PortfolioItem.query.order_by(PortfolioItem.order).all()
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
                # Crear item en base de datos
                portfolio_item = PortfolioItem(
                    title=form.title.data,
                    description=form.description.data,
                    image=os.path.basename(result['path']),
                    order=int(form.order.data) if form.order.data else 999
                )

                db.session.add(portfolio_item)
                db.session.commit()

                flash(f'Item "{form.title.data}" añadido al portfolio exitosamente!', 'success')
                return redirect(url_for('portfolio.admin_items'))
            else:
                flash(f'Error procesando imagen: {result["error"]}', 'danger')

    return render_template('portfolio/admin/upload.html', form=form)


@portfolio_bp.route('/admin/items/delete/<int:item_id>')
def admin_delete(item_id):
    """Eliminar item del portfolio."""
    portfolio_item = PortfolioItem.query.get_or_404(item_id)

    # Eliminar de la base de datos
    db.session.delete(portfolio_item)
    db.session.commit()

    flash('Item eliminado del portfolio', 'info')
    return redirect(url_for('portfolio.admin_items'))


@portfolio_bp.route('/admin/items/edit/<int:item_id>', methods=['GET', 'POST'])
def admin_edit(item_id):
    """Editar item del portfolio."""
    portfolio_item = PortfolioItem.query.get_or_404(item_id)
    form = PortfolioItemForm()

    if form.validate_on_submit():
        # Actualizar item
        portfolio_item.title = form.title.data
        portfolio_item.description = form.description.data
        portfolio_item.order = int(form.order.data) if form.order.data else 999

        # Procesar nueva imagen si se sube una
        if form.image.data:
            image_file = form.image.data
            if validate_image(image_file.filename):
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
                    # Eliminar imagen anterior
                    old_image_path = os.path.join(upload_folder, portfolio_item.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                    portfolio_item.image = os.path.basename(result['path'])
                else:
                    flash(f'Error procesando nueva imagen: {result["error"]}', 'warning')

        db.session.commit()
        flash(f'Item "{form.title.data}" actualizado exitosamente!', 'success')
        return redirect(url_for('portfolio.admin_items'))

    # Cargar datos existentes
    if request.method == 'GET':
        form.title.data = portfolio_item.title
        form.description.data = portfolio_item.description
        form.order.data = str(portfolio_item.order) if portfolio_item.order != 999 else ''

    return render_template('portfolio/admin/edit.html', form=form, item=portfolio_item)
