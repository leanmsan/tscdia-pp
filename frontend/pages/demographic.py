"""
Página de Análisi    try:
    .info(f"Analizando {len(df):,} registros totales")
        
        show_demographic_analysis(df)= fetch_dengue_data()
        if df is None or len(df) == 0:
            st.error("No se pudieron obtener datos del backend")
            return
        
        st.info(f" Analizando {len(df):,} registros totales")
        
        show_demographic_analysis(df)- Solo gráficos del análisis original
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.data_fetcher import fetch_dengue_data

# Configuración de la página
st.set_page_config(
    page_title="Análisis Demográfico",
    layout="wide"
)

def main():
    """Función principal de la página demográfica"""
    
    st.title("Análisis Demográfico")
    
    # Obtener datos
    try:
        df = fetch_dengue_data()
        if df is None or len(df) == 0:
            st.error("No se pudieron obtener datos del backend")
            return
        
        st.info(f"Analizando {len(df):,} registros totales")
        
        show_demographic_page(df)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

def show_demographic_page(df: pd.DataFrame):
    """Análisis demográfico basado exactamente en el script original"""
    
    if len(df) == 0:
        st.warning(" No hay datos disponibles con los filtros seleccionados")
        return
    
    # GRÁFICO 1: Distribución de edad (EXACTO del análisis original)
    if 'edad' in df.columns:
        st.subheader(" Distribución de la Edad")
        
        # Filtrar datos válidos
        df_edad = df[(df['edad'].notna()) & (df['edad'] > 0) & (df['edad'] <= 100)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma como en el original
            fig = px.histogram(
                df_edad,
                x='edad',
                nbins=30,
                title='Distribución de la Edad',
                color_discrete_sequence=['#4ECDC4']
            )
            fig.update_layout(
                xaxis_title="Edad",
                yaxis_title="Frecuencia",
                xaxis=dict(range=[0, 100])
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # GRÁFICO 2: Distribución por grupos etarios (EXACTO del análisis original)
            bins = [0, 10, 20, 30, 40, 50, 60, 70, 100]
            labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']
            df_edad['grupo_etario'] = pd.cut(df_edad['edad'], bins=bins, labels=labels, right=False)
            
            grupo_counts = df_edad['grupo_etario'].value_counts().sort_index()
            
            fig = px.bar(
                x=grupo_counts.index,
                y=grupo_counts.values,
                title='Distribución de Casos por Grupo Etario',
                color=grupo_counts.values,
                color_continuous_scale='viridis'
            )
            
            # Añadir porcentajes como en el análisis original
            total_casos = len(df_edad)
            for i, (idx, val) in enumerate(grupo_counts.items()):
                porcentaje = (val / total_casos) * 100
                fig.add_annotation(
                    x=i, y=val/2,
                    text=f"{val:,}<br>({porcentaje:.1f}%)",
                    showarrow=False,
                    font=dict(color="white", size=10, family="Arial Black")
                )
            
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # GRÁFICO 3: Box Plot - Distribución de Días de Evolución por Grupo Etario (DEL ANÁLISIS ORIGINAL)
    if 'edad' in df.columns and 'dias_evolucion' in df.columns:
        st.subheader("📈 Distribución de Días de Evolución por Grupo Etario")
        
        # Preparar datos
        df_evol = df[(df['edad'].notna()) & (df['dias_evolucion'].notna()) & 
                     (df['edad'] > 0) & (df['edad'] <= 100) & (df['dias_evolucion'] >= 0)]
        
        if len(df_evol) > 0:
            bins = [0, 10, 20, 30, 40, 50, 60, 70, 100]
            labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']
            df_evol['grupo_etario'] = pd.cut(df_evol['edad'], bins=bins, labels=labels, right=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Box plot como en el análisis original
                fig = px.box(
                    df_evol,
                    x='grupo_etario',
                    y='dias_evolucion',
                    title='Distribución de Días de Evolución por Grupo Etario',
                    color='grupo_etario',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                # Añadir línea de mediana global (como en el original)
                mediana_global = df_evol['dias_evolucion'].median()
                fig.add_hline(y=mediana_global, line_dash="dash", line_color="red", 
                             annotation_text=f"Mediana global: {mediana_global:.0f} días")
                
                fig.update_layout(
                    xaxis_title="Grupo Etario",
                    yaxis_title="Días de Evolución",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Estadísticas por grupo etario (como en el análisis original)
                stats_by_group = df_evol.groupby('grupo_etario')['dias_evolucion'].agg([
                    'count', 'mean', 'median', 'std', 
                    lambda x: x.quantile(0.25),
                    lambda x: x.quantile(0.75),
                    'max'
                ]).round(1)
                
                stats_by_group.columns = ['Casos', 'Media', 'Mediana', 'Desv.Est', 'Q25', 'Q75', 'Máximo']
                
                st.subheader("Estadísticas por Grupo Etario")
                st.dataframe(stats_by_group, use_container_width=True)
                
                # Insights del análisis original
                st.info("""
                **Patrones Identificados:**
                - A mayor edad, mayor tiempo promedio de evolución
                - Los grupos >50 años superan la mediana global
                - Alta variabilidad en todos los grupos (casos atípicos hasta 29 días)
                - El 25% inferior en todos los grupos muestra 0 días
                """)
    
    # GRÁFICO 4: Edad vs Género (Del análisis original - análisis cruzado)
    if 'edad' in df.columns and 'sexo_normalizado' in df.columns:
        st.subheader("👫 Análisis Cruzado: Edad vs Género")
        
        df_gender = df[(df['edad'].notna()) & (df['sexo_normalizado'].notna()) & 
                       (df['edad'] > 0) & (df['edad'] <= 100)]
        
        if len(df_gender) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Box plot edad por género
                fig = px.box(
                    df_gender,
                    x='sexo_normalizado',
                    y='edad',
                    title='Distribución de Edad por Género',
                    color='sexo_normalizado',
                    color_discrete_sequence=['#FF6B6B', '#4ECDC4']
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Distribución por género (pie chart)
                genero_counts = df_gender['sexo_normalizado'].value_counts()
                
                fig = px.pie(
                    values=genero_counts.values,
                    names=genero_counts.index,
                    title='Distribución por Género',
                    color_discrete_sequence=['#FF6B6B', '#4ECDC4']
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
