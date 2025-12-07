@echo off
echo ========================================
echo DOCENTIA - CREAR ESTRUCTURA FRONTEND
echo ========================================
echo.

REM Verificar que estamos en la carpeta del proyecto
if not exist "venv" (
    echo ERROR: No se encuentra la carpeta 'venv'
    echo Por favor, ejecuta este script desde: C:\Users\PC\Proyectos\DocentIA
    pause
    exit /b 1
)

echo Creando estructura de carpetas...
echo.

REM Crear carpeta principal
if not exist "frontend" mkdir frontend
echo [OK] frontend/

REM Crear subcarpetas
if not exist "frontend\generadores" mkdir frontend\generadores
echo [OK] frontend\generadores/

if not exist "frontend\assets" mkdir frontend\assets
echo [OK] frontend\assets/

if not exist "frontend\assets\css" mkdir frontend\assets\css
echo [OK] frontend\assets\css/

if not exist "frontend\assets\js" mkdir frontend\assets\js
echo [OK] frontend\assets\js/

if not exist "frontend\assets\images" mkdir frontend\assets\images
echo [OK] frontend\assets\images/

echo.
echo ========================================
echo ESTRUCTURA CREADA EXITOSAMENTE
echo ========================================
echo.
echo Ahora copia los archivos descargados a:
echo.
echo   frontend\
echo   - index.html
echo   - README.md
echo.
echo   frontend\generadores\
echo   - boton-emergencia.html
echo   - problemas-matematicas.html
echo.
echo   frontend\assets\css\
echo   - common.css
echo.
echo   frontend\assets\js\
echo   - common.js
echo   - boton-emergencia.js
echo   - problemas-matematicas.js
echo.
echo ========================================
pause
