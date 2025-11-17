#!/bin/bash

echo "===================================="
echo "  Universidad Fit - Servidor Django"
echo "===================================="
echo ""

cd "$(dirname "$0")"

echo "Verificando entorno..."
python3 --version
echo ""

echo "Iniciando servidor de desarrollo..."
echo ""
echo "Abre tu navegador en: http://127.0.0.1:8000/"
echo "Presiona Ctrl+C para detener el servidor"
echo ""

python3 manage.py runserver

