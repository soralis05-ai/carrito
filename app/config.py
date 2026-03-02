import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                         'sqlite:///' + os.path.join(basedir, '..', 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DOMAIN = os.environ.get('DOMAIN', 'almapunt.es')
    LOGO_PATH = os.environ.get('LOGO_PATH', '/static/img/brand/logo.png')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
