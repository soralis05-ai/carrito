from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.DevelopmentConfig')
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # minimal user loader (no users yet)
    @login_manager.user_loader
    def load_user(user_id):
        return None
    
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

    # redirect root to products listing
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('products.list'))

    with app.app_context():
        db.create_all()

    return app