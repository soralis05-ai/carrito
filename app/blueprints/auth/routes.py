from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from app import db
from app.models import User

def get_logger():
    """Obtener logger de la app."""
    try:
        return current_app.logger
    except RuntimeError:
        import logging
        return logging.getLogger(__name__)

logger = get_logger()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login de usuarios."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        # Buscar usuario por email
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            logger.info(f'Usuario logueado: {user.username} (email: {user.email})')
            flash('¡Bienvenido!', 'success')

            # Redirigir al siguiente o según rol
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            # Si es admin, ir al dashboard
            if user.is_admin:
                logger.info(f'Admin {user.username} accedió al dashboard')
                return redirect(url_for('admin.dashboard'))

            # Si es usuario normal, ir a productos
            return redirect(url_for('products.list'))
        else:
            logger.warning(f'Intento de login fallido para email: {email}')
            flash('Email o contraseña incorrectos', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevos usuarios."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')

        # Validaciones
        errors = []

        if not username or len(username) < 3:
            errors.append('El usuario debe tener al menos 3 caracteres')

        if not email or '@' not in email:
            errors.append('Email inválido')
        
        if not password or len(password) < 6:
            errors.append('La contraseña debe tener al menos 6 caracteres')
        
        if password != password_confirm:
            errors.append('Las contraseñas no coinciden')
        
        # Verificar si el email ya existe
        if User.query.filter_by(email=email).first():
            errors.append('El email ya está registrado')
        
        # Verificar si el username ya existe
        if User.query.filter_by(username=username).first():
            errors.append('El nombre de usuario ya existe')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')
        
        # Crear usuario
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión."""
    logger.info(f'Usuario cerró sesión: {current_user.username}')
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('products.list'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Perfil de usuario - Ver y editar."""
    if request.method == 'POST':
        # Obtener datos del formulario
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        zip_code = request.form.get('zip_code', '').strip()
        country = request.form.get('country', 'España').strip()

        # Validar email único (si cambió)
        if email != current_user.email:
            existing = User.query.filter_by(email=email).first()
            if existing:
                logger.warning(f'Intento de usar email duplicado: {email} (user: {current_user.username})')
                flash('El email ya está en uso', 'danger')
                return redirect(url_for('auth.profile'))

        # Actualizar usuario
        old_email = current_user.email
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email
        current_user.phone = phone
        current_user.address = address
        current_user.city = city
        current_user.zip_code = zip_code
        current_user.country = country

        db.session.commit()
        logger.info(f'Perfil actualizado: {current_user.username} (email: {old_email} → {email})')
        flash('Perfil actualizado exitosamente', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', user=current_user)


@auth_bp.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    """Cambiar contraseña."""
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Validar contraseña actual
    if not check_password_hash(current_user.password_hash, current_password):
        flash('Contraseña actual incorrecta', 'danger')
        return redirect(url_for('auth.profile'))
    
    # Validar nueva contraseña
    if len(new_password) < 6:
        flash('La contraseña debe tener al menos 6 caracteres', 'danger')
        return redirect(url_for('auth.profile'))
    
    # Validar confirmación
    if new_password != confirm_password:
        flash('Las contraseñas no coinciden', 'danger')
        return redirect(url_for('auth.profile'))
    
    # Actualizar contraseña
    current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    flash('Contraseña actualizada exitosamente', 'success')
    return redirect(url_for('auth.profile'))
