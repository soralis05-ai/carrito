@echo off
REM Script para configurar GitHub con tokens de acceso
REM Ejecutar después de crear el repositorio en GitHub

echo ============================================
echo   Configuracion de GitHub - Almapunt
echo ============================================
echo.

REM Verificar si se proporcionó la URL del repositorio
if "%~1"=="" (
    echo Error: Debes proporcionar la URL del repositorio
    echo.
    echo Uso: setup-github.bat ^<URL_DEL_REPOSITORIO^>
    echo.
    echo Ejemplo:
    echo   setup-github.bat https://github.com/tu-usuario/almapunt.git
    echo.
    pause
    exit /b 1
)

set GIT_URL=%~1
set GIT_BIN=C:\Program Files\Git\bin\git.exe

echo [1/4] Configurando credenciales...
echo.

REM Pedir token de desarrollo
set /p DEV_TOKEN="Ingresa tu token de DESARROLLO (lectura/escritura): "
if "%DEV_TOKEN%"=="" (
    echo Error: El token es requerido
    pause
    exit /b 1
)

REM Extraer nombre de usuario de la URL
for /f "tokens=4 delims=/" %%a in ("%GIT_URL%") do set GITHUB_USER=%%a

REM Configurar credencial de desarrollo
echo Configurando token para %GITHUB_USER%...
echo %GIT_BIN% credential-store store
echo protocol=https > "%TEMP%\git-creds"
echo host=github.com >> "%TEMP%\git-creds"
echo username=%GITHUB_USER% >> "%TEMP%\git-creds"
echo password=%DEV_TOKEN% >> "%TEMP%\git-creds"

REM Usar credential manager de Git
"%GIT_BIN%" config --global credential.helper store
type "%TEMP%\git-creds" | "%GIT_BIN%" credential approve

echo.
echo [2/4] Agregando remoto origin...
"%GIT_BIN%" remote add origin %GIT_URL%

echo.
echo [3/4] Creando primer commit...
"%GIT_BIN%" add .
"%GIT_BIN%" commit -m "Initial commit: Almapunt e-commerce con portfolio"

echo.
echo [4/4] Subiendo a GitHub (rama main)...
"%GIT_BIN%" branch -M main
"%GIT_BIN%" push -u origin main

echo.
echo ============================================
echo   !Configuracion completada exitosamente!
echo ============================================
echo.
echo Tu repositorio esta disponible en:
echo %GIT_URL%
echo.
echo Para futuras operaciones:
echo   - git pull (descargar cambios)
echo   - git push (subir cambios)
echo   - git status (ver estado)
echo.
echo NOTA: Guarda tu token en un lugar seguro.
echo       Para produccion, configura el token de solo lectura
echo       en las variables de entorno de tu servidor.
echo.
pause
