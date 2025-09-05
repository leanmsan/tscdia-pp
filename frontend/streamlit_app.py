import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_fetcher import fetch_dengue_data
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Dashboard - Análisis de Dengue",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Página principal - Dashboard"""
    
    st.title("Dashboard Principal")
    st.caption("Resumen general de casos de dengue")
    
    # Obtener y validar datos
    try:
        df = fetch_dengue_data()
        
        if df is None or len(df) == 0:
            st.error("❌ **Error:** No se pudieron obtener datos del backend")
            st.info("🔧 **Soluciones posibles:**")
            st.write("1. Verificar que el backend esté ejecutándose en http://localhost:8000")
            st.write("2. Comprobar la conexión a la base de datos")
            st.write("3. Revisar los logs del backend para errores")
            
            if st.button("🔄 Reintentar Conexión"):
                st.rerun()
            return
        
        st.info(f"Analizando {len(df):,} registros totales")
        
        # Mostrar contenido del dashboard
        show_dashboard_content(df)
    
    except Exception as e:
        st.error(f"❌ **Error inesperado:** {str(e)}")
        with st.expander("Ver detalles del error"):
            import traceback
            st.code(traceback.format_exc())

def show_dashboard_content(df: pd.DataFrame):
    """Dashboard principal con KPIs y gráficos del análisis original"""
    
    if len(df) == 0:
        st.warning("No hay datos disponibles con los filtros seleccionados")
        return
    
    import plotly.express as px
    import plotly.graph_objects as go
    import numpy as np
    
    # === KPIs PRINCIPALES ===
    st.subheader("Indicadores Clave")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_casos = len(df)
        st.metric("Total Casos", f"{total_casos:,}")
    
    with col2:
        if 'rt_pcr_tiempo_real_dengue' in df.columns:
            pcr_positivos = df[df['rt_pcr_tiempo_real_dengue'].str.contains('positivo|POSITIVO', na=False)].shape[0]
            st.metric("PCR Positivos", f"{pcr_positivos:,}")
        else:
            st.metric("PCR Positivos", "N/A")
    
    with col3:
        if 'edad' in df.columns:
            edad_promedio = df['edad'].mean()
            st.metric("Edad Promedio", f"{edad_promedio:.1f} años" if pd.notna(edad_promedio) else "N/A")
        else:
            st.metric("Edad Promedio", "N/A")
    
    with col4:
        if 'localidad_normalizada' in df.columns:
            localidades = df['localidad_normalizada'].nunique()
            st.metric("Localidades", f"{localidades:,}")
        else:
            st.metric("Localidades", "N/A")
    
    with col5:
        # Demora promedio en procesamiento
        if 'fecha_recepcion' in df.columns and 'fecha_procesamiento' in df.columns:
            df_temp = df.copy()
            df_temp['fecha_recepcion'] = pd.to_datetime(df_temp['fecha_recepcion'], errors='coerce')
            df_temp['fecha_procesamiento'] = pd.to_datetime(df_temp['fecha_procesamiento'], errors='coerce')
            
            delta = df_temp['fecha_procesamiento'] - df_temp['fecha_recepcion']
            demora_promedio = delta.dt.total_seconds() / 86400
            demora_promedio = demora_promedio[demora_promedio.notna() & (demora_promedio >= 0)].mean()
            
            if pd.notna(demora_promedio):
                st.metric("Demora Procesamiento", f"{demora_promedio:.1f} días")
            else:
                st.metric("Demora Procesamiento", "N/A")
        else:
            st.metric("Demora Procesamiento", "N/A")
    
    # === GRÁFICOS PRINCIPALES (FILA 1) ===
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico 1: Distribución de resultados PCR (PIE CHART)
        if 'rt_pcr_tiempo_real_dengue' in df.columns:
            # Normalizar valores PCR como en el análisis original
            pcr_values = df['rt_pcr_tiempo_real_dengue'].fillna('No realizado')
            pcr_normalized = []
            for val in pcr_values:
                val_str = str(val).lower().strip()
                if 'positivo' in val_str:
                    pcr_normalized.append('Positivo')
                elif 'negativo' in val_str or 'no detectable' in val_str:
                    pcr_normalized.append('Negativo')
                elif 'proceso' in val_str:
                    pcr_normalized.append('En proceso')
                elif 'den-1' in val_str:
                    pcr_normalized.append('DEN-1')
                else:
                    pcr_normalized.append('No realizado')
            
            pcr_counts = pd.Series(pcr_normalized).value_counts()
            
            colors = {
                'Positivo': '#FF5252',
                'Negativo': '#4CAF50', 
                'No realizado': '#BDBDBD',
                'En proceso': '#FFD600',
                'DEN-1': '#9C27B0'
            }
            
            fig = px.pie(
                values=pcr_counts.values,
                names=pcr_counts.index,
                title='Distribución de Resultados RT-PCR Dengue',
                color=pcr_counts.index,
                color_discrete_map=colors
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico 2: Top 10 Establecimientos Notificadores (BARRAS HORIZONTALES)
        if 'establecimiento_notificador_normalizada' in df.columns:
            top_establecimientos = df['establecimiento_notificador_normalizada'].value_counts().head(10)
            
            fig = px.bar(
                x=top_establecimientos.values,
                y=top_establecimientos.index,
                orientation='h',
                title='Top 10 Establecimientos Notificadores',
                color=top_establecimientos.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # === GRÁFICOS DEMOGRÁFICOS (FILA 2) ===
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico 3: Distribución de edad (HISTOGRAMA)
        if 'edad' in df.columns:
            df_edad = df[df['edad'].notna() & (df['edad'] > 0) & (df['edad'] <= 100)]
            
            fig = px.histogram(
                df_edad,
                x='edad',
                nbins=30,
                title='Distribución de Edades',
                color_discrete_sequence=['#4ECDC4']
            )
            fig.update_layout(
                xaxis_title="Edad",
                yaxis_title="Frecuencia",
                bargap=0.1
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico 4: Distribución por grupos etarios (BARRAS CON PORCENTAJES)
        if 'edad' in df.columns:
            df_edad = df[df['edad'].notna() & (df['edad'] > 0) & (df['edad'] <= 100)]
            
            # Crear grupos etarios como en el análisis original
            bins = [0, 10, 20, 30, 40, 50, 60, 70, 100]
            labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']
            df_edad['grupo_etario'] = pd.cut(df_edad['edad'], bins=bins, labels=labels, right=False)
            
            grupo_counts = df_edad['grupo_etario'].value_counts().sort_index()
            
            fig = px.bar(
                x=grupo_counts.index,
                y=grupo_counts.values,
                title='Distribución por Grupos Etarios',
                color=grupo_counts.values,
                color_continuous_scale='viridis'
            )
            
            # Añadir porcentajes como en el análisis original
            total_casos_edad = len(df_edad)
            for i, (idx, val) in enumerate(grupo_counts.items()):
                porcentaje = (val / total_casos_edad) * 100
                fig.add_annotation(
                    x=i, y=val/2,
                    text=f"{val}<br>({porcentaje:.1f}%)",
                    showarrow=False,
                    font=dict(color="white", size=10)
                )
            
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # === ANÁLISIS TEMPORAL ===
    if 'fecha_consulta' in df.columns:
        st.subheader(" Análisis Temporal")
        
        df_temp = df.copy()
        df_temp['fecha_consulta'] = pd.to_datetime(df_temp['fecha_consulta'], errors='coerce')
        df_temp = df_temp[df_temp['fecha_consulta'].notna()]
        
        if len(df_temp) > 0:
            # Gráfico 5: Tendencia mensual (LÍNEA TEMPORAL)
            df_temp['mes_año'] = df_temp['fecha_consulta'].dt.to_period('M').astype(str)
            casos_mensuales = df_temp['mes_año'].value_counts().sort_index()
            
            fig = px.line(
                x=casos_mensuales.index,
                y=casos_mensuales.values,
                title='Tendencia Mensual de Casos de Dengue',
                markers=True
            )
            fig.update_traces(line_color='#4ECDC4', line_width=3, marker_size=8)
            fig.update_layout(
                xaxis_title="Mes-Año",
                yaxis_title="Número de Casos"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # === ANÁLISIS DE LOCALIDADES ===
    if 'localidad_normalizada' in df.columns:
        st.subheader("Análisis Geográfico")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 20 localidades como en el análisis original
            top_localidades = df['localidad_normalizada'].value_counts().head(20)
            
            fig = px.bar(
                x=top_localidades.values,
                y=top_localidades.index,
                orientation='h',
                title='Top 20 Localidades más Frecuentes',
                color=top_localidades.values,
                color_continuous_scale='viridis'
            )
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Métricas geográficas adicionales
            st.subheader("Estadísticas Geográficas")
            
            departamentos = df['departamento_normalizada'].nunique() if 'departamento_normalizada' in df.columns else 0
            st.metric("Departamentos Afectados", departamentos)
            
            # Concentración en principales localidades
            if len(top_localidades) > 0:
                concentracion_top5 = (top_localidades.head(5).sum() / len(df)) * 100
                st.metric("Concentración Top 5", f"{concentracion_top5:.1f}%")
                
                localidad_principal = top_localidades.index[0]
                casos_principal = top_localidades.iloc[0]
                porcentaje_principal = (casos_principal / len(df)) * 100
                
                st.info(f"**{localidad_principal}** concentra {casos_principal:,} casos ({porcentaje_principal:.1f}% del total)")
    
    # === ANÁLISIS DE LABORATORIO (Si hay datos de serotipos) ===
    if 'serotipo_virus_dengue' in df.columns:
        st.subheader("🔬 Análisis de Serotipos")
        
        # Normalizar serotipos
        serotipos_norm = []
        for val in df['serotipo_virus_dengue'].fillna('No realizado'):
            val_str = str(val).lower().strip()
            if 'den-1' in val_str:
                serotipos_norm.append('DEN-1')
            elif 'den-2' in val_str:
                serotipos_norm.append('DEN-2')
            elif 'den-3' in val_str:
                serotipos_norm.append('DEN-3')
            elif 'den-4' in val_str:
                serotipos_norm.append('DEN-4')
            else:
                serotipos_norm.append('No realizado')
        
        serotipos_counts = pd.Series(serotipos_norm).value_counts()
        
        if len(serotipos_counts[serotipos_counts.index != 'No realizado']) > 0:
            fig = px.bar(
                x=serotipos_counts.index,
                y=serotipos_counts.values,
                title='Distribución de Serotipos de Dengue',
                color=serotipos_counts.values,
                color_continuous_scale=['#FF6B6B', '#4ECDC4', '#FFD93D', '#6C5CE7']
            )
            
            # Añadir porcentajes
            total_serotipos = serotipos_counts.sum()
            for i, (idx, val) in enumerate(serotipos_counts.items()):
                porcentaje = (val / total_serotipos) * 100
                fig.add_annotation(
                    x=i, y=val + val*0.05,
                    text=f"{val}<br>({porcentaje:.1f}%)",
                    showarrow=False
                )
            
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # === KPI DE EFECTIVIDAD ===
    st.subheader("Indicadores de Efectividad")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Efectividad en detección
        if 'rt_pcr_tiempo_real_dengue' in df.columns:
            total_casos = len(df)
            casos_testeados = df[df['rt_pcr_tiempo_real_dengue'].notna()].shape[0]
            efectividad = (casos_testeados / total_casos) * 100 if total_casos > 0 else 0
            
            st.metric("Cobertura de Testeo", f"{efectividad:.1f}%")
    
    with col2:
        # Porcentaje de casos positivos entre testeados
        if 'rt_pcr_tiempo_real_dengue' in df.columns:
            df_testeados = df[df['rt_pcr_tiempo_real_dengue'].notna()]
            positivos = df_testeados[df_testeados['rt_pcr_tiempo_real_dengue'].str.contains('positivo|POSITIVO', na=False)].shape[0]
            tasa_positividad = (positivos / len(df_testeados)) * 100 if len(df_testeados) > 0 else 0
            
            st.metric("Tasa de Positividad", f"{tasa_positividad:.1f}%")
    
    with col3:
        # Completitud de datos demográficos
        if 'edad' in df.columns and 'sexo_normalizado' in df.columns:
            datos_completos = df[(df['edad'].notna()) & (df['sexo_normalizado'].notna())].shape[0]
            completitud = (datos_completos / len(df)) * 100
            
            st.metric("Completitud Demográfica", f"{completitud:.1f}%")

if __name__ == "__main__":
    main()
