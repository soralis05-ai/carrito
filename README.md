# Almapunt - Tienda Online & Portfolio

E-commerce artesanal con panel de administración y portfolio personal integrado.

## 🚀 Estado del Proyecto

**Versión:** 1.0.0  
**Última actualización:** 28 de febrero de 2024  
**Framework:** Flask 3.1+  
**Python:** 3.14  
**Frontend:** Bootstrap 5.3.3 + Bootstrap Icons  
**Repositorio:** https://github.com/soralis05-ai/carrito.git

---

## 📋 Descripción

Almapunt es una plataforma de comercio electrónico diseñada para productos artesanales y únicos. Incluye:

- **Tienda completa** - Catálogo de productos con carrito de compras
- **Portfolio personal** - Página de presentación con galería de fotos destacadas
- **Panel de administración** - Gestión de productos y contenido del portfolio
- **Procesamiento de imágenes** - Subida multi-formato con redimensionamiento automático

---

## 🎨 Tema Visual

Diseño personalizado con gradiente signature:
- **Colores principales:** `#667eea` → `#764ba2` (morado/azul)
- **Estilo:** Moderno, limpio, con efectos hover y sombras suaves
- **Responsive:** Adaptable a móviles, tablets y desktop

---

## 📁 Estructura del Proyecto

```
c:\soraya\carrito\
├── app/
│   ├── __init__.py                 # Factory de la aplicación
│   ├── config.py                   # Configuraciones por entorno
│   ├── blueprints/
│   │   ├── admin/                  # Panel de administración
│   │   ├── auth/                   # Autenticación de usuarios
│   │   ├── cart/                   # Carrito de compras
│   │   ├── orders/                 # Gestión de pedidos
│   │   ├── portfolio/              # Portfolio personal (NUEVO)
│   │   └── products/               # Catálogo de productos
│   ├── models/                     # Modelos de base de datos
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css           # Estilos globales
│   │   │   └── components.css      # Componentes (productos, carrusel)
│   │   ├── img/
│   │   │   ├── productos/          # Imágenes de productos
│   │   │   └── portfolio/          # Imágenes del portfolio
│   │   └── js/
│   │       └── utils.js            # Utilidades JavaScript
│   ├── templates/
│   │   ├── base.html               # Template base (con tema portfolio)
│   │   ├── navbar.html             # Barra de navegación
│   │   ├── footer.html             # Pie de página
│   │   └── errors/                 # Páginas de error
│   └── utils/
│       ├── image_processor.py      # Procesamiento de imágenes (NUEVO)
│       ├── decorators.py           # Decoradores personalizados
│       └── helpers.py              # Funciones de ayuda
├── scripts/
│   └── resize_images.py            # Script para redimensionar imágenes
├── tests/                          # Tests unitarios
├── run.py                          # Punto de entrada
├── requirements.txt                # Dependencias
├── .env                            # Variables de entorno
└── .flaskenv                       # Configuración Flask
```

---

## 🔧 Instalación

### Requisitos previos
- Python 3.14+
- pip

### Pasos de instalación

```bash
# 1. Clonar o navegar al proyecto
cd c:\soraya\carrito

# 2. Crear entorno virtual (si no existe)
python -m venv .venv

# 3. Activar entorno virtual
.venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
# Editar .env con tus valores:
# SECRET_KEY=tu_clave_secreta
# DOMAIN=almapunt.es

# 6. Ejecutar la aplicación
python run.py
```

### Dependencias principales

```
Flask>=3.1
Flask-SQLAlchemy>=3.1
Flask-Login>=0.6
Flask-WTF>=1.2
Pillow>=10.0
pillow-avif-plugin>=1.5
python-dotenv>=1.0
waitress              # (opcional, para producción)
```

---

## 🌐 Rutas Disponibles

### Públicas
| Ruta | Descripción |
|------|-------------|
| `/` | Redirige al catálogo de productos |
| `/products/` | Catálogo completo de productos |
| `/products/<id>` | Detalle de producto individual |
| `/portfolio/` | **Portfolio personal** (página de presentación) |
| `/cart/` | Carrito de compras |
| `/orders/checkout` | Proceso de checkout |
| `/auth/login` | Inicio de sesión |
| `/auth/register` | Registro de usuarios |

### Administración
| Ruta | Descripción |
|------|-------------|
| `/admin/` | Dashboard principal |
| `/admin/products/upload` | Subir nuevo producto (hasta 5 imágenes) |
| `/admin/products` | Listar productos del catálogo |
| `/admin/portfolio` | **Gestión del portfolio** (NUEVO) |
| `/admin/portfolio/info` | Editar información personal |
| `/admin/portfolio/items` | Gestionar items del portfolio |
| `/admin/portfolio/upload` | Subir fotos al portfolio |

---

## 📸 Procesamiento de Imágenes

### Formatos soportados
- **Entrada:** JPG, JPEG, PNG, WEBP, AVIF, GIF
- **Salida:** WEBP (optimizado)

### Características
- Conversión automática a WEBP para mejor compresión
- Redimensionamiento manteniendo aspect ratio
- Manejo de transparencia (fondo blanco automático)
- Generación de 3 versiones:
  - `original`: 800x800px máx.
  - `thumbnail`: 220x220px (grid productos)
  - `detail`: 600x600px (página detalle)

### Uso del procesador
```python
from app.utils.image_processor import process_image, validate_image

# Validar formato
if validate_image(filename):
    # Procesar imagen
    result = process_image(
        input_path,
        output_path,
        max_size=(800, 800),
        output_format='WEBP',
        quality=85
    )
```

---

## 📝 Avance Realizado - 28 de Febrero 2024

### ✅ Completado

#### 1. Configuración Inicial y Debugging
- [x] Resuelto error 404/500 por procesos Python duplicados
- [x] Configurado `run.py` con servidor de desarrollo
- [x] Verificado mapeo de rutas de todos los blueprints

#### 2. Tema Visual Portfolio
- [x] Diseñado tema con gradiente morado/azul signature
- [x] Actualizado `base.html` con estilos inline del tema
- [x] Navbar con gradiente e íconos de Bootstrap
- [x] Footer con 3 columnas y mismo gradiente
- [x] Hero section en página de productos
- [x] Tarjetas de productos con hover effects y precios gradiente
- [x] Cards responsive con shadow y bordes redondeados

#### 3. Sistema de Imágenes Multi-formato
- [x] Creado `app/utils/image_processor.py`
- [x] Instalado `pillow-avif-plugin` para soporte AVIF
- [x] Soporte para: JPG, PNG, WEBP, AVIF, GIF
- [x] Conversión automática a WEBP
- [x] Generación de thumbnails y versiones detail
- [x] Script `resize_images.py` para procesamiento batch

#### 4. Formulario de Subida de Productos
- [x] 5 campos de imagen (1 obligatorio + 4 opcionales)
- [x] Vista previa en tiempo real para cada imagen
- [x] Validación de formatos desde el formulario
- [x] Procesamiento con redimensionamiento automático
- [x] Nombres de archivo únicos (UUID)

#### 5. Página de Detalle de Producto
- [x] Carrusel Bootstrap para múltiples imágenes
- [x] Miniaturas clickeables debajo del carrusel
- [x] Selector de cantidad
- [x] Botón "Añadir al Carrito"
- [x] Información de envío y garantías
- [x] Imagen simple si solo hay 1 foto

#### 6. Módulo Portfolio Personal
- [x] Blueprint `/portfolio` independiente
- [x] Página pública con hero, bio y galería
- [x] Panel de administración para portfolio
- [x] Formulario para información personal (nombre, bio, contacto)
- [x] Subida de items al portfolio con vista previa
- [x] Orden de visualización configurable
- [x] Eliminación de items
- [x] Integración en navbar y admin dashboard

#### 7. Documentación
- [x] Estructura de archivos organizada
- [x] Comentarios en código
- [x] Templates separados por blueprint

---

## 🎯 Mejoras para Implementar - Mañana

### Prioridad Alta 🔴

#### 1. Base de Datos para Portfolio
- [ ] Migrar de sesión a base de datos (SQLite/PostgreSQL)
- [ ] Crear modelos: `PortfolioItem`, `PortfolioInfo`
- [ ] CRUD completo con SQLAlchemy
- [ ] Persistencia de datos entre reinicios

#### 2. Carrito de Compras Funcional
- [ ] Implementar sesión de carrito
- [ ] Añadir/eliminar productos del carrito
- [ ] Calcular total dinámicamente
- [ ] Guardar carrito en base de datos (usuarios registrados)

#### 3. Sistema de Usuarios
- [ ] Completar registro de usuarios (Flask-Login)
- [ ] Login/logout funcional
- [ ] Roles (admin vs cliente)
- [ ] Protección de rutas admin con `@login_required`

### Prioridad Media 🟡

#### 4. Checkout y Pedidos
- [ ] Formulario de datos de envío
- [ ] Integración con pasarela de pago (Stripe/PayPal)
- [ ] Confirmación de pedido por email
- [ ] Historial de pedidos por usuario

#### 5. Mejoras en Portfolio
- [ ] Lightbox para ver imágenes en grande
- [ ] Filtros por categoría
- [ ] Paginación de items
- [ ] Drag & drop para reordenar

#### 6. Panel de Administración
- [ ] Dashboard con estadísticas (ventas, productos, visitas)
- [ ] Gráficos con Chart.js
- [ ] Exportar datos a CSV/Excel
- [ ] Editor de productos existente (editar/eliminar)

### Prioridad Baja 🟢

#### 7. Optimización SEO
- [ ] Meta tags dinámicos por página
- [ ] Sitemap.xml
- [ ] Robots.txt
- [ ] URLs amigables

#### 8. Rendimiento
- [ ] Caché de templates (Flask-Caching)
- [ ] Lazy loading para imágenes
- [ ] Minificación de CSS/JS
- [ ] CDN para assets estáticos

#### 9. Experiencia de Usuario
- [ ] Búsqueda de productos
- [ ] Filtros por precio/categoría
- [ ] Ordenamiento (precio, nombre, popularidad)
- [ ] Productos relacionados en detalle

#### 10. Seguridad
- [ ] Rate limiting en formularios
- [ ] CSRF protection en todas las rutas
- [ ] Validación de archivos más estricta
- [ ] HTTPS en producción

---

## 📊 Próximos Hitos

| Hito | Fecha Estimada | Estado |
|------|----------------|--------|
| Portfolio con BD | 1 marzo | ⏳ Pendiente |
| Carrito funcional | 3 marzo | ⏳ Pendiente |
| Usuarios y auth | 5 marzo | ⏳ Pendiente |
| Checkout completo | 10 marzo | ⏳ Pendiente |
| Producción (deploy) | 15 marzo | ⏳ Pendiente |

---

## 🛠️ Comandos Útiles

```bash
# Ejecutar en desarrollo
python run.py

# Ejecutar con waitress (producción)
python -c "from waitress import serve; from app import create_app; serve(create_app(), host='0.0.0.0', port=5000)"

# Redimensionar imágenes existentes
python scripts/resize_images.py

# Ver rutas registradas
python -c "from app import create_app; app = create_app(); [print(r) for r in app.url_map.iter_rules()]"

# Tests
python -m pytest tests/
```

---

## 🗄️ Base de Datos

### Motor: SQLite (Desarrollo y Producción)

**Configuración:**
- **Desarrollo (Windows):** `sqlite:///app.db`
- **Producción (Hetzner/Debian):** `sqlite:///app.db` (mismo archivo)
- **Sin dependencias adicionales:** No requiere instalar MySQL/PostgreSQL

### Modelos Disponibles

| Modelo | Tabla | Descripción |
|--------|-------|-------------|
| `User` | `users` | Usuarios con Flask-Login (admin, clientes) |
| `Product` | `products` | Productos con imágenes (JSON), stock, categorías |
| `Category` | `categories` | Categorías de productos |
| `CartItem` | `cart_items` | Items del carrito (usuarios o sesiones) |
| `Order` | `orders` | Pedidos con estados y totales |
| `OrderItem` | `order_items` | Items individuales de cada pedido |

### Inicializar Base de Datos

```cmd
# Crear tablas y datos de ejemplo
python scripts/init_db.py
```

**Datos de ejemplo creados:**
- 4 categorías (Peluches, Accesorios, Hogar, Papelería)
- 6 productos de ejemplo
- 1 usuario admin (username: `admin`, email: `admin@almapunt.es`)

### Servicios Conectados a la DB

| Servicio | Métodos Principales |
|----------|---------------------|
| `ProductsService` | `get_all()`, `get_by_id()`, `search()`, `get_featured()` |
| `CartService` | `add_item()`, `remove_item()`, `calculate_total()`, `clear_cart()` |
| `AuthService` | `login()`, `register()`, `logout()` (con password hashing) |

### Migrar a Producción (Hetzner)

```bash
# Opción 1: Copiar la DB existente
scp app.db user@hetzner:/var/www/almapunt/

# Opción 2: Inicializar en el servidor
ssh user@hetzner
cd /var/www/almapunt
source .venv/bin/activate
python scripts/init_db.py
```

### Backup de la DB

```bash
# Copiar archivo SQLite
cp app.db app.db.backup

# O comprimir
tar -czf db-backup-$(date +%Y%m%d).tar.gz app.db
```

---

## 🔐 Autenticación

### Características

- **Flask-Login** integrado para gestión de sesiones
- **Password hashing** con Werkzeug (SHA256)
- **Roles:** Usuario normal y Admin
- **Carrito persistente** por usuario o sesión (invitados)

### Registro de Usuarios

```python
from werkzeug.security import generate_password_hash

# Crear usuario con password seguro
password_hash = generate_password_hash('tu_password')
```

### Login en Templates

```html
{% if current_user.is_authenticated %}
    <p>Bienvenido, {{ current_user.username }}</p>
{% else %}
    <a href="{{ url_for('auth.login') }}">Iniciar sesión</a>
{% endif %}
```

### Rutas Protegidas

```python
from flask_login import login_required

@app.route('/admin')
@login_required
def admin_panel():
    return render_template('admin.html')
```

---

## 🎛️ Control de Versiones (Git/GitHub)

### Repositorio Oficial
```
URL: https://github.com/soralis05-ai/carrito.git
Rama: main
```

### Configuración de Git

**Git instalado en:** `C:\Program Files\Git\bin\git.exe`  
**Credenciales:** Guardadas en Credential Manager de Windows

### Token de Desarrollo

| Característica | Detalle |
|----------------|---------|
| **Ubicación** | `%USERPROFILE%\AppData\Local\Git\credentials` |
| **Permisos** | Lectura/Escritura (`repo`, `workflow`) |
| **Seguridad** | Encriptado por Windows, solo Git puede leerlo |
| **NO está en** | Ningún archivo .md, .txt, ni en GitHub |

### Gestión de Credenciales

Para ver, cambiar o eliminar el token guardado:

```cmd
scripts\git-credentials.bat
```

Este script proporciona un menú interactivo para:
1. ✅ Verificar que el token está guardado
2. ⚠️ Ver el token (no recomendado en público)
3. 🗑️ Eliminar credenciales (para cambiar token)
4. 🔌 Verificar conexión con GitHub

### Flujo de Trabajo Diario

```cmd
# Antes de empezar a trabajar:
git pull origin main

# Después de hacer cambios:
git add .
git commit -m "Descripción clara del cambio"
git push origin main    # No pide token, ya está guardado

# Ver estado del repositorio:
git status

# Ver historial de commits:
git log --oneline

# Ver cambios sin subir:
git diff
```

### Cambio de Token

Si necesitas cambiar el token de desarrollo:

1. Ejecuta: `scripts\git-credentials.bat`
2. Selecciona opción 3 (Eliminar credenciales)
3. La próxima vez que hagas `git push`, Git te pedirá el nuevo token
4. Pega tu nuevo token de GitHub

### Token de Producción

Para desplegar en producción (Vercel, Railway, etc.):

1. **Crea un token NUEVO** en GitHub:
   - URL: https://github.com/settings/tokens/new
   - Nombre: `almapunt-production`
   - Permisos: `public_repo` (solo lectura)

2. **Configúralo en el servidor** como variable de entorno:
   ```
   GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
   ```

3. **NUNCA uses tu token de desarrollo en producción**

### Archivos de Configuración

| Archivo | Propósito | ¿En GitHub? |
|---------|-----------|-------------|
| `scripts/git-credentials.bat` | Gestor visual de tokens | ✅ Sí |
| `docs/GITHUB_SETUP.md` | Guía detallada de configuración | ✅ Sí |
| `.git-config-local.txt` | Referencia de configuración local | ✅ Sí |
| `.gitignore` | Excluye .env, .venv, __pycache__ | ✅ Sí |
| `.env` | Variables de entorno reales | ❌ No (seguridad) |

### Solución de Problemas

| Problema | Solución |
|----------|----------|
| "Permission denied" al hacer push | Token expirado. Elimina credenciales y vuelve a ingresar |
| "Git no se reconoce" | Usa ruta completa: `"C:\Program Files\Git\bin\git.exe"` |
| Conflictos de merge | Edita archivos, busca `<<<<<<<`, resuelve y haz commit |
| Olvidé hacer commit | `git commit --amend -m "Nuevo mensaje"` |

### Más Información

- **Guía completa:** `docs/GITHUB_SETUP.md`
- **Gestor de tokens:** `scripts/git-credentials.bat`
- **Referencia local:** `.git-config-local.txt`

---

## 📧 Contacto

- **Dominio:** almapunt.es
- **Email:** contacto@almapunt.es
- **Ubicación:** España

---

## 📄 Licencia

Todos los derechos reservados © 2024 Almapunt

---

*Documento generado el 28 de febrero de 2024*
