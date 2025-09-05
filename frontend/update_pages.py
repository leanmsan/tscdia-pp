#!/usr/bin/env python3
"""
Script para actualizar todas las páginas para usar navegación nativa de Streamlit
"""

import os
import re

def update_page_file(filepath, page_title, page_icon):
    """Actualizar un archivo de página individual"""
    
    print(f"Actualizando {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar el nombre de la función principal
    function_match = re.search(r'def (show_\w+_page)', content)
    if not function_match:
        print(f"No se encontró función show_*_page en {filepath}")
        return
    
    function_name = function_match.group(1)
    
    # Reemplazar imports
    new_imports = '''"""
Página de {title} - Simple
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_fetcher import fetch_dengue_data
from shared_filters import FilterManager

# Configuración de la página
st.set_page_config(
    page_title="{title}",
    page_icon="{icon}",
    layout="wide"
)

def main():
    """Función principal de la página"""
    
    st.title("{icon} {title}")
    
    # Obtener datos
    try:
        df = fetch_dengue_data()
        if df is None or len(df) == 0:
            st.error("No se pudieron obtener datos del backend")
            return
        
        # Crear filtros en sidebar
        filter_manager = FilterManager()
        with st.sidebar:
            filters = filter_manager.create_sidebar_filters(df)
        
        df_filtered = filter_manager.apply_filters(df, filters)
        
        {function_name}(df_filtered)
        
    except Exception as e:
        st.error(f"Error: {{str(e)}}")

'''.format(title=page_title, icon=page_icon, function_name=function_name)
    
    # Encontrar donde termina la función
    pattern = r'"""[^"]*"""\s*import.*?from shared_filters.*?\n\ndef ' + function_name
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # Reemplazar la parte inicial
        content = new_imports + content[match.end()-len(function_name)-4:]
        
        # Reemplazar las llamadas a create_page_header y show_no_data_message
        content = re.sub(r'\s*create_page_header\([^)]+\)\s*', '\n    ', content)
        content = re.sub(r'\s*show_no_data_message\(\)\s*', '        st.warning(" No hay datos disponibles con los filtros seleccionados")', content)
        
        # Agregar main() al final si no existe
        if 'if __name__ == "__main__":' not in content:
            content += '\n\nif __name__ == "__main__":\n    main()'
        
        # Escribir el archivo actualizado
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Actualizado {filepath}")
    else:
        print(f"❌ No se pudo actualizar {filepath} - patrón no encontrado")

# Páginas a actualizar
pages_to_update = [
    ("geographic.py", "Análisis Geográfico", ""),
    ("laboratory.py", "Análisis de Laboratorio", "🔬"), 
    ("temporal.py", "Análisis Temporal", ""),
    ("dashboard.py", "Dashboard Completo", "")
]

# Actualizar cada página
pages_dir = "pages"
for filename, title, icon in pages_to_update:
    filepath = os.path.join(pages_dir, filename)
    if os.path.exists(filepath):
        update_page_file(filepath, title, icon)
    else:
        print(f" Archivo no encontrado: {filepath}")

print("\n🎉 ¡Actualización completada!")
