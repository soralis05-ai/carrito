import os
import logging

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
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_TO_CONSOLE = True
    LOG_TO_FILE = True
    LOG_FILE_PATH = os.path.join(basedir, '..', 'instance', 'logs')
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 5

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


    
