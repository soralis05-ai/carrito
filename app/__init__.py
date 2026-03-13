from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.DevelopmentConfig')
    
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
        return User.query.get(int(user_id))

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

    # Importar modelos después de registrar blueprints
    with app.app_context():
        from app.models import User, Product, Category, PortfolioInfo, PortfolioItem
        db.create_all()

    return app