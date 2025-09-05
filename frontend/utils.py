"""
Utilidades para el dashboard de Streamlit
Funciones auxiliares para manejo de datos y configuración
"""

import streamlit as st
import pandas as pd
import requests
import logging
from typing import Optional, Dict, Any
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class BackendClient:
    """Cliente para comunicación con el backend FastAPI"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.timeout = 30
        
    def health_check(self) -> bool:
        """Verificar si el backend está disponible"""
        try:
            response = requests.get(f"{self.base_url}/laboratorio-dengue/kpis", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_data(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Obtener datos de un endpoint específico"""
        try:
            url = f"{self.base_url}/laboratorio-dengue/{endpoint}"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching from {endpoint}: {e}")
            return None
    
    def get_processed_data(self) -> Optional[pd.DataFrame]:
        """Obtener datos procesados como DataFrame"""
        data = self.get_data('procesados')
        if data:
            try:
                return pd.DataFrame(data)
            except Exception as e:
                logger.error(f"Error converting to DataFrame: {e}")
        return None
    
    def get_kpis(self) -> Optional[Dict[str, Any]]:
        """Obtener KPIs del backend"""
        return self.get_data('kpis')

def check_required_columns(df: pd.DataFrame, required_columns: list) -> list:
    """Verificar que el DataFrame tenga las columnas requeridas"""
    missing = [col for col in required_columns if col not in df.columns]
    return missing

def safe_numeric_conversion(df: pd.DataFrame, column: str, default_value: float = 0.0) -> pd.Series:
    """Conversión segura a numérico con valor por defecto"""
    try:
        return pd.to_numeric(df[column], errors='coerce').fillna(default_value)
    except Exception as e:
        logger.warning(f"Error converting {column} to numeric: {e}")
        return pd.Series([default_value] * len(df))

def safe_date_conversion(df: pd.DataFrame, column: str) -> pd.Series:
    """Conversión segura a fecha"""
    try:
        return pd.to_datetime(df[column], errors='coerce')
    except Exception as e:
        logger.warning(f"Error converting {column} to datetime: {e}")
        return pd.Series([pd.NaT] * len(df))

def create_age_groups_safe(ages: pd.Series) -> pd.Series:
    """Crear grupos etarios de forma segura"""
    try:
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 100]
        labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']
        return pd.cut(ages, bins=bins, labels=labels, right=False)
    except Exception as e:
        logger.warning(f"Error creating age groups: {e}")
        return pd.Series(['0-10'] * len(ages))

def format_number(number: float, decimals: int = 0) -> str:
    """Formatear número con separadores de miles"""
    try:
        if pd.isna(number):
            return "N/A"
        if decimals == 0:
            return f"{int(number):,}"
        else:
            return f"{number:,.{decimals}f}"
    except:
        return "N/A"

def format_percentage(value: float, total: float, decimals: int = 1) -> str:
    """Formatear como porcentaje"""
    try:
        if total == 0 or pd.isna(value) or pd.isna(total):
            return "0.0%"
        percentage = (value / total) * 100
        return f"{percentage:.{decimals}f}%"
    except:
        return "0.0%"

def create_download_link(df: pd.DataFrame, filename: str, link_text: str = "Descargar datos") -> str:
    """Crear enlace de descarga para DataFrame"""
    try:
        csv = df.to_csv(index=False)
        return st.download_button(
            label=link_text,
            data=csv,
            file_name=filename,
            mime='text/csv'
        )
    except Exception as e:
        logger.error(f"Error creating download link: {e}")
        return ""

def display_error_message(error_type: str, details: str = None):
    """Mostrar mensaje de error estandarizado"""
    error_messages = {
        'backend_connection': {
            'title': '🔌 Error de Conexión con el Backend',
            'message': 'No se pudo conectar con el servidor de datos. Verifique que el backend esté ejecutándose.',
            'suggestions': [
                'Verificar que el backend esté corriendo en http://localhost:8000',
                'Revisar la configuración de BACKEND_URL en el código',
                'Comprobar que no haya problemas de firewall o red'
            ]
        },
        'no_data': {
            'title': ' Sin Datos Disponibles',
            'message': 'No hay datos disponibles con los filtros seleccionados.',
            'suggestions': [
                'Ampliar el rango de fechas',
                'Seleccionar "Todas" en los filtros de localidad/departamento',
                'Verificar que haya datos cargados en la base de datos'
            ]
        },
        'data_processing': {
            'title': ' Error de Procesamiento',
            'message': 'Ocurrió un error al procesar los datos.',
            'suggestions': [
                'Intentar recargar la página',
                'Verificar la calidad de los datos en el backend',
                'Contactar al administrador del sistema'
            ]
        }
    }
    
    error_info = error_messages.get(error_type, {
        'title': '❌ Error Desconocido',
        'message': 'Se produjo un error inesperado.',
        'suggestions': ['Contactar al soporte técnico']
    })
    
    st.error(f"**{error_info['title']}**")
    st.write(error_info['message'])
    
    if details:
        with st.expander("Ver detalles técnicos"):
            st.code(details)
    
    st.write("**Posibles soluciones:**")
    for suggestion in error_info['suggestions']:
        st.write(f"• {suggestion}")

def show_data_summary(df: pd.DataFrame):
    """Mostrar resumen de datos cargados"""
    if df is not None and len(df) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Registros", format_number(len(df)))
        
        with col2:
            if 'fecha_recepcion' in df.columns:
                date_range = (df['fecha_recepcion'].max() - df['fecha_recepcion'].min()).days
                st.metric("Período (días)", format_number(date_range))
        
        with col3:
            if 'localidad_normalizada' in df.columns:
                unique_locations = df['localidad_normalizada'].nunique()
                st.metric("Localidades", format_number(unique_locations))
        
        with col4:
            if 'establecimiento_notificador_normalizada' in df.columns:
                unique_establishments = df['establecimiento_notificador_normalizada'].nunique()
                st.metric("Establecimientos", format_number(unique_establishments))

@st.cache_data
def get_filter_options(df: pd.DataFrame) -> Dict[str, list]:
    """Obtener opciones para filtros (con cache)"""
    options = {}
    
    # Localidades
    if 'localidad_normalizada' in df.columns:
        options['localidades'] = ['Todas'] + sorted(df['localidad_normalizada'].dropna().unique().tolist())
    
    # Departamentos
    if 'departamento_normalizado' in df.columns:
        options['departamentos'] = ['Todos'] + sorted(df['departamento_normalizado'].dropna().unique().tolist())
    
    # Grupos etarios
    if 'grupo_etario' in df.columns:
        options['grupos_etarios'] = ['Todos'] + sorted(df['grupo_etario'].dropna().astype(str).unique().tolist())
    
    return options

def validate_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """Validar calidad de datos y retornar reporte"""
    report = {
        'total_rows': len(df),
        'columns': df.columns.tolist(),
        'missing_data': {},
        'data_types': {},
        'quality_issues': []
    }
    
    # Revisar datos faltantes
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        missing_percent = (missing_count / len(df)) * 100
        report['missing_data'][col] = {
            'count': missing_count,
            'percentage': missing_percent
        }
        
        if missing_percent > 50:
            report['quality_issues'].append(f"Columna '{col}' tiene {missing_percent:.1f}% de datos faltantes")
    
    # Revisar tipos de datos
    for col in df.columns:
        report['data_types'][col] = str(df[col].dtype)
    
    return report

def create_performance_info():
    """Mostrar información de rendimiento"""
    with st.sidebar:
        st.markdown("---")
        st.subheader("ℹ️ Información del Sistema")
        
        # Información de cache
        cache_info = st.cache_data.get_stats()
        if cache_info:
            st.write(f"**Cache hits:** {cache_info[0].cache_hits}")
            st.write(f"**Cache misses:** {cache_info[0].cache_misses}")
        
        # Timestamp
        st.write(f"**Última carga:** {datetime.now().strftime('%H:%M:%S')}")
        
        # Botón para limpiar cache
        if st.button("🔄 Limpiar Cache"):
            st.cache_data.clear()
            st.rerun()
