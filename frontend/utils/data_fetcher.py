import streamlit as st
import requests
import pandas as pd
import logging

logger = logging.getLogger(__name__)

@st.cache_data(ttl=300)
def fetch_data():
    try:
        backend_url = "http://localhost:8000"
        response = requests.get(f"{backend_url}/laboratorio-dengue/procesados", timeout=30)
        response.raise_for_status()
        
        data = response.json()
        if not data or len(data) == 0:
            st.warning("No hay datos disponibles en la API")
            return None
        
        logger.info(f"Datos obtenidos exitosamente: {len(data)} registros")
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error conectando al backend: {e}")
        return None

@st.cache_data(ttl=300)
def fetch_dengue_data():
    """Función para obtener datos de dengue del backend y preprocesarlos"""
    try:
        # Obtener datos raw del backend
        data = fetch_data()
        if data is None:
            return None
        
        # Convertir a DataFrame
        df = pd.DataFrame(data)
        
        # Limpiar y preparar los datos
        df = clean_data_original_style(df)
        
        logger.info(f"Datos procesados exitosamente: {len(df)} registros")
        return df
        
    except Exception as e:
        logger.error(f"Error procesando datos de dengue: {str(e)}")
        st.error(f"Error procesando datos: {str(e)}")
        return None

def clean_data_original_style(df):
    columnas_no_dengue = ['rt_pcr_chik', 'rt_pcr_tiempo_real_yf', 'igm_chik', 'rt_pcr_tiempo_real_zika']
    
    for col in columnas_no_dengue:
        if col in df.columns:
            df = df.drop(columns=[col])
    if 'edad' in df.columns:
        df['edad'] = pd.to_numeric(df['edad'], errors='coerce').fillna(0).astype(int)
        df['edad'] = df['edad'].clip(0, 100)
    
    if 'dias_evolucion' in df.columns:
        df['dias_evolucion'] = pd.to_numeric(df['dias_evolucion'], errors='coerce').fillna(0).astype(int)
    for col in ['fecha_recepcion', 'fecha_procesamiento']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%Y-%m-%d', errors='coerce')
    if 'fecha_procesamiento' in df.columns and 'fecha_recepcion' in df.columns:
        delta = df['fecha_procesamiento'] - df['fecha_recepcion']
        df['demora_dias'] = delta.dt.total_seconds() / 86400
        df['demora_horas'] = delta.dt.total_seconds() / 3600
        df = df[df['demora_dias'].notna() & (df['demora_dias'] >= 0)]
    if 'fecha_recepcion' in df.columns:
        df['anio_recepcion'] = df['fecha_recepcion'].dt.year
        df['mes_recepcion'] = df['fecha_recepcion'].dt.month
        df['mes_anio_recepcion'] = df['fecha_recepcion'].dt.to_period('M').astype(str)
        df['sem_epid_recepcion'] = df['fecha_recepcion'].dt.isocalendar().week
    if 'edad' in df.columns:
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 100]
        labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']
        df['grupo_etario'] = pd.cut(df['edad'], bins=bins, labels=labels, right=False)
    if 'localidad_normalizada' in df.columns:
        df['localidad_agrupada'] = df['localidad_normalizada']
    
    return df
