@echo off
REM Gestion de Credenciales de Git - GitHub
REM Permite ver, actualizar o eliminar tokens guardados

echo ============================================
echo   Gestion de Credenciales - Git/GitHub
echo ============================================
echo.
echo Tu token de GitHub esta guardado en:
echo %USERPROFILE%\AppData\Local\Git\credentials
echo.
echo Este archivo esta protegido por Windows.
echo.

:MENU
echo ============================================
echo   OPCIONES:
echo ============================================
echo   1. Ver credenciales guardadas (solo URL)
echo   2. Ver archivo de credenciales completo
echo   3. Eliminar credenciales (para cambiar token)
echo   4. Verificar conexion con GitHub
echo   5. Salir
echo.
set /p OPCION="Elige una opcion (1-5): "

if "%OPCION%"=="1" goto VER_URL
if "%OPCION%"=="2" goto VER_COMPLETO
if "%OPCION%"=="3" goto ELIMINAR
if "%OPCION%"=="4" goto VERIFICAR
if "%OPCION%"=="5" goto SALIR
echo Opcion no valida. Intenta de nuevo.
goto MENU

:VER_URL
echo.
echo Credenciales configuradas para:
findstr /C:"host=github.com" "%USERPROFILE%\AppData\Local\Git\credentials" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   - github.com (Token de desarrollo configurado)
    echo.
    echo   El token esta oculto por seguridad.
) else (
    echo   - No hay credenciales de GitHub guardadas
)
echo.
pause
cls
goto MENU

:VER_COMPLETO
echo.
echo ADVERTENCIA: Esto mostrara tu token en texto plano.
echo Asegurate de que nadie este mirando tu pantalla.
echo.
pause
echo.
echo Contenido del archivo:
type "%USERPROFILE%\AppData\Local\Git\credentials" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo No se encontro el archivo de credenciales.
)
echo.
echo ============================================
echo   IMPORTANTE: Si compartiste esta salida,
echo   tu token quedo expuesto. Cambialo en:
echo   https://github.com/settings/tokens
echo ============================================
echo.
pause
cls
goto MENU

:ELIMINAR
echo.
echo Esto eliminara el token guardado.
echo Tendras que volver a ingresarlo la proxima vez
echo que hagas push.
echo.
set /p CONFIRM="¿Estas seguro? (S/N): "
if /i not "%CONFIRM%"=="S" goto MENU

del "%USERPROFILE%\AppData\Local\Git\credentials" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Credenciales eliminadas exitosamente.
    echo La proxima vez que hagas "git push", Git te pedira el token.
) else (
    echo.
    echo No se encontraron credenciales para eliminar.
)
echo.
pause
cls
goto MENU

:VERIFICAR
echo.
echo Verificando conexion con GitHub...
echo.
"C:\Program Files\Git\bin\git.exe" remote -v
echo.
echo Probando autenticacion...
"C:\Program Files\Git\bin\git.exe" ls-remote --heads origin >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Conexion exitosa con GitHub
    echo   Tu token de desarrollo es valido.
) else (
    echo   [ERROR] No se pudo conectar con GitHub
    echo   Posibles causas:
    echo   - Token expirado o invalido
    echo   - Sin conexion a internet
    echo   - El repositorio no existe o es privado
)
echo.
pause
cls
goto MENU

:SALIR
echo.
echo ¡Hasta luego!
echo.
timeout /t 2 >nul
