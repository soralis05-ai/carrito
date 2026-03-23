# 📘 Configuración de MySQL para Desarrollo

## Requisitos Previos

- ✅ MySQL Community Server 8.0+ instalado
- ✅ MySQL Workbench instalado
- ✅ Python 3.14+
- ✅ Dependencias instaladas (`pip install -r requirements.txt`)

---

## Paso 1: Instalar MySQL Community Server

### Opción A: Usando winget (Recomendado)

```powershell
# Abrir PowerShell como Administrador
winget install Oracle.MySQL -e
winget install Oracle.MySQLWorkbench -e
```

### Opción B: Manual

1. **Descargar:** https://dev.mysql.com/downloads/installer/
2. **Seleccionar:** `MySQL Installer for Windows`
3. **Tipo:** Development Machine
4. **Componentes:**
   - ✅ MySQL Server 8.0.x
   - ✅ MySQL Workbench 8.0.x

---

## Paso 2: Configurar MySQL

### Durante la Instalación

| Configuración | Valor |
|---------------|-------|
| **Tipo de Setup** | Development Machine |
| **Puerto** | 3306 |
| **Root Password** | `root123` (anotalo) |
| **Windows Service** | ✅ Iniciar automáticamente |

### Crear Base de Datos

**Opción A: MySQL Workbench (GUI)**

1. Abrir MySQL Workbench
2. Conexión: `Local instance MySQL80`
3. Password: el que configuraste
4. Ejecutar:
```sql
CREATE DATABASE almapunt_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Opción B: Command Line**

```bash
mysql -u root -p
# Ingresar password

CREATE DATABASE almapunt_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

---

## Paso 3: Configurar Proyecto

### Crear archivo `.env`

Copiá `.env.example` a `.env` en la raíz del proyecto:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# O manualmente: crear .env con:
MYSQL_USER=root
MYSQL_PASSWORD=root123
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=almapunt_dev
SECRET_KEY=devkey-secret-change-in-production
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Paso 4: Inicializar Base de Datos

### Opción A: Script automático

```bash
python scripts/init_mysql.py
```

### Opción B: Manual

```bash
# 1. Crear database (ver Paso 2)
# 2. Ejecutar migraciones
flask db upgrade
# O si no usas Flask-Migrate:
python scripts/init_db.py
```

---

## Paso 5: Crear Administrador

```bash
python scripts/create_admin.py
```

**Credenciales:**
```
Username: SorayaR
Email: soralis05@gmail.com
Password: Soraya79@
```

---

## Paso 6: Iniciar Aplicación

```bash
python run.py
```

**Acceder:**
- Público: http://127.0.0.1:5000/
- Admin: http://127.0.0.1:5000/admin/

---

## 🔧 Troubleshooting

### Error: "Can't connect to MySQL server"

**Verificar servicio:**
```powershell
Get-Service -Name MySQL*
Start-Service MySQL80  # O el nombre de tu servicio
```

**Verificar puerto:**
```bash
netstat -an | findstr 3306
```

### Error: "Access denied for user 'root'"

1. Verificar password en `.env`
2. Resetear password:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'nuevo_password';
FLUSH PRIVILEGES;
```

### Error: "Unknown database"

```sql
-- Verificar databases existentes
SHOW DATABASES;

-- Crear si no existe
CREATE DATABASE almapunt_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 📊 Verificar Conexión

**Desde Python:**
```python
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root123',
    database='almapunt_dev'
)
print("✅ Conexión exitosa")
conn.close()
```

**Desde Workbench:**
1. Abrir MySQL Workbench
2. Click en conexión local
3. Ejecutar: `USE almapunt_dev; SELECT 1;`

---

## 🔄 Volver a SQLite (Opcional)

Si querés usar SQLite en lugar de MySQL:

**`.env`:**
```bash
DATABASE_URL=sqlite:///app.db
```

**Reiniciar app:**
```bash
python run.py
```

---

**Última actualización:** 23 de marzo de 2026
**Versión:** 3.0.16
