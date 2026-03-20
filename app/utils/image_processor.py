"""
Módulo utilitario para procesamiento de imágenes.
Soporta: JPG, JPEG, PNG, WEBP, AVIF, GIF
Convierte todas las imágenes a formato uniforme y tamaño consistente.
"""
import os
from PIL import Image

# Intentar registrar el plugin AVIF si está disponible
try:
    import pillow_avif_plugin  # Registro del plugin AVIF
except ImportError:
    pass  # AVIF no disponible, pero otros formatos funcionan


# Formatos soportados
SUPPORTED_FORMATS = {
    'jpg': 'JPEG',
    'jpeg': 'JPEG',
    'png': 'PNG',
    'webp': 'WEBP',
    'avif': 'AVIF',
    'gif': 'PNG'  # GIF animado se convierte a PNG estático
}

# Extensiones permitidas para formularios (exportado para forms.py)
ALLOWED_EXTENSIONS = list(SUPPORTED_FORMATS.keys())
EXTENSIONS_STRING = ', '.join(ext.upper() for ext in ALLOWED_EXTENSIONS)

# Configuración de redimensionamiento
IMAGE_CONFIG = {
    'productos': {
        'max_size': (800, 800),      # Tamaño máximo original
        'thumbnail_size': (220, 220), # Para grid de productos
        'detail_size': (600, 600),    # Para página de detalle
        'quality': 85,
        'format': 'WEBP'              # Formato de salida uniforme
    }
}


def get_image_format(filename):
    """Obtener formato desde la extensión del archivo."""
    ext = os.path.splitext(filename)[1].lower().lstrip('.')
    return SUPPORTED_FORMATS.get(ext)


def validate_image(filename):
    """Validar si el archivo tiene un formato soportado."""
    ext = os.path.splitext(filename)[1].lower().lstrip('.')
    return ext in SUPPORTED_FORMATS


def validate_file_size(file_storage, max_size_mb=5):
    """
    Validar tamaño de archivo Flask FileStorage.
    
    Args:
        file_storage: Flask FileStorage object
        max_size_mb: Tamaño máximo en MB (default: 5)
    
    Returns:
        tuple: (is_valid, error_message, file_size_mb)
    """
    # Obtener tamaño
    file_storage.stream.seek(0, 2)  # Ir al final
    file_size = file_storage.stream.tell()
    file_storage.stream.seek(0)  # Volver al inicio
    
    file_size_mb = file_size / (1024 * 1024)
    
    if file_size_mb > max_size_mb:
        return False, f'Imagen demasiado grande ({file_size_mb:.2f} MB). Tamaño máximo: {max_size_mb} MB', file_size_mb
    
    return True, None, file_size_mb


def get_allowed_extensions():
    """Obtener lista de extensiones permitidas para el formulario."""
    return ALLOWED_EXTENSIONS


def process_image(
    input_path, 
    output_path, 
    max_size=(800, 800), 
    output_format='WEBP',
    quality=85
):
    """
    Procesar imagen: convertir, redimensionar y optimizar.
    
    Args:
        input_path: Ruta de la imagen original
        output_path: Ruta de salida (sin extensión)
        max_size: Tamaño máximo (ancho, alto)
        output_format: Formato de salida (WEBP, JPEG, PNG)
        quality: Calidad de compresión (1-100)
    
    Returns:
        dict con información de la imagen procesada
    """
    result = {
        'success': False,
        'path': None,
        'thumbnail_path': None,
        'detail_path': None,
        'original_size': None,
        'processed_size': None,
        'error': None
    }
    
    try:
        with Image.open(input_path) as img:
            # Guardar tamaño original
            result['original_size'] = img.size
            
            # Convertir a RGB si es necesario (para formatos con transparencia)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Crear fondo blanco para imágenes con transparencia
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                # Pegar imagen sobre fondo usando canal alpha
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[3])
                else:
                    background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionar manteniendo aspect ratio
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            result['processed_size'] = img.size
            
            # Determinar extensión de salida
            ext_map = {'WEBP': '.webp', 'JPEG': '.jpg', 'PNG': '.png'}
            output_ext = ext_map.get(output_format, '.webp')
            
            # Guardar imagen principal
            main_path = f"{output_path}{output_ext}"
            if output_format == 'WEBP':
                img.save(main_path, 'WEBP', quality=quality, optimize=True)
            elif output_format == 'JPEG':
                img.save(main_path, 'JPEG', quality=quality, optimize=True)
            else:
                img.save(main_path, 'PNG', optimize=True)
            result['path'] = main_path
            
            # Crear thumbnail para grid de productos
            thumbnail = img.copy()
            thumbnail.thumbnail(IMAGE_CONFIG['productos']['thumbnail_size'], Image.Resampling.LANCZOS)
            thumb_path = f"{output_path}_thumb{output_ext}"
            if output_format == 'WEBP':
                thumbnail.save(thumb_path, 'WEBP', quality=quality, optimize=True)
            elif output_format == 'JPEG':
                thumbnail.save(thumb_path, 'JPEG', quality=quality, optimize=True)
            else:
                thumbnail.save(thumb_path, 'PNG', optimize=True)
            result['thumbnail_path'] = thumb_path
            
            # Crear versión para detalle
            detail = img.copy()
            detail.thumbnail(IMAGE_CONFIG['productos']['detail_size'], Image.Resampling.LANCZOS)
            detail_path = f"{output_path}_detail{output_ext}"
            if output_format == 'WEBP':
                detail.save(detail_path, 'WEBP', quality=quality, optimize=True)
            elif output_format == 'JPEG':
                detail.save(detail_path, 'JPEG', quality=quality, optimize=True)
            else:
                detail.save(detail_path, 'PNG', optimize=True)
            result['detail_path'] = detail_path
            
            result['success'] = True
            
    except Exception as e:
        result['error'] = str(e)
    
    return result


def resize_for_display(image_path, size=(300, 300)):
    """
    Redimensionar imagen para visualización en contenedor específico.
    
    Args:
        image_path: Ruta de la imagen
        size: Tupla (ancho, alto) del contenedor
    
    Returns:
        Ruta de la imagen redimensionada o None si hay error
    """
    try:
        with Image.open(image_path) as img:
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            output_path = image_path.rsplit('.', 1)[0] + '_resized.webp'
            img.save(output_path, 'WEBP', quality=85, optimize=True)
            
            return output_path
    except Exception:
        return None
