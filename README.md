# Almapunt - Tienda Online & Portfolio

E-commerce artesanal con panel de administración y portfolio personal integrado.

## 🚀 Estado del Proyecto

**Versión:** 1.4.0
**Última actualización:** 13 de marzo de 2026
**Framework:** Flask 3.1+
**Python:** 3.14
**Frontend:** Bootstrap 5.3.3 + Bootstrap Icons
**Repositorio:** https://github.com/soralis05-ai/carrito.git
**Dominio:** almapunt.es
**Email:** soralis05@gmail.com

---

## 🎯 Filosofía de Trabajo - Reglas de Oro

> **Nuestra filosofía de desarrollo se basa en 7 reglas fundamentales que guían cada decisión técnica:**

### 1. 🏛️ Separación de Responsabilidades
**Mantener la separación entre administración y lado público.**

- ✅ Templates independientes: `base.html` (público) vs `admin_base.html` (administración)
- ✅ Navbars separadas: `navbar.html` (pública) vs `admin_navbar.html` (admin)
- ✅ Blueprints bien delimitados: cada módulo tiene su responsabilidad clara
- ✅ Contextos diferentes: el admin nunca comparte layout con el público

### 2. 🎨 Diseño Consistente
**Mantener el diseño en todas las plantillas, tanto públicas como de administración.**

- ✅ Mismo framework CSS (Bootstrap 5.3.3) en todo el proyecto
- ✅ Mismos íconos (Bootstrap Icons) en toda la aplicación
- ✅ Estilos coherentes pero diferenciados por contexto
- ✅ Experiencia de usuario uniforme en cada sección

### 3. 🚫 No Duplicar Código
**No duplicar código en ningún archivo `.py` ni en plantillas.**

- ✅ Constantes centralizadas (ej: `ALLOWED_EXTENSIONS` en `image_processor.py`)
- ✅ Funciones utilitarias reutilizables
- ✅ Templates base que extienden funcionalidad
- ✅ Imports compartidos en lugar de código repetido

### 4. 🧹 Eliminar Código en Desuso
**Eliminar código en desuso tanto en archivos `.py` como en plantillas.**

- ✅ Archivos vacíos o incompletos se eliminan (ej: `services.py` vacíos)
- ✅ Funciones no usadas se remueven (ej: `helpers.py` con watermark)
- ✅ Templates sin uso se eliminan del proyecto
- ✅ Imports innecesarios se limpian

### 5. 🧼 Producción Limpia
**Producción se debe mantener limpia, sin basura de desarrollo ni archivos `*.md`.**

- ✅ Tests solo en desarrollo, no en producción
- ✅ Scripts de migración/documentación separados
- ✅ Archivos temporales se eliminan después de usar
- ✅ Solo código necesario en producción

### 6. 📚 Documentación Actualizada
**Solo se documentará en el archivo `README.md` de forma actualizada, ordenada y sin duplicados.**

- ✅ Único README.md como fuente de verdad
- ✅ Historial de cambios cronológico y sin repetir
- ✅ Novedades de versión en la parte superior
- ✅ Estructura clara y navegable
- ✅ No hay otros archivos `.md` de documentación

### 7. 🏗️ Blueprints Bien Estructurados
**Mantener los blueprints bien estructurados.**

- ✅ Cada blueprint en su directorio: `admin/`, `auth/`, `cart/`, `products/`, `portfolio/`, `orders/`
- ✅ Estructura consistente: `__init__.py`, `routes.py`, `forms.py`, `templates/`
- ✅ Templates en subdirectorios por blueprint
- ✅ Models separados en `app/models/`
- ✅ Utils compartidos en `app/utils/`

### 8. 🔐 Variables de Entorno Seguras
**Nunca crear ni subir `.env.example` al repositorio.**

- ✅ `.env` contiene secretos reales (SECRET_KEY, DATABASE_URL)
- ✅ `.env` está en `.gitignore` y nunca se sube
- ✅ Documentar variables requeridas directamente en el README
- ✅ En producción usar variables de entorno del servidor
- ✅ No crear `.env.example` o `.env.template` (regla de seguridad)

---

## 📋 Descripción

Almapunt es una plataforma de comercio electrónico diseñada para productos artesanales y únicos. Incluye:

- **Tienda completa** - Catálogo de productos con carrito de compras
- **Portfolio personal** - Página de presentación con galería de fotos destacadas
- **Panel de administración** - Gestión de productos con calculadora de costos
- **Procesamiento de imágenes** - Subida multi-formato con redimensionamiento automático
- **Calculadora de Amigurumis** - Cálculo automático de precios basado en costos

---

## 🆕 Novedades (v1.4.0 - 13 marzo 2026)

### 🛒 Checkout y Carrito de Compras

**✨ Carrito de Compras Funcional:**
- ✅ Añadir/eliminar productos del carrito
- ✅ Actualizar cantidades (+ / -)
- ✅ Contador de items en navbar
- ✅ Session-based (usuarios e invitados)
- ✅ AJAX para añadir sin recargar
- ✅ Toast notifications

**📝 Checkout Básico:**
- ✅ Formulario de datos de envío
- ✅ Cálculo automático de IVA (21%)
- ✅ Envío gratis en todos los pedidos
- ✅ Validación de campos requeridos
- ✅ Guardado de pedido en base de datos

**📄 Oferta en PDF Descargable:**
- ✅ Generación automática con ReportLab
- ✅ Diseño profesional con colores de marca
- ✅ Incluye: datos de envío, productos, totales
- ✅ Validez de 7 días
- ✅ Descarga desde confirmación de pedido

**🔧 Nuevas Dependencias:**
- `reportlab>=4.0` - Generación de PDFs

---

## 🆕 Novedades (v1.3.4 - 13 marzo 2026)

### Flask-Migrate para Gestión de Base de Datos

**📦 Nueva Dependencia:**
- ✅ `Flask-Migrate>=4.0` agregado a `requirements.txt`
- ✅ `migrate.init_app(app, db)` registrado en `app/__init__.py`

**🔧 Comandos Disponibles:**
```bash
flask db init          # Inicializar (solo primera vez)
flask db migrate -m "Mensaje"  # Crear migración
flask db upgrade       # Aplicar migraciones
flask db current       # Ver estado actual
flask db downgrade -1  # Revertir última migración
```

**📝 Nueva Regla de Oro (#8):**
- 🔐 **Variables de Entorno Seguras** - Nunca crear `.env.example`
- ✅ `.env` siempre en `.gitignore`
- ✅ Documentar variables en README directamente
- ✅ No crear plantillas de `.env`

**🗑️ Scripts Manuales:**
- Los scripts `add_costos_column.py` y `add_portfolio_tables.py` fueron reemplazados por Flask-Migrate
- Se mantiene `run_migrations.py` para compatibilidad

---

## 🆕 Novedades (v1.3.3 - 13 marzo 2026)

### 🔒 Seguridad: Templates Admin en Blueprint

**Cambio de Ubicación por Seguridad:**
- ❌ **Antes:** `app/templates/admin_base.html`, `app/templates/admin_navbar.html` (globales)
- ✅ **Ahora:** `app/blueprints/admin/templates/admin/layout.html`, `app/blueprints/admin/templates/admin/_navbar.html`

**Ventajas:**
- 🛡️ **Aislamiento:** Templates de admin aislados en el blueprint
- 🔐 **Seguridad:** No accesibles desde otros blueprints accidentalmente
- 📁 **Organización:** Estructura más clara y mantenible
- 🎯 **Convención:** Sigue mejores prácticas de Flask

**Archivos Movidos:**
| Archivo Original | Nueva Ubicación |
|-----------------|-----------------|
| `app/templates/admin_base.html` | `app/blueprints/admin/templates/admin/layout.html` |
| `app/templates/admin_navbar.html` | `app/blueprints/admin/templates/admin/_navbar.html` |

**Templates Actualizados (12):**
- ✅ 7 templates de admin (`admin/*.html`)
- ✅ 5 templates de portfolio admin (`portfolio/admin/*.html`)

---

## 🆕 Novedades (v1.3.2 - 13 marzo 2026)

### Navbar Independiente para Admin

**✨ Separación de Contextos:**
- **Navbar Público:** Mantiene el diseño con gradiente morado/azul signature
- **Navbar Admin:** Diseño oscuro profesional (`#2c3e50` → `#34495e`)
- **Templates independientes:** `admin_base.html` y `admin_navbar.html`

**📝 Nuevos Templates:**
- `app/templates/admin_base.html` - Base layout exclusivo para admin
- `app/templates/admin_navbar.html` - Navbar específico para panel de administración

**🎨 Diferencias Visuales:**
| Característica | Navbar Público | Navbar Admin |
|----------------|----------------|--------------|
| Color | Gradiente morado/azul | Oscuro profesional |
| Icono | `bi-shop` Almapunt | `bi-gear-fill` Admin Panel |
| Enlaces | Tienda, Portfolio, Carrito | Dashboard, Productos, Portfolio, Categorías |
| Fondo | Gradiente signature | `#2c3e50` → `#34495e` |

---

## 🆕 Novedades (v1.3.1 - 13 marzo 2026)

### Mejoras en Administración de Productos

**✨ Nuevo Layout de Formularios:**
- **Columna Izquierda (4 cols):** Configuración y Costos Amigurumis
- **Columna Derecha (8 cols):** Información Básica, Precio/Stock, Imágenes
- **Botones de acción:** Alineados a la derecha, debajo de las imágenes

**🐛 Bug Fixes en Edición:**
- Precarga correcta de costos desde base de datos
- Visualización de imágenes existentes adicionales
- Validación de precio > 0 antes de guardar
- Imagen principal opcional al editar

**📝 Nuevos Formularios:**
- `ProductEditForm` - Versión de edición con imagen opcional
- Validaciones mejoradas para evitar precio 0

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
│   │   ├── admin/                  # Panel de administración (CRUD productos y categorías)
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── forms.py
│   │   │   └── templates/
│   │   │       └── admin/
│   │   │           ├── layout.html         # Layout exclusivo admin ✨ SEGURO
│   │   │           ├── _navbar.html        # Navbar exclusivo admin ✨ SEGURO
│   │   │           ├── dashboard.html
│   │   │           ├── upload_product.html
│   │   │           ├── edit_product.html
│   │   │           ├── list_products.html
│   │   │           ├── list_categories.html
│   │   │           ├── create_category.html
│   │   │           └── edit_category.html
│   │   ├── auth/                   # Autenticación de usuarios
│   │   ├── cart/                   # Carrito de compras
│   │   ├── orders/                 # Gestión de pedidos
│   │   ├── portfolio/              # Portfolio personal
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
│   │   ├── navbar.html             # Barra de navegación (pública)
│   │   ├── footer.html             # Pie de página
│   │   └── errors/                 # Páginas de error
│   └── utils/
│       ├── image_processor.py      # Procesamiento de imágenes
│       ├── decorators.py           # Decoradores personalizados
│       └── helpers.py              # Funciones de ayuda (eliminado en v1.3.2)
├── scripts/
│   ├── add_costos_column.py        # Migración: agrega columna costos
│   ├── add_portfolio_tables.py     # Migración: tablas portfolio ✨ NUEVO
│   ├── clear_sample_products.py    # Eliminar productos de ejemplo
│   ├── create_admin.py             # Crear usuario administrador
│   ├── create_admin_quick.py       # Crear admin (no interactivo)
│   ├── init_db.py                  # Inicializar base de datos
│   ├── manage_users.py             # Gestionar usuarios
│   ├── reset_password.py           # Resetear contraseña
│   └── resize_images.py            # Redimensionar imágenes batch
├── tests/                          # Tests unitarios
│   ├── __init__.py
│   ├── test_auth.py                # Tests de autenticación
│   ├── test_cart.py                # Tests del carrito
│   └── test_products.py            # Tests de productos
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
| `/admin/portfolio/items/edit/<id>` | Editar item existente ✨ NUEVO |
| `/admin/portfolio/items/delete/<id>` | Eliminar item del portfolio |

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
- [x] **Base de datos para portfolio** (v1.3.0) ✨

#### 7. Edición de Productos (v1.3.1) ✨
- [x] Precarga de datos de costos en edición
- [x] Precarga de checkboxes (ojos, mano de obra, utilidad)
- [x] Visualización de imágenes existentes
- [x] Validación de precio > 0
- [x] Imagen principal opcional en edición
- [x] Layout invertido (Configuración izquierda, Información derecha)
- [x] Botones de acción a la derecha

#### 8. Documentación
- [x] Estructura de archivos organizada
- [x] Comentarios en código
- [x] Templates separados por blueprint

---

## 🎯 Mejoras para Implementar - Mañana

### Prioridad Alta 🔴

#### 1. Carrito de Compras Funcional
- [ ] Implementar sesión de carrito
- [ ] Añadir/eliminar productos del carrito
- [ ] Calcular total dinámicamente
- [ ] Guardar carrito en base de datos (usuarios registrados)

#### 2. Sistema de Usuarios
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
- [x] Migrar de sesión a base de datos (SQLite) ✨ COMPLETADO (v1.3.0)
- [x] Modelos: `PortfolioItem`, `PortfolioInfo`
- [x] CRUD completo con SQLAlchemy
- [x] Persistencia de datos entre reinicios
- [x] Edición de items ✨ COMPLETADO (v1.3.1)
- [ ] Lightbox para ver imágenes en grande
- [ ] Filtros por categoría
- [ ] Paginación de items
- [ ] Drag & drop para reordenar

#### 6. Panel de Administración
- [x] Editor de productos existente (editar/eliminar) ✨ COMPLETADO (v1.3.1)
- [x] Layout optimizado (Configuración izquierda, Información derecha) ✨ COMPLETADO (v1.3.1)
- [x] Validación de precio > 0 ✨ COMPLETADO (v1.3.1)
- [ ] Dashboard con estadísticas (ventas, productos, visitas)
- [ ] Gráficos con Chart.js
- [ ] Exportar datos a CSV/Excel

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
| Portfolio con BD | 13 marzo | ✅ Completado |
| Mejoras Admin (v1.3.1) | 13 marzo | ✅ Completado |
| Carrito funcional | 15 marzo | ⏳ Pendiente |
| Usuarios y auth | 17 marzo | ⏳ Pendiente |
| Checkout completo | 20 marzo | ⏳ Pendiente |
| Producción (deploy) | 25 marzo | ⏳ Pendiente |

---

## 🛠️ Comandos Útiles

```bash
# Ejecutar en desarrollo
python run.py

# Ejecutar con waitress (producción)
python -c "from waitress import serve; from app import create_app; serve(create_app(), host='0.0.0.0', port=5000)"

# Instalar dependencias
pip install -r requirements.txt

# Redimensionar imágenes existentes
python scripts/resize_images.py

# Tests
python -m pytest tests/
```

### Flask-Migrate (Base de Datos)

```bash
# Inicializar migraciones (solo primera vez)
flask db init

# Crear nueva migración después de cambiar modelos
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Ver estado de migraciones
flask db current

# Revertir última migración
flask db downgrade -1
```

### Migraciones en Producción (Hetzner/Debian)

**⚠️ IMPORTANTE: Primero instalar Flask-Migrate**

```bash
# 1. Conectarse al servidor
ssh user@hetzner

# 2. Navegar al proyecto
cd /var/www/almapunt

# 3. Activar entorno virtual
source .venv/bin/activate

# 4. Instalar Flask-Migrate (solo primera vez)
pip install Flask-Migrate

# 5. Actualizar dependencias del proyecto
pip install -r requirements.txt

# 6. Aplicar migraciones
flask db upgrade

# 7. Reiniciar aplicación
sudo systemctl restart almapunt
```

**Resolver conflictos de Git en producción:**

```bash
# Si hay conflicto con requirements.txt:
git stash              # Guardar cambios locales temporalmente
git pull origin main   # Actualizar desde GitHub
git stash pop          # Restaurar cambios locales (si los hay)

# O descartar cambios locales:
git checkout -- requirements.txt
git pull origin main
```

### Verificar Base de Datos (SQLite)

```bash
# Ver tablas
sqlite3 app.db ".tables"

# Ver esquema de tabla
sqlite3 app.db ".schema products"

# Ver columna específica
sqlite3 app.db "PRAGMA table_info(products);"
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
| `PortfolioInfo` | `portfolio_info` | Información del portfolio (nombre, bio, contacto) ✨ NUEVO |
| `PortfolioItem` | `portfolio_items` | Items/gallery del portfolio (imágenes destacadas) ✨ NUEVO |

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

## 🧮 Calculadora de Costos para Amigurumis

### Descripción

El panel de administración incluye una calculadora automática de costos para productos artesanales (amigurumis). El **precio de venta se calcula automáticamente** basado en los costos de materiales y mano de obra.

### Fórmula de Cálculo

```
┌─────────────────────────────────────────────────────────┐
│  CÁLCULO AUTOMÁTICO DE PRECIO DE VENTA                 │
├─────────────────────────────────────────────────────────┤
│  1. MATERIALES:                                         │
│     Lana = (costo_rollo / peso_rollo) × peso_usado     │
│     Relleno = (costo_bolsa / peso_bolsa) × peso_usado  │
│     Ojos = costo_unitario × cantidad                    │
│     ─────────────────────────────────────────────────  │
│     Subtotal Materiales = Lana + Relleno + Ojos        │
│                                                         │
│  2. MANO DE OBRA (Opcional ☑):                          │
│     Mano de Obra = costo_hora × horas_dedicadas        │
│                                                         │
│  3. COSTO TOTAL:                                        │
│     Costo Total = Materiales + Mano de Obra            │
│                                                         │
│  4. UTILIDAD ADICIONAL (Opcional ☑):                    │
│     Utilidad = Costo Total × (porcentaje / 100)        │
│                                                         │
│  5. PRECIO DE VENTA (Automático):                       │
│     Precio = Costo Total + Utilidad                     │
│     (Se calcula SOLO en el campo de Precio de Venta)   │
└─────────────────────────────────────────────────────────┘
```

### Ejemplo Práctico

**Datos ingresados:**

```
MATERIALES:
  Lana:    5.00€ (rollo 50g) → Usa 30g      = 3.00€
  Relleno: 3.00€ (bolsa 100g) → Usa 20g    = 0.60€
  Ojos:    0.50€ × 1 par                    = 0.50€
  ────────────────────────────────────────────────
  Subtotal Materiales:                      = 4.10€

MANO DE OBRA ☑:
  Costo por Hora: 10.00€
  Horas Dedicadas: 2 horas
  ────────────────────────────────────────────────
  Mano de Obra: 10.00 × 2                   = 20.00€

COSTO TOTAL: 4.10 + 20.00                   = 24.10€

UTILIDAD ADICIONAL ☑:
  Porcentaje: 20%
  Utilidad: 24.10 × 0.20                    = 4.82€

┌─────────────────────────────────────────────────────┐
│  PRECIO DE VENTA: 24.10 + 4.82 = 28.92€ (AUTO)     │
└─────────────────────────────────────────────────────┘
```

### Interfaz de Usuario

**Flujo en el formulario:**

1. **Información Básica** (arriba):
   - Nombre del producto
   - **Precio de Venta** ← Se calcula automáticamente (readonly)
   - Descripción

2. **Costos de Producción** (abajo):
   - ☑ Lana (costo, peso, usado)
   - ☑ Relleno (costo, peso, usado)
   - ☑ Ojos (checkbox, costo, cantidad)
   - ☑ Mano de Obra (checkbox, costo/hora, horas)
   - ☑ Utilidad (checkbox, porcentaje)

3. **Referencia**:
   - Muestra "Costo Total + Utilidad" como referencia
   - El precio se actualiza automáticamente mientras escribes

### Características

| Característica | Descripción |
|----------------|-------------|
| **Auto-cálculo** | El precio se actualiza en tiempo real |
| **Campo readonly** | No editable manualmente (solo cálculo) |
| **Opcional** | Mano de obra y utilidad son opcionales (checkbox) |
| **Referencia** | Muestra el desglose como referencia |
| **JavaScript** | Cálculo instantáneo sin recargar |

### Código JavaScript

```javascript
function calcularCostos() {
    // Lana
    const costoLana = (costoLanaRollo / pesoLanaRollo) * pesoLanaUsado;
    
    // Relleno
    const costoRelleno = (costoRellenoBolsa / pesoRellenoBolsa) * pesoRellenoUsado;
    
    // Ojos (si checkbox activo)
    const costoOjos = ojosUsar ? (ojosCosto * ojosCantidad) : 0;
    
    // Mano de Obra (si checkbox activo)
    const costoManoObra = manoObraUsar ? (manoObraCostoHora * manoObraHoras) : 0;
    
    // Utilidad (si checkbox activo)
    const utilidad = utilidadUsar ? ((costoLana + costoRelleno + costoOjos + costoManoObra) * (utilidadPorcentaje / 100)) : 0;
    
    // Costo Total
    const costoTotal = costoLana + costoRelleno + costoOjos + costoManoObra;
    
    // Precio de Venta (Automático)
    const precioVenta = costoTotal + utilidad;
    
    // Actualizar campo de Precio de Venta (readonly)
    document.querySelector('#precio_venta').value = precioVenta.toFixed(2);
}
```

---

## 📚 Gestión del Portfolio

### Descripción

El módulo Portfolio permite mostrar una galería de productos destacados con información personal del artista. Totalmente gestionado desde el panel de administración.

### Migración de Base de Datos

```cmd
# Crear tablas del portfolio
python scripts/add_portfolio_tables.py
```

**Tablas creadas:**
- `portfolio_info` - Información general (nombre, bio, contacto)
- `portfolio_items` - Items individuales (título, descripción, imagen, orden)

### Modelos

#### PortfolioInfo

```python
from app.models import PortfolioInfo

# Obtener información (o crear por defecto)
info = PortfolioInfo.get_or_create()
print(info.name)    # 'Almapunt'
print(info.bio)     # Biografía del artista
```

**Campos:**
- `name` - Nombre del artista o negocio
- `title` - Título profesional
- `bio` - Biografía (hasta 1000 caracteres)
- `email` - Email de contacto
- `phone` - Teléfono

#### PortfolioItem

```python
from app.models import PortfolioItem
from app import db

# Obtener todos los items activos
items = PortfolioItem.get_all_active()

# Crear nuevo item
item = PortfolioItem(
    title='Colección Primavera',
    description='Amigurumis florales',
    image='abc123.webp',
    order=1
)
db.session.add(item)
db.session.commit()
```

**Campos:**
- `title` - Título del item
- `description` - Descripción (hasta 500 caracteres)
- `image` - Nombre del archivo WEBP
- `order` - Orden de visualización (menor = primero)
- `is_active` - Estado (activo/inactivo)

### Rutas Públicas

| Ruta | Descripción |
|------|-------------|
| `/portfolio/` | Página pública con galería completa |

**Características:**
- Hero section con nombre y título
- Biografía del artista
- Grid responsive de items
- Información de contacto
- Botón "Ver Tienda"

### Rutas de Administración

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/portfolio/admin` | GET | Dashboard del portfolio |
| `/portfolio/admin/info` | GET, POST | Editar información personal |
| `/portfolio/admin/items` | GET | Listar todos los items |
| `/portfolio/admin/items/upload` | GET, POST | Subir nuevo item |
| `/portfolio/admin/items/edit/<id>` | GET, POST | Editar item existente |
| `/portfolio/admin/items/delete/<id>` | GET | Eliminar item |

### Flujo de Trabajo

1. **Configurar información personal:**
   - Ir a `/portfolio/admin/info`
   - Completar nombre, título, biografía y contacto
   - Guardar cambios

2. **Subir items al portfolio:**
   - Ir a `/portfolio/admin/items/upload`
   - Subir imagen (JPG, PNG, WEBP, AVIF)
   - Completar título y descripción
   - Definir orden de visualización
   - Vista previa en tiempo real

3. **Gestionar items existentes:**
   - Ir a `/portfolio/admin/items`
   - Editar: modificar datos o cambiar imagen
   - Eliminar: confirmar eliminación

### Procesamiento de Imágenes

- **Formatos soportados:** JPG, PNG, WEBP, AVIF, GIF
- **Conversión:** Automática a WEBP
- **Tamaño máximo:** 1200x1200px
- **Calidad:** 90%
- **Ubicación:** `app/static/img/portfolio/`

### Ejemplo: Ver Portfolio Público

```
URL: http://localhost:5000/portfolio/

Muestra:
├── Hero con gradiente morado/azul
├── Nombre: Almapunt
├── Título: Artesanía y Productos Únicos
├── Biografía
└── Grid de items (3 columnas)
    ├── Imagen
    ├── Título
    └── Descripción
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
- **Email:** soralis05@gmail.com
- **Ubicación:** España

---

## 📄 Licencia

Todos los derechos reservados © 2024-2026 Almapunt

---

## 📝 Historial de Cambios

### Versión 1.4.0 (13 de marzo de 2026) - **ACTUAL** ✨

**🛒 Carrito de Compras:**
- ✅ Implementación completa del carrito
- ✅ Session-based para usuarios e invitados
- ✅ AJAX para añadir sin recargar
- ✅ Contador de items en navbar
- ✅ Toast notifications

**📝 Checkout Básico:**
- ✅ Formulario de envío completo
- ✅ Cálculo de IVA (21%)
- ✅ Envío gratis
- ✅ Validación de campos
- ✅ Guardado en BD (Order, OrderItem)

**📄 PDF de Oferta:**
- ✅ Generación con ReportLab
- ✅ Diseño profesional (colores de marca)
- ✅ Datos de envío, productos, totales
- ✅ Descarga desde confirmación
- ✅ Validez 7 días

**Archivos Nuevos:**
- `app/blueprints/orders/routes.py` - Rutas de checkout
- `orders/checkout.html` - Formulario de checkout
- `orders/confirmation.html` - Confirmación de pedido

---

### Versión 1.3.4 (13 de marzo de 2026)

**Flask-Migrate para Base de Datos:**

- ✅ **Flask-Migrate agregado** - `requirements.txt` actualizado
- ✅ **Migrate registrado** - `migrate.init_app(app, db)` en `app/__init__.py`
- ✅ **Comandos disponibles** - `flask db migrate`, `flask db upgrade`
- ✅ **Documentación actualizada** - Comandos de migración en README

**⚠️ IMPORTANTE - Producción (Hetzner):**

Después de hacer pull en producción, ejecutar:

```bash
cd /var/www/almapunt
source .venv/bin/activate
pip install Flask-Migrate
pip install -r requirements.txt
flask db upgrade
sudo systemctl restart almapunt
```

**Nueva Regla de Oro (#8):**
- ✅ **Variables de Entorno Seguras** - Nunca crear `.env.example`
- ✅ `.env` siempre en `.gitignore`
- ✅ Documentar variables directamente en README

**Scripts:**
- 🗑️ Scripts manuales reemplazados por Flask-Migrate
- ✅ `run_migrations.py` se mantiene para compatibilidad

---

### Versión 1.3.3 (13 de marzo de 2026)

**🔒 Seguridad: Templates Admin en Blueprint:**

- ✅ **Templates movidos a blueprint admin** - De `app/templates/` a `app/blueprints/admin/templates/admin/`
- ✅ **Renombrados por convención** - `layout.html` y `_navbar.html`
- ✅ **12 templates actualizados** - Todos usan `admin/layout.html`
- ✅ **Archivos globales eliminados** - `admin_base.html`, `admin_navbar.html` eliminados

**Archivos Movidos:**
| Original | Nueva Ubicación |
|----------|----------------|
| `app/templates/admin_base.html` | `app/blueprints/admin/templates/admin/layout.html` |
| `app/templates/admin_navbar.html` | `app/blueprints/admin/templates/admin/_navbar.html` |

**Ventajas de Seguridad:**
- 🛡️ Aislamiento total del admin
- 🔐 No accesible desde otros blueprints
- 📁 Mejor organización del código
- 🎯 Sigue mejores prácticas de Flask

---

### Versión 1.3.2 (13 de marzo de 2026)

**Navbar Independiente para Admin:**

- ✅ **Separación de contextos** - Admin y público ahora tienen navbars diferentes
- ✅ **Nuevo template `admin_base.html`** - Layout exclusivo para panel de administración
- ✅ **Nuevo template `admin_navbar.html`** - Navbar oscuro profesional para admin
- ✅ **Todos los templates admin actualizados** - 12 templates migrados a `admin_base.html`

**Templates Actualizados:**
- ✅ `admin/dashboard.html`, `admin/list_products.html`, `admin/upload_product.html`
- ✅ `admin/edit_product.html`, `admin/list_categories.html`
- ✅ `admin/create_category.html`, `admin/edit_category.html`
- ✅ `portfolio/admin/dashboard.html`, `portfolio/admin/info.html`
- ✅ `portfolio/admin/items.html`, `portfolio/admin/upload.html`, `portfolio/admin/edit.html`

**Diferencias Visuales:**
| Característica | Navbar Público | Navbar Admin |
|----------------|----------------|--------------|
| Color | Gradiente morado/azul | Oscuro (`#2c3e50` → `#34495e`) |
| Icono | `bi-shop` Almapunt | `bi-gear-fill` Admin Panel |
| Estilo | Vibrante, comercial | Profesional, sobrio |

---

### Versión 1.3.1 (13 de marzo de 2026)

**Mejoras en la Interfaz de Administración:**

- ✅ **Rediseño del layout de productos** - Columnas invertidas
  - Izquierda (col-lg-4): Configuración y Costos
  - Derecha (col-lg-8): Información básica, Precio/Stock, Imágenes
  - Botones de acción movidos a la derecha (debajo de imágenes)

- ✅ **Bug fixes en edición de productos**
  - Precarga correcta de datos de costos (JSON)
  - Precarga de checkboxes (ojos, mano de obra, utilidad)
  - Visualización de imágenes existentes adicionales
  - Validación de precio > 0 antes de guardar
  - Imagen principal opcional en edición

- ✅ **Nuevo formulario `ProductEditForm`**
  - Hereda de `ProductUploadForm`
  - Imagen principal opcional (sin `FileRequired`)
  - Precio permite 0 inicialmente (se calcula)

**Archivos Modificados:**
- ✅ `app/blueprints/admin/forms.py` - Nuevo `ProductEditForm`
- ✅ `app/blueprints/admin/routes.py` - Precarga de costos, validación
- ✅ `app/blueprints/admin/templates/admin/upload_product.html` - Layout invertido
- ✅ `app/blueprints/admin/templates/admin/edit_product.html` - Layout + imágenes existentes

**Mejoras de UX:**
- ✅ Flujo de trabajo más lógico (configuración → información → imágenes)
- ✅ Botones de acción accesibles al final del formulario
- ✅ Vista previa de imágenes existentes en edición
- ✅ Cálculo automático de precios al cargar (JavaScript)

---

### Versión 1.3.0 (13 de marzo de 2026)

**Portfolio con Base de Datos:**
- ✅ Migración de sesión a base de datos SQLite
- ✅ Modelos: `PortfolioInfo` y `PortfolioItem`
- ✅ CRUD completo con SQLAlchemy
- ✅ Persistencia de datos entre reinicios
- ✅ Información del portfolio almacenada en BD (nombre, bio, contacto)
- ✅ Items del portfolio con orden y descripción

**Nuevos Modelos:**
- ✅ `PortfolioInfo` - Información personal del portfolio
  - Campos: name, title, bio, email, phone
  - Método `get_or_create()` para registro único
  - Método `to_dict()` para serialización
- ✅ `PortfolioItem` - Items individuales del portfolio
  - Campos: title, description, image, order, is_active
  - Método `get_all_active()` para obtener items activos
  - Orden configurable por número

**Nuevas Rutas:**
- ✅ `/portfolio/` - Página pública del portfolio
- ✅ `/portfolio/admin` - Dashboard de administración
- ✅ `/portfolio/admin/info` - Editar información personal
- ✅ `/portfolio/admin/items` - Listar items
- ✅ `/portfolio/admin/items/upload` - Subir nuevo item
- ✅ `/portfolio/admin/items/edit/<id>` - Editar item existente
- ✅ `/portfolio/admin/items/delete/<id>` - Eliminar item

**Nuevos Scripts:**
- ✅ `add_portfolio_tables.py` - Migración para crear tablas del portfolio

**Templates Actualizados:**
- ✅ `portfolio/public.html` - Página pública con grid de items
- ✅ `portfolio/admin/dashboard.html` - Panel principal
- ✅ `portfolio/admin/info.html` - Formulario de información
- ✅ `portfolio/admin/items.html` - Lista con editar/eliminar
- ✅ `portfolio/admin/upload.html` - Subida de imágenes
- ✅ `portfolio/admin/edit.html` - Edición de items (NUEVO)

**Mejoras de UX:**
- ✅ Vista previa de imágenes en tiempo real (subida y edición)
- ✅ Mensajes flash para feedback de operaciones
- ✅ Confirmación antes de eliminar
- ✅ Precarga de datos en edición
- ✅ Botones de editar y eliminar en lista de items

**Base de Datos:**
- ✅ Nueva tabla `portfolio_info` (información general)
- ✅ Nueva tabla `portfolio_items` (items individuales)
- ✅ Script de migración `add_portfolio_tables.py`
- ✅ Registro por defecto creado automáticamente

---

### Versión 1.2.0 (11 de marzo de 2026)

**Gestión de Productos (CRUD Completo):**
- ✅ Crear productos con formulario completo (nombre, descripción, precio, stock, SKU)
- ✅ Listar productos en tabla con vista previa de imágenes
- ✅ Editar productos existentes con precarga de datos
- ✅ Eliminar productos con confirmación
- ✅ Generación automática de slug y SKU
- ✅ Cálculo automático de precio basado en costos (calculadora de amigurumis)

**Calculadora de Costos (Amigurumis):**
- ✅ Campos de costos en formulario de subida y edición
- ✅ Cálculo en tiempo real con JavaScript
- ✅ Lana: (costo_rollo / peso_rollo) × peso_usado
- ✅ Relleno: (costo_bolsa / peso_bolsa) × peso_usado
- ✅ Ojos de seguridad (opcional)
- ✅ Mano de obra (opcional): costo_hora × horas
- ✅ Utilidad porcentual (opcional)
- ✅ Precio de venta = Costo total + Utilidad
- ✅ Campo de precio readonly (solo cálculo)
- ✅ Resumen visual de costos en tarjeta

**Gestión de Categorías (CRUD):**
- ✅ Listar categorías ordenadas por ID
- ✅ Crear categorías con nombre, slug, descripción
- ✅ Editar categorías existentes
- ✅ Eliminar categorías (solo si no tienen productos)
- ✅ Validación de slugs únicos
- ✅ Generación automática de slug desde nombre

**Base de Datos:**
- ✅ Nueva columna `costos` (JSON) en tabla products
- ✅ Script `add_costos_column.py` para migración
- ✅ Persistencia de estructura de costos por producto

**Templates Actualizados:**
- ✅ `admin/upload_product.html` - Formulario completo con cálculo automático
- ✅ `admin/edit_product.html` - Edición con precarga de datos y costos
- ✅ `admin/list_products.html` - Tabla con acciones editar/eliminar/ver
- ✅ `admin/list_categories.html` - Gestión de categorías
- ✅ `admin/create_category.html` - Crear categoría
- ✅ `admin/edit_category.html` - Editar categoría
- ✅ `admin/dashboard.html` - Contadores y accesos rápidos

**Scripts Nuevos:**
- ✅ `add_costos_column.py` - Migración de base de datos
- ✅ `clear_sample_products.py` - Limpiar productos de ejemplo
- ✅ `create_admin_quick.py` - Crear admin por línea de comandos
- ✅ `reset_password.py` - Resetear contraseña por email

**Mejoras de UX:**
- ✅ Vista previa de imágenes en tiempo real
- ✅ Toggle de campos opcionales (ojos, mano de obra, utilidad)
- ✅ Mensajes flash para feedback de operaciones
- ✅ Confirmación antes de eliminar
- ✅ Precarga de datos en edición

---

### Versión 1.1.0 (11 de marzo de 2026)

**Calculadora de Costos:**
- ✅ Precio de venta se calcula automáticamente
- ✅ Campo de precio readonly (no editable manualmente)
- ✅ Cálculo basado en: materiales + mano de obra + utilidad
- ✅ Mano de obra opcional (checkbox)
- ✅ Utilidad adicional opcional (checkbox)

**Página de Construcción:**
- ✅ Eliminados botones de acceso a Productos y Portfolio
- ✅ Solo muestra countdown y redes sociales

**Actualizaciones Generales:**
- ✅ Email actualizado a `soralis05@gmail.com` en todo el sitio
- ✅ Año dinámico en footer (2026 o futuro)
- ✅ Coming Soon sin acceso a Admin

**Base de Datos:**
- ✅ Modelos: User, Product, Category, CartItem, Order, OrderItem
- ✅ SQLite para desarrollo y producción (sin dependencias extra)
- ✅ Script `init_db.py` para inicializar con datos de ejemplo

**Autenticación:**
- ✅ Panel de administración protegido (login + rol admin)
- ✅ Login funcional con redirección por rol
- ✅ Registro de usuarios con validaciones

**Tema Visual:**
- ✅ Gradiente morado/azul signature (`#667eea` → `#764ba2`)
- ✅ Navbar, footer y cards con tema personalizado
- ✅ Responsive y moderno

---

*Documento actualizado el 13 de marzo de 2026 - v1.4.0 - Checkout y Carrito Funcional*