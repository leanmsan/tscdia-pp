"""
Página de Análisis de La .info(f"Analizando {len(df):,} registros totales")
        
        show_laboratory_analysis(df)o - Solo gráficos del análisis original
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.data_fetcher import fetch_dengue_data


# Configuración de la página
st.set_page_config(
    page_title="Análisis de Laboratorio",
    page_icon="🔬",
    layout="wide"
)

def main():
    """Función principal de la página"""
    
    st.title("🔬 Análisis de Laboratorio")
    
    # Obtener datos
    try:
        df = fetch_dengue_data()
        if df is None or len(df) == 0:
            st.error("No se pudieron obtener datos del backend")
            return
        
        st.info(f"Analizando {len(df):,} registros totales")
        
        show_laboratory_page(df)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

def show_laboratory_page(df: pd.DataFrame):
    """Análisis de laboratorio basado exactamente en el script original"""
    
    if len(df) == 0:
        st.warning(" No hay datos disponibles con los filtros seleccionados")
        return
    
    # GRÁFICO 1: Distribución de serotipos (EXACTO del análisis original)
    if 'serotipo_virus_dengue' in df.columns:
        st.subheader("🧬 Distribución de Serotipos")
        
        # Normalizar serotipos como en el análisis original
        serotipos_norm = []
        for val in df['serotipo_virus_dengue'].fillna('no realizado'):
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
                serotipos_norm.append('no realizado')
        
        serotipos_counts = pd.Series(serotipos_norm).value_counts()
        
        # Filtrar solo los serotipos identificados (excluir 'no realizado')
        serotipos_identificados = serotipos_counts[serotipos_counts.index != 'no realizado']
        
        if len(serotipos_identificados) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de barras como en el análisis original
                fig = px.bar(
                    x=serotipos_identificados.index,
                    y=serotipos_identificados.values,
                    title='Distribución de Serotipos de Dengue',
                    color=serotipos_identificados.values,
                    color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#FFD93D', '#6C5CE7']
                )
                
                # Añadir porcentajes como en el análisis original
                total_serotipos = serotipos_identificados.sum()
                for i, (idx, val) in enumerate(serotipos_identificados.items()):
                    porcentaje = (val / total_serotipos) * 100
                    fig.add_annotation(
                        x=i, y=val + val*0.05,
                        text=f"{val}<br>({porcentaje:.1f}%)",
                        showarrow=False
                    )
                
                # Añadir línea de promedio como en el análisis original
                promedio = np.mean(serotipos_identificados.values)
                fig.add_hline(y=promedio, line_dash="dash", line_color="gray", 
                             annotation_text="Promedio")
                
                fig.update_layout(
                    xaxis_title="Serotipo",
                    yaxis_title="Número de Casos",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Información del serotipo más frecuente (como en el análisis original)
                serotipo_mas_frec = serotipos_identificados.idxmax()
                casos_mas_frec = serotipos_identificados.max()
                porc_mas_frec = (casos_mas_frec / total_serotipos) * 100
                
                st.subheader("Análisis de Serotipos")
                
                st.metric("Serotipo Dominante", serotipo_mas_frec)
                st.metric("Casos del Dominante", f"{casos_mas_frec:,}")
                st.metric("Porcentaje Dominante", f"{porc_mas_frec:.1f}%")
                
                # Información contextual del análisis original
                st.info(f"""
                **Interpretación Epidemiológica:**
                
                El serotipo {serotipo_mas_frec} representa el {porc_mas_frec:.1f}% de los casos confirmados.
                
                La co-circulación de múltiples serotipos (DEN-1 y DEN-2) es una situación que requiere 
                especial atención debido al riesgo de segundas infecciones con un serotipo diferente, 
                lo que aumenta el riesgo de casos de dengue grave.
                
                **Total de casos con serotipo identificado: {total_serotipos:,}**
                """)
    
    # GRÁFICO 2: Efectividad en la Detección de Dengue (EXACTO del análisis original)
    if 'rt_pcr_tiempo_real_dengue' in df.columns:
        st.subheader("📈 Efectividad en la Detección de Dengue")
        
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
        
        # Separar testeados vs no realizados como en el análisis original
        total_testeados = pcr_counts.get('Positivo', 0) + pcr_counts.get('Negativo', 0) + pcr_counts.get('En proceso', 0) + pcr_counts.get('DEN-1', 0)
        total_no_realizados = pcr_counts.get('No realizado', 0)
        total_casos = len(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico 1: Testeados vs No Realizados
            fig = px.bar(
                x=['Testeados', 'No realizado'],
                y=[total_testeados, total_no_realizados],
                title='Proporción de Pruebas Realizadas',
                color=['Testeados', 'No realizado'],
                color_discrete_map={'Testeados': '#3f51b5', 'No realizado': '#999999'}
            )
            
            # Añadir porcentajes
            for i, valor in enumerate([total_testeados, total_no_realizados]):
                porcentaje = (valor / total_casos) * 100
                fig.add_annotation(
                    x=i, y=valor + valor*0.05,
                    text=f"{porcentaje:.1f}%",
                    showarrow=False,
                    font=dict(size=12, color="black")
                )
            
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico 2: Desglose de Resultados en Testeados
            resultados_testeados = {k: v for k, v in pcr_counts.items() if k != 'No realizado'}
            
            if len(resultados_testeados) > 0:
                colores = {'Positivo': '#F44336', 'Negativo': '#4CAF50', 'En proceso': '#FFC107', 'DEN-1': '#9C27B0'}
                
                fig = px.bar(
                    x=list(resultados_testeados.keys()),
                    y=list(resultados_testeados.values()),
                    title='Resultados de Pruebas Realizadas',
                    color=list(resultados_testeados.keys()),
                    color_discrete_map=colores
                )
                
                # Añadir porcentajes sobre el total de testeados
                for i, (clave, valor) in enumerate(resultados_testeados.items()):
                    porcentaje = (valor / total_testeados) * 100 if total_testeados > 0 else 0
                    fig.add_annotation(
                        x=i, y=valor + valor*0.05,
                        text=f"{porcentaje:.1f}%",
                        showarrow=False,
                        font=dict(size=12, color="black")
                    )
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        # Resumen de efectividad como en el análisis original
        st.subheader(" Resumen de Efectividad")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cobertura = (total_testeados / total_casos) * 100
            st.metric("Cobertura de Testeo", f"{cobertura:.1f}%")
        
        with col2:
            if total_testeados > 0:
                tasa_positividad = (pcr_counts.get('Positivo', 0) / total_testeados) * 100
                st.metric("Tasa de Positividad", f"{tasa_positividad:.1f}%")
        
        with col3:
            st.metric("Casos Testeados", f"{total_testeados:,}")
        
        with col4:
            st.metric("Casos No Testeados", f"{total_no_realizados:,}")
        
        # Conclusiones del análisis original
        st.info(f"""
        **Análisis de Efectividad:**
        
        Solo el {cobertura:.1f}% de los casos sospechosos fueron testeados ({total_testeados:,} pruebas), 
        mientras que el {100-cobertura:.1f}% no recibió evaluación ({total_no_realizados:,} casos).
        
        Entre los testeados, se detectó un {(pcr_counts.get('Positivo', 0)/total_testeados*100):.1f}% de positivos 
        y un {(pcr_counts.get('Negativo', 0)/total_testeados*100):.1f}% de negativos.
        
        **Recomendación:** La baja cobertura de testeo combinada con la alta positividad sugiere una 
        probable subestimación de casos reales. Se recomienda ampliar urgentemente la capacidad diagnóstica.
        """)

if __name__ == "__main__":
    main()
