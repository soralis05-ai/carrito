from functools import wraps
from flask import flash, redirect, url_for, session
from flask_login import current_user


def admin_required(f):
    """
    Decorador para requerir que el usuario sea admin.
    Usa junto con @login_required.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar que el usuario esté logueado
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión para acceder al panel de administración', 'warning')
            return redirect(url_for('auth.login', next=url_for('admin.dashboard')))
        
        # Verificar que sea admin
        if not current_user.is_admin:
            flash('No tienes permisos de administrador para acceder a esta página', 'danger')
            return redirect(url_for('products.list'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def guest_required(f):
    """
    Decorador para rutas que solo deben verse si NO está logueado.
    Útil para login/register.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('products.list'))
        return f(*args, **kwargs)
    
    return decorated_function
