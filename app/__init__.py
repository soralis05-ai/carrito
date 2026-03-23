from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import logging

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.DevelopmentConfig')

    # Configurar logging
    from app.utils.logger import setup_logging
    setup_logging(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página'
    login_manager.login_message_category = 'warning'
    migrate.init_app(app, db)

    # User loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return db.session.get(User, int(user_id))

    # Context processor para carrito
    @app.context_processor
    def inject_cart_count():
        """Inyectar contador del carrito en todos los templates."""
        from flask_login import current_user
        from app.blueprints.cart.services import CartService
        import uuid
        
        user_id = current_user.id if current_user.is_authenticated else None
        session_id = session.get('session_id') or str(uuid.uuid4())
        
        cart_count = CartService.count_items(user_id=user_id, session_id=session_id)
        return {'cart_count': cart_count}

    # Registrar blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.products import products_bp
    from app.blueprints.cart import cart_bp
    from app.blueprints.orders import orders_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.portfolio import portfolio_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio')

    # Página de construcción en la ruta raíz
    @app.route('/')
    def index():
        return render_template('coming_soon.html')

    # Manejador de error 403 (acceso denegado)
    @app.errorhandler(403)
    def handle_forbidden(e):
        return render_template('errors/403.html'), 403

    # Manejador de error 404 (página no encontrada)
    @app.errorhandler(404)
    def handle_not_found(e):
        return render_template('errors/404.html'), 404

    # Manejador de error 500 (error interno del servidor)
    @app.errorhandler(500)
    def handle_internal_error(e):
        db.session.rollback()  # Importante: rollback de la sesión
        return render_template('errors/500.html'), 500

    # Manejador de error 503 (servicio no disponible)
    @app.errorhandler(503)
    def handle_service_unavailable(e):
        return render_template('errors/503.html'), 503

    # Manejador de error 413 (archivo demasiado grande)
    @app.errorhandler(413)
    def handle_too_large(e):
        flash('El archivo subido es demasiado grande. Tamaño máximo: 5 MB por imagen.', 'danger')
        return render_template('errors/413.html'), 413

    # Importar modelos después de registrar blueprints
    with app.app_context():
        from app.models import User, Product, Category, PortfolioInfo, PortfolioItem
        db.create_all()

    return app