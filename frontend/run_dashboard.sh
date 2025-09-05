#!/bin/bash

echo "Iniciando Dashboard de Dengue - Streamlit"
echo "========================================"
echo

echo "Verificando que el backend esté corriendo..."
if ! curl -s http://localhost:8000/laboratorio-dengue/kpis > /dev/null 2>&1; then
    echo "ERROR: El backend no está disponible en http://localhost:8000"
    echo "Por favor, asegúrese de que el backend esté corriendo antes de continuar."
    echo
    echo "Para iniciar el backend:"
    echo "  cd backend"
    echo "  python main.py"
    echo
    read -p "Presiona Enter para continuar..."
    exit 1
fi

echo "Backend disponible ✓"
echo

echo "Instalando dependencias si es necesario..."
pip install -r requirements.txt > /dev/null 2>&1

echo
echo "Iniciando Streamlit Dashboard..."
echo "El dashboard estará disponible en: http://localhost:8501"
echo
echo "Presiona Ctrl+C para detener el servidor"
echo

streamlit run streamlit_app.py
