"""
Dashboard ejemplo usando Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="TSCDIA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📊 Dashboard TSCDIA - Análisis de Datos")
st.markdown("---")

# Sidebar
st.sidebar.header("🔧 Configuración")
st.sidebar.markdown("Selecciona las opciones para personalizar el análisis")

# Ejemplo de datos (reemplazar con datos reales)
@st.cache_data
def load_data():
    """Cargar datos de ejemplo"""
    np.random.seed(42)
    data = {
        'fecha': pd.date_range('2024-01-01', periods=100),
        'ventas': np.random.normal(1000, 200, 100),
        'categoria': np.random.choice(['A', 'B', 'C', 'D'], 100),
        'region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], 100),
        'satisfaccion': np.random.uniform(1, 5, 100)
    }
    return pd.DataFrame(data)

# Cargar datos
df = load_data()

# Filtros en sidebar
st.sidebar.subheader("📅 Filtros de Fecha")
date_range = st.sidebar.date_input(
    "Seleccionar rango de fechas",
    value=(df['fecha'].min(), df['fecha'].max()),
    min_value=df['fecha'].min(),
    max_value=df['fecha'].max()
)

st.sidebar.subheader("🏷️ Filtros de Categoría")
categorias = st.sidebar.multiselect(
    "Seleccionar categorías",
    options=df['categoria'].unique(),
    default=df['categoria'].unique()
)

# Aplicar filtros
filtered_df = df[
    (df['fecha'] >= pd.to_datetime(date_range[0])) &
    (df['fecha'] <= pd.to_datetime(date_range[1])) &
    (df['categoria'].isin(categorias))
]

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Ventas Total",
        value=f"${filtered_df['ventas'].sum():,.0f}",
        delta=f"{filtered_df['ventas'].sum() - df['ventas'].mean()*len(filtered_df):,.0f}"
    )

with col2:
    st.metric(
        label="📈 Promedio Ventas",
        value=f"${filtered_df['ventas'].mean():,.0f}",
        delta=f"{filtered_df['ventas'].mean() - df['ventas'].mean():,.0f}"
    )

with col3:
    st.metric(
        label="📊 Registros",
        value=len(filtered_df),
        delta=f"{len(filtered_df) - len(df)}"
    )

with col4:
    st.metric(
        label="⭐ Satisfacción Prom.",
        value=f"{filtered_df['satisfaccion'].mean():.1f}",
        delta=f"{filtered_df['satisfaccion'].mean() - df['satisfaccion'].mean():.1f}"
    )

st.markdown("---")

# Gráficos principales
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Evolución de Ventas")
    fig_line = px.line(
        filtered_df, 
        x='fecha', 
        y='ventas',
        title="Ventas por Fecha"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("🏷️ Ventas por Categoría")
    ventas_categoria = filtered_df.groupby('categoria')['ventas'].sum().reset_index()
    fig_bar = px.bar(
        ventas_categoria,
        x='categoria',
        y='ventas',
        title="Ventas Totales por Categoría"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Segunda fila de gráficos
col3, col4 = st.columns(2)

with col3:
    st.subheader("🗺️ Ventas por Región")
    fig_pie = px.pie(
        filtered_df,
        values='ventas',
        names='region',
        title="Distribución de Ventas por Región"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.subheader("⭐ Distribución de Satisfacción")
    fig_hist = px.histogram(
        filtered_df,
        x='satisfaccion',
        nbins=20,
        title="Distribución de Satisfacción del Cliente"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# Análisis avanzado
st.markdown("---")
st.subheader("🔍 Análisis Detallado")

tab1, tab2, tab3 = st.tabs(["📊 Estadísticas", "📈 Correlaciones", "🔢 Datos"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Estadísticas Descriptivas - Ventas**")
        st.dataframe(filtered_df['ventas'].describe())
    
    with col2:
        st.write("**Estadísticas Descriptivas - Satisfacción**")
        st.dataframe(filtered_df['satisfaccion'].describe())

with tab2:
    st.write("**Matriz de Correlación**")
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    corr_matrix = filtered_df[numeric_cols].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Matriz de Correlación"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

with tab3:
    st.write("**Datos Filtrados**")
    st.dataframe(filtered_df)
    
    # Botón de descarga
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Descargar datos como CSV",
        data=csv,
        file_name='datos_filtrados.csv',
        mime='text/csv'
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <small>
        Dashboard desarrollado para TSCDIA - Instituto Tecnológico de Santiago del Estero
        </small>
    </div>
    """,
    unsafe_allow_html=True
)
