@echo off
echo ====================================
echo   Universidad Fit - Servidor Django
echo ====================================
echo.

cd /d "%~dp0"

echo Verificando entorno...
python --version
echo.

echo Iniciando servidor de desarrollo...
echo.
echo Abre tu navegador en: http://127.0.0.1:8000/
echo Presiona Ctrl+C para detener el servidor
echo.

python manage.py runserver

pause

