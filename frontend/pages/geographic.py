"""
Página de Análisi    try:
        df = fetch_dengue_data()
        if df is None or len(df) == 0:
            st.error("No se pudieron obtener datos del backend")
            return
        
        st.info(f" Analizando {len(df):,} registros totales")
        
        show_geographic_analysis(df) Solo gráficos del análisis original
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.data_fetcher import fetch_dengue_data

# Configuración de la página
st.set_page_config(
    page_title="Análisis Geográfico",
    page_icon="",
    layout="wide"
)

def main():
    """Función principal de la página"""
    
    st.title("Análisis Geográfico")
    
    # Obtener datos
    try:
        df = fetch_dengue_data()
        if df is None or len(df) == 0:
            st.error("No se pudieron obtener datos del backend")
            return
        
        st.info(f"Analizando {len(df):,} registros totales")
        
        show_geographic_page(df)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

def show_geographic_page(df: pd.DataFrame):
    """Análisis geográfico basado exactamente en el script original"""
    
    if len(df) == 0:
        st.warning(" No hay datos disponibles con los filtros seleccionados")
        return
    
    # GRÁFICO 1: Top 20 Localidades más frecuentes (EXACTO del análisis original)
    if 'localidad_normalizada' in df.columns:
        st.subheader("🏘️ Top 20 Localidades más Frecuentes")
        
        # Agrupar localidades como en el análisis original
        df_geo = df.copy()
        df_geo['localidad_agrupada'] = df_geo['localidad_normalizada']
        
        top_localidades = df_geo['localidad_agrupada'].value_counts().head(20)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de barras horizontales como en el análisis original
            fig = px.bar(
                x=top_localidades.values,
                y=top_localidades.index,
                orientation='h',
                title='Top 20 Localidades más Frecuentes (Agrupado)',
                color=top_localidades.values,
                color_continuous_scale='viridis'
            )
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False,
                height=600
            )
            
            # Añadir etiquetas de valor como en el análisis original
            for i, (idx, val) in enumerate(top_localidades.items()):
                fig.add_annotation(
                    x=val + val*0.02,
                    y=i,
                    text=str(val),
                    showarrow=False,
                    font=dict(size=10, color="black")
                )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Estadísticas geográficas
            st.subheader("Estadísticas Geográficas")
            
            total_casos = len(df)
            total_localidades = df_geo['localidad_agrupada'].nunique()
            
            st.metric("Total Localidades", total_localidades)
            st.metric("Total Casos", f"{total_casos:,}")
            
            # Concentración en principales localidades
            concentracion_top5 = (top_localidades.head(5).sum() / total_casos) * 100
            concentracion_top10 = (top_localidades.head(10).sum() / total_casos) * 100
            
            st.metric("Concentración Top 5", f"{concentracion_top5:.1f}%")
            st.metric("Concentración Top 10", f"{concentracion_top10:.1f}%")
            
            # Localidad principal
            if len(top_localidades) > 0:
                localidad_principal = top_localidades.index[0]
                casos_principal = top_localidades.iloc[0]
                porcentaje_principal = (casos_principal / total_casos) * 100
                
                st.info(f"""
                **Localidad Principal:**
                
                **{localidad_principal}** concentra {casos_principal:,} casos 
                ({porcentaje_principal:.1f}% del total)
                """)
    
    # GRÁFICO 2: Top 10 Establecimientos Notificadores (EXACTO del análisis original)  
    if 'establecimiento_notificador_normalizada' in df.columns:
        st.subheader("🏥 Top 10 Establecimientos con Más Notificaciones")
        
        top_establecimientos = df.groupby('establecimiento_notificador_normalizada').size().nlargest(10)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de barras horizontales como en el análisis original
            fig = px.bar(
                x=top_establecimientos.values,
                y=top_establecimientos.index,
                orientation='h',
                title='Top 10 Establecimientos con Más Notificaciones de Dengue',
                color_discrete_sequence=['#3498db']
            )
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                height=500
            )
            
            # Añadir etiquetas de valor como en el análisis original
            for i, (idx, val) in enumerate(top_establecimientos.items()):
                fig.add_annotation(
                    x=val + val*0.02,
                    y=i,
                    text=str(val),
                    showarrow=False,
                    font=dict(size=10, color="black")
                )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Estadísticas de establecimientos
            st.subheader("Estadísticas de Establecimientos")
            
            total_establecimientos = df['establecimiento_notificador_normalizada'].nunique()
            st.metric("Total Establecimientos", total_establecimientos)
            
            # Concentración en principales establecimientos
            concentracion_est_top5 = (top_establecimientos.head(5).sum() / total_casos) * 100
            st.metric("Concentración Top 5 Est.", f"{concentracion_est_top5:.1f}%")
            
            # Establecimiento principal
            if len(top_establecimientos) > 0:
                est_principal = top_establecimientos.index[0]
                casos_est_principal = top_establecimientos.iloc[0]
                porcentaje_est = (casos_est_principal / total_casos) * 100
                
                # Truncar nombre si es muy largo
                est_display = est_principal[:30] + "..." if len(est_principal) > 30 else est_principal
                
                st.info(f"""
                **Establecimiento Principal:**
                
                **{est_display}** 
                
                {casos_est_principal:,} casos ({porcentaje_est:.1f}% del total)
                """)
    
    # GRÁFICO 3: Concentración geográfica por departamento (si disponible)
    if 'departamento_normalizada' in df.columns:
        st.subheader("📍 Distribución por Departamento")
        
        dept_counts = df['departamento_normalizada'].value_counts().head(10)
        
        if len(dept_counts) > 0:
            fig = px.pie(
                values=dept_counts.values,
                names=dept_counts.index,
                title='Distribución de Casos por Departamento (Top 10)'
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
