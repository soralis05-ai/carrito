"""
Script para redimensionar y uniformizar todas las imágenes de productos.
Las imágenes se escalan a un tamaño máximo manteniendo el aspect ratio.
"""
from PIL import Image
import os

# Configuración
INPUT_FOLDER = os.path.join('app', 'static', 'img', 'productos')
OUTPUT_FOLDER = os.path.join('app', 'static', 'img', 'productos_resized')
MAX_SIZE = (800, 800)  # Tamaño máximo en píxeles (ancho, alto)
QUALITY = 85  # Calidad de compresión JPEG (1-100)

def resize_image(input_path, output_path, max_size):
    """Redimensiona una imagen manteniendo el aspect ratio."""
    try:
        with Image.open(input_path) as img:
            # Convertir a RGB si es necesario (para manejar PNG con transparencia)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionar si excede el tamaño máximo
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Guardar imagen redimensionada
            img.save(output_path, 'JPEG', quality=QUALITY, optimize=True)
            print(f"[OK] {os.path.basename(input_path)} -> {img.size[0]}x{img.size[1]}")
            return True
    except Exception as e:
        print(f"[ERROR] procesando {os.path.basename(input_path)}: {e}")
        return False

def main():
    # Crear carpeta de salida si no existe
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Obtener lista de imágenes
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
    images = [f for f in os.listdir(INPUT_FOLDER) 
              if f.lower().endswith(valid_extensions)]
    
    print(f"Encontradas {len(images)} imagenes para procesar\n")
    
    # Procesar cada imagen
    success_count = 0
    for filename in sorted(images):
        input_path = os.path.join(INPUT_FOLDER, filename)
        
        # Cambiar extensión a .jpg para uniformidad
        output_filename = os.path.splitext(filename)[0] + '.jpg'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        if resize_image(input_path, output_path, MAX_SIZE):
            success_count += 1
    
    print(f"\n[OK] {success_count}/{len(images)} imagenes procesadas exitosamente")
    print(f"Imagenes guardadas en: {OUTPUT_FOLDER}")

if __name__ == '__main__':
    main()
