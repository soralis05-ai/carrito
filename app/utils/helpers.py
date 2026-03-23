"""
Funciones helper utilitarias para la aplicación.
Centraliza funciones comunes para evitar duplicación.
"""

from datetime import datetime
from typing import Optional


def format_currency(amount: float, currency: str = '€') -> str:
    """
    Formatear cantidad como moneda.
    
    Args:
        amount: Cantidad a formatear
        currency: Símbolo de moneda (default: €)
    
    Returns:
        String formateado (ej: "€10.00")
    """
    return f"{currency}{amount:.2f}"


def format_datetime(dt: Optional[datetime], format_str: str = '%d/%m/%Y %H:%M') -> str:
    """
    Formatear datetime como string.
    
    Args:
        dt: Datetime a formatear
        format_str: Formato de salida
    
    Returns:
        String formateado o '-' si es None
    """
    if dt is None:
        return '-'
    return dt.strftime(format_str)


def truncate_string(text: str, length: int = 50, suffix: str = '...') -> str:
    """
    Truncar string a longitud máxima.
    
    Args:
        text: Texto a truncar
        length: Longitud máxima
        suffix: Sufijo para texto truncado
    
    Returns:
        Texto truncado o completo si es menor que length
    """
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def generate_slug(text: str) -> str:
    """
    Generar slug desde texto.
    
    Args:
        text: Texto original
    
    Returns:
        Slug formateado (minúsculas, sin espacios, sin caracteres especiales)
    """
    slug = text.lower().strip()
    slug = slug.replace(' ', '-').replace('_', '-')
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    return slug


def calculate_percentage(value: float, total: float) -> float:
    """
    Calcular porcentaje.
    
    Args:
        value: Valor del cual calcular porcentaje
        total: Total base
    
    Returns:
        Porcentaje (0-100) o 0 si total es 0
    """
    if total == 0:
        return 0.0
    return (value / total) * 100


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    División segura (evita división por cero).
    
    Args:
        numerator: Numerador
        denominator: Denominador
        default: Valor por defecto si denominador es 0
    
    Returns:
        Resultado de la división o default
    """
    if denominator == 0:
        return default
    return numerator / denominator
