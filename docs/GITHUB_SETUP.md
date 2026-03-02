# 🚀 Guía de Configuración con GitHub

## ✅ Lo que ya está hecho

- [x] Git instalado en `C:\Program Files\Git\bin\git.exe`
- [x] Git agregado al PATH de usuario
- [x] Repositorio local inicializado
- [x] Primer commit creado (96 archivos)
- [x] `.gitignore` configurado para Python/Flask
- [x] `.env.example` creado como plantilla

---

## 📋 Pasos para conectar con GitHub

### Paso 1: Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `almapunt` (o el que prefieras)
3. Descripción: "E-commerce artesanal con portfolio personal"
4. **NO** marques "Initialize this repository with a README" (ya tenemos uno)
5. Haz clic en **Create repository**

### Paso 2: Copiar la URL del repositorio

Después de crear el repositorio, GitHub te mostrará algo como:
```
https://github.com/TU-USUARIO/almapunt.git
```

Copia esa URL.

### Paso 3: Ejecutar script de configuración

1. Abre una **nueva** terminal (para que recargue el PATH)
2. Navega al proyecto:
   ```cmd
   cd c:\soraya\carrito
   ```

3. Ejecuta el script con tu URL:
   ```cmd
   scripts\setup-github.bat https://github.com/TU-USUARIO/almapunt.git
   ```

4. Cuando te pida el token:
   - Pega tu **token de DESARROLLO** (lectura/escritura)
   - El token no se mostrará mientras escribes (es normal)

### Paso 4: Verificar

El script hará:
- Configurar tus credenciales
- Agregar el remoto `origin`
- Hacer commit inicial
- Subir a GitHub en la rama `main`

Al finalizar, verás:
```
!Configuracion completada exitosamente!
Tu repositorio esta disponible en:
https://github.com/TU-USUARIO/almapunt.git
```

---

## 🔐 Gestión de Tokens

### Token de Desarrollo (lectura/escritura)
- **Uso:** Para subir cambios desde tu computadora
- **Permisos necesarios:**
  - `repo` (Full control of private repositories)
  - `workflow` (Update GitHub Action workflows)
- **Configurado en:** Tu computadora local

### Token de Producción (solo lectura)
- **Uso:** Para desplegar en servidor (Vercel, Railway, etc.)
- **Permisos necesarios:**
  - `public_repo` (Access public repositories)
- **Configurado en:** Variables de entorno del servidor

### Crear nuevo token (si es necesario)

1. Ve a https://github.com/settings/tokens
2. Haz clic en **Generate new token (classic)**
3. Pon un nombre: `almapunt-dev` o `almapunt-prod`
4. Selecciona los permisos según el uso
5. Haz clic en **Generate token**
6. **Copia el token inmediatamente** (no se vuelve a mostrar)

---

## 📝 Comandos Git Útiles

### Diario
```cmd
# Ver estado de archivos
git status

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Descripción del cambio"

# Subir cambios a GitHub
git push

# Bajar cambios de GitHub
git pull
```

### Ver historial
```cmd
# Ver últimos commits
git log --oneline

# Ver cambios sin subir
git status

# Ver diferencias
git diff
```

### Ramas
```cmd
# Crear nueva rama
git checkout -b nombre-rama

# Cambiar de rama
git checkout nombre-rama

# Ver ramas
git branch

# Fusionar rama
git merge nombre-rama
```

---

## ⚠️ Archivos que NO se suben a GitHub

El `.gitignore` excluye:
- `.env` - Variables de entorno con secretos
- `.venv/` - Entorno virtual de Python
- `__pycache__/` - Archivos compilados de Python
- `*.db` - Base de datos SQLite
- `app/static/img/productos/*.jpg` - Imágenes originales (solo las procesadas)
- `app/static/img/portfolio/*.webp` - Imágenes del portfolio

**Importante:** Si necesitas compartir el proyecto:
1. Copia `.env.example` a `.env`
2. Edita `.env` con tus valores reales
3. Nunca compartas tu `.env` real

---

## 🔄 Flujo de Trabajo Recomendado

### Al empezar a trabajar:
```cmd
git pull origin main
```

### Al terminar una funcionalidad:
```cmd
git add .
git commit -m "Descripción clara del cambio"
git push origin main
```

### Para una nueva característica:
```cmd
# Crear rama para la feature
git checkout -b feature/nueva-funcionalidad

# Trabajar y hacer commits
git add .
git commit -m "Avance de la funcionalidad"

# Subir rama
git push origin feature/nueva-funcionalidad

# Crear Pull Request en GitHub
# Fusionar a main desde la UI de GitHub
```

---

## 🛠️ Solución de Problemas

### "Git no se reconoce como comando"
- Cierra y abre una nueva terminal
- O usa la ruta completa: `"C:\Program Files\Git\bin\git.exe"`

### "Permission denied" al hacer push
- Tu token expiró o no tiene permisos
- Genera uno nuevo en GitHub Settings > Developer settings > Personal access tokens

### "Conflictos de merge"
```cmd
# Ver archivos en conflicto
git status

# Editar archivos y resolver conflictos
# Buscar <<<<<<< y ======= y >>>>>>>

# Marcar como resuelto
git add archivo-en-conflicto.py

# Continuar merge
git commit
```

### "Olvidé hacer commit de algo"
```cmd
# Si fue el último commit
git commit --amend -m "Nuevo mensaje con lo olvidado"

# Si fueron varios commits atrás
git add archivo-olvidado.py
git commit --fixup HEAD~2  # Ajusta el número
git rebase -i --autosquash HEAD~3
```

---

## 📞 Soporte

Si tienes problemas:
1. Revisa esta guía
2. Verifica que el token sea correcto
3. Asegúrate de tener permisos en el repositorio
4. Revisa la consola de errores de Git

---

*Última actualización: 28 de febrero de 2024*
