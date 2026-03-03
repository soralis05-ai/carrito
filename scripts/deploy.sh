#!/bin/bash
# Script de actualización para producción (Hetzner/Debian)
# Uso: ./deploy.sh

echo "============================================"
echo "  Actualizacion - Almapunt Carrito"
echo "============================================"
echo ""

# Detener la aplicación si está corriendo
echo "[1/5] Deteniendo aplicacion..."
pkill -f "python.*run.py" 2>/dev/null || true
pkill -f "waitress" 2>/dev/null || true
sleep 2

# Pull de cambios
echo "[2/5] Descargando cambios de GitHub..."
git pull origin main
if [ $? -ne 0 ]; then
    echo "[ERROR] No se pudo descargar los cambios"
    exit 1
fi

# Instalar dependencias
echo "[3/5] Instalando dependencias..."
source .venv/bin/activate
pip install -r requirements.txt --quiet

# Migrar base de datos (si hay nuevos modelos)
echo "[4/5] Verificando base de datos..."
python scripts/init_db.py 2>/dev/null || echo "[OK] DB verificada"

# Iniciar aplicación
echo "[5/5] Iniciando aplicacion..."
nohup waitress-serve --host=0.0.0.0 --port=5000 run:app > app.log 2>&1 &
sleep 3

# Verificar
if pgrep -f "waitress" > /dev/null; then
    echo ""
    echo "============================================"
    echo "  [EXITO] Actualizacion completada"
    echo "============================================"
    echo "  Servidor corriendo en puerto 5000"
    echo "  Logs: tail -f app.log"
    echo "============================================"
else
    echo ""
    echo "============================================"
    echo "  [ERROR] No se pudo iniciar el servidor"
    echo "  Revisa los logs: tail -f app.log"
    echo "============================================"
    exit 1
fi
