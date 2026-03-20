import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                         'sqlite:///' + os.path.join(basedir, '..', 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DOMAIN = os.environ.get('DOMAIN', 'almapunt.es')
    LOGO_PATH = os.environ.get('LOGO_PATH', '/static/img/brand/logo.png')
    
    # Límite de tamaño para subida de archivos (16 MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB máximo por request
    
    # Tamaño máximo por imagen (5 MB)
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB por imagen

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
