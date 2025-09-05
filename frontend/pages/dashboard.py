"""
Página de Dashboard Completo - Simple
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_fetcher import fetch_dengue_data

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Completo",
    layout="wide"
)

def format_number(num):
    """Formatear número con comas como separadores de miles"""
    return f"{num:,}"

def format_percentage(part, total):
    """Formatear porcentaje"""
    if total == 0:
        return "0.0%"
    return f"{(part/total)*100:.1f}%"

def main():
    """Función principal de la página"""
    
    st.title("Dashboard Completo")
    
    # Obtener datos
    try:
        df = fetch_dengue_data()
        if df is None or len(df) == 0:
            st.error("No se pudieron obtener datos del backend")
            return
        
        st.info(f"Analizando {len(df):,} registros totales")
        
        show_dashboard_content(df)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

def show_dashboard_content(df: pd.DataFrame):
    """Mostrar página principal del dashboard"""
    
    if len(df) == 0:
        st.warning("No hay datos disponibles")
        return
    
    # SECCIÓN 1: INDICADORES CLAVE
    st.subheader("Indicadores Clave")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_casos = len(df)
        st.metric("Total Casos", format_number(total_casos))
    
    with col2:
        if 'rt_pcr_tiempo_real_dengue_normalizado' in df.columns:
            positivos = df[df['rt_pcr_tiempo_real_dengue_normalizado'] == 'positivo']
            st.metric("Casos Positivos", format_number(len(positivos)))
        else:
            st.metric("Casos Positivos", "N/A")
    
    with col3:
        if 'edad' in df.columns:
            edad_promedio = df['edad'].mean()
            st.metric("Edad Promedio", f"{edad_promedio:.1f} años" if pd.notna(edad_promedio) else "N/A")
        else:
            st.metric("Edad Promedio", "N/A")
    
    with col4:
        if 'localidad_normalizada' in df.columns:
            localidades_unicas = df['localidad_normalizada'].nunique()
            st.metric("Localidades", format_number(localidades_unicas))
        else:
            st.metric("Localidades", "N/A")
    
    with col5:
        if 'establecimiento_notificador_normalizada' in df.columns:
            establecimientos = df['establecimiento_notificador_normalizada'].nunique()
            st.metric("Establecimientos", format_number(establecimientos))
        else:
            st.metric("Establecimientos", "N/A")

    # GRÁFICOS PRINCIPALES DEL ANÁLISIS ORIGINAL
    col1, col2 = st.columns(2)
    
    # GRÁFICO 1: Distribución de PCR (del análisis original)
    with col1:
        if 'rt_pcr_tiempo_real_dengue_normalizado' in df.columns:
            pcr_counts = df['rt_pcr_tiempo_real_dengue_normalizado'].value_counts()
            
            colors = {
                'positivo': '#FF5252',
                'negativo': '#4CAF50', 
                'no realizado': '#BDBDBD',
                'en proceso': '#FFD600'
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
    
    # GRÁFICO 2: Histograma de edades (del análisis original)
    with col2:
        if 'edad' in df.columns:
            df_edad = df[(df['edad'].notna()) & (df['edad'] > 0) & (df['edad'] <= 100)]
            
            if len(df_edad) > 0:
                fig = px.histogram(
                    df_edad,
                    x='edad',
                    nbins=30,
                    title='Distribución de la Edad',
                    color_discrete_sequence=['#2E86C1']
                )
                fig.update_layout(
                    xaxis_title="Edad",
                    yaxis_title="Frecuencia",
                    bargap=0.1
                )
                st.plotly_chart(fig, use_container_width=True)

    # GRÁFICO 3: Distribución por grupos etarios (del análisis original)
    if 'edad' in df.columns:
        st.subheader("Análisis Demográfico")
        
        df_edad = df[(df['edad'].notna()) & (df['edad'] > 0) & (df['edad'] <= 100)]
        
        if len(df_edad) > 0:
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
            fig.update_layout(
                xaxis_title="Grupo Etario",
                yaxis_title="Número de Casos"
            )
            st.plotly_chart(fig, use_container_width=True)

    # GRÁFICO 4: Top 20 localidades (del análisis original)
    if 'localidad_normalizada' in df.columns:
        st.subheader("Análisis Geográfico")
        
        top_localidades = df['localidad_normalizada'].value_counts().nlargest(20)
        
        if len(top_localidades) > 0:
            fig = px.bar(
                y=top_localidades.index,
                x=top_localidades.values,
                orientation='h',
                title='Top 20 Localidades más Frecuentes',
                color=top_localidades.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                xaxis_title="Cantidad de Registros",
                yaxis_title="Localidad",
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)

    # GRÁFICO 5: Análisis de serotipos (del análisis original)
    if 'serotipo_virus_dengue_normalizado' in df.columns:
        serotipos_data = df[df['serotipo_virus_dengue_normalizado'].notna() & 
                           (df['serotipo_virus_dengue_normalizado'] != 'no realizado')]
        
        if len(serotipos_data) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                serotipos_counts = serotipos_data['serotipo_virus_dengue_normalizado'].value_counts()
                
                fig = px.bar(
                    x=serotipos_counts.index,
                    y=serotipos_counts.values,
                    title='Distribución de Serotipos de Dengue',
                    color=serotipos_counts.values,
                    color_continuous_scale=['#FF6B6B', '#4ECDC4', '#FFD93D', '#6C5CE7']
                )
                
                # Añadir porcentajes
                total = serotipos_counts.sum()
                for i, (serotipo, count) in enumerate(serotipos_counts.items()):
                    percentage = (count / total) * 100
                    fig.add_annotation(
                        x=serotipo, y=count,
                        text=f"{count}<br>({percentage:.1f}%)",
                        showarrow=False,
                        font=dict(color="white", size=12)
                    )
                
                fig.update_layout(
                    xaxis_title="Serotipo",
                    yaxis_title="Número de Casos"
                )
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
