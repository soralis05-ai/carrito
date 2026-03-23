"""
Módulo de logging centralizado para Almapunt E-commerce.

Uso:
    from app.utils.logger import get_logger
    
    logger = get_logger(__name__)
    logger.info("Mensaje informativo")
    logger.error("Mensaje de error", extra={"user_id": 123})
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional
from flask import request, session
from flask_login import current_user


class RequestContextFilter(logging.Filter):
    """
    Filtro que agrega contexto de request a cada log.
    
    Agrega automáticamente:
    - user_id: ID del usuario logueado (o 'anonymous')
    - user_ip: IP del cliente
    - endpoint: Endpoint solicitado
    - method: Método HTTP (GET, POST, etc.)
    """
    
    def filter(self, record):
        try:
            # Intentar obtener contexto de Flask
            record.user_id = getattr(current_user, 'id', 'anonymous')
            record.user_ip = request.remote_addr or 'unknown'
            record.endpoint = request.endpoint or 'unknown'
            record.method = request.method or 'unknown'
        except RuntimeError:
            # Fuera de contexto de request
            record.user_id = 'no-context'
            record.user_ip = 'no-context'
            record.endpoint = 'no-context'
            record.method = 'no-context'
        
        return True


def setup_logging(app) -> None:
    """
    Configurar logging para la aplicación Flask.
    
    Args:
        app: Aplicación Flask
    """
    # Crear directorio de logs si no existe
    log_dir = Path(app.instance_path) / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configurar formato con contexto de request
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s '
        '[user:%(user_id)s ip:%(user_ip)s %(method)s %(endpoint)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(RequestContextFilter())
    
    # Handler para archivo (rotativo)
    file_handler = RotatingFileHandler(
        log_dir / 'almapunt.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(RequestContextFilter())
    
    # Configurar logger de la app
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(stream_handler)
    app.logger.addHandler(file_handler)
    
    # Configurar logger de Werkzeug (requests HTTP)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.addHandler(stream_handler)
    werkzeug_logger.addHandler(file_handler)
    werkzeug_logger.addFilter(RequestContextFilter())
    
    app.logger.info('🚀 Logging configurado exitosamente')
    app.logger.info(f'Logs guardados en: {log_dir}')
    app.logger.info('✅ Contexto de request habilitado (user_id, ip, endpoint)')


def get_logger(name: str) -> logging.Logger:
    """
    Obtener un logger configurado para un módulo específico.
    
    Args:
        name: Nombre del módulo (usualmente __name__)
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)


class LogContext:
    """
    Contexto de logging para agregar información adicional automáticamente.
    
    Uso:
        with LogContext(user_id=user.id, action='create_product'):
            logger.info('Producto creado')
    """
    
    def __init__(self, **kwargs):
        self.context = kwargs
        self.old_factory = None
    
    def __enter__(self):
        self.old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            # Agregar contexto al record
            for key, value in self.context.items():
                setattr(record, key, value)
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.setLogRecordFactory(self.old_factory)
