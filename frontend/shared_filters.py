"""
Filtros compartidos para todas las páginas del dashboard
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional

class FilterManager:
    """Gestor de filtros compartidos entre páginas"""
    
    def __init__(self):
        self.filters = {}
    
    def create_sidebar_filters(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Crear filtros en la sidebar que persistan entre páginas"""
        
        st.sidebar.markdown("---")
        st.sidebar.subheader(" Filtros")
        
        filters = {}
        
        # Filtro de fechas
        if 'fecha_recepcion' in df.columns and df['fecha_recepcion'].notna().any():
            min_date = df['fecha_recepcion'].min().date() if df['fecha_recepcion'].notna().any() else datetime.now().date()
            max_date = df['fecha_recepcion'].max().date() if df['fecha_recepcion'].notna().any() else datetime.now().date()
            
            # Usar session state para persistir el valor
            if 'filter_date_range' not in st.session_state:
                st.session_state.filter_date_range = (min_date, max_date)
            
            date_range = st.sidebar.date_input(
                " Rango de Fechas",
                value=st.session_state.filter_date_range,
                min_value=min_date,
                max_value=max_date,
                key='filter_date_input'
            )
            
            if isinstance(date_range, tuple) and len(date_range) == 2:
                filters['date_range'] = date_range
                st.session_state.filter_date_range = date_range
            elif len(date_range) == 1:
                filters['date_range'] = (date_range, date_range)
        
        # Filtro de localidades
        if 'localidad_normalizada' in df.columns:
            localidades = ['Todas'] + sorted([loc for loc in df['localidad_normalizada'].dropna().unique() if pd.notna(loc)])
            
            selected_localidad = st.sidebar.selectbox(
                "🏘️ Localidad",
                localidades,
                key='filter_localidad'
            )
            filters['localidad'] = selected_localidad
        
        # Filtro de departamentos
        if 'departamento_normalizado' in df.columns:
            departamentos = ['Todos'] + sorted([dep for dep in df['departamento_normalizado'].dropna().unique() if pd.notna(dep)])
            
            selected_departamento = st.sidebar.selectbox(
                " Departamento",
                departamentos,
                key='filter_departamento'
            )
            filters['departamento'] = selected_departamento
        
        # Filtro de grupos etarios
        if 'grupo_etario' in df.columns:
            grupos = ['Todos'] + sorted([grupo for grupo in df['grupo_etario'].dropna().astype(str).unique() if pd.notna(grupo)])
            
            selected_grupo = st.sidebar.selectbox(
                " Grupo Etario",
                grupos,
                key='filter_grupo_etario'
            )
            filters['grupo_etario'] = selected_grupo
        
        # Filtro de resultado RT-PCR
        if 'rt_pcr_tiempo_real_dengue_normalizado' in df.columns:
            pcr_options = ['Todos'] + sorted([pcr for pcr in df['rt_pcr_tiempo_real_dengue_normalizado'].dropna().unique() if pd.notna(pcr)])
            
            selected_pcr = st.sidebar.selectbox(
                " Resultado RT-PCR",
                pcr_options,
                key='filter_pcr'
            )
            filters['pcr_result'] = selected_pcr
        
        # Mostrar resumen de filtros aplicados
        self._show_filter_summary(filters, df)
        
        return filters
    
    def apply_filters(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Aplicar filtros al dataframe"""
        filtered_df = df.copy()
        
        # Filtro de fechas
        if 'date_range' in filters and len(filters['date_range']) == 2:
            start_date, end_date = filters['date_range']
            if 'fecha_recepcion' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['fecha_recepcion'].dt.date >= start_date) &
                    (filtered_df['fecha_recepcion'].dt.date <= end_date)
                ]
        
        # Filtro de localidad
        if filters.get('localidad') and filters['localidad'] != 'Todas':
            if 'localidad_normalizada' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['localidad_normalizada'] == filters['localidad']]
        
        # Filtro de departamento
        if filters.get('departamento') and filters['departamento'] != 'Todos':
            if 'departamento_normalizado' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['departamento_normalizado'] == filters['departamento']]
        
        # Filtro de grupo etario
        if filters.get('grupo_etario') and filters['grupo_etario'] != 'Todos':
            if 'grupo_etario' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['grupo_etario'].astype(str) == filters['grupo_etario']]
        
        # Filtro de resultado PCR
        if filters.get('pcr_result') and filters['pcr_result'] != 'Todos':
            if 'rt_pcr_tiempo_real_dengue_normalizado' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['rt_pcr_tiempo_real_dengue_normalizado'] == filters['pcr_result']]
        
        return filtered_df
    
    def _show_filter_summary(self, filters: Dict[str, Any], original_df: pd.DataFrame):
        """Mostrar resumen de filtros aplicados"""
        st.sidebar.markdown("---")
        st.sidebar.subheader(" Resumen de Filtros")
        
        # Aplicar filtros para contar registros
        filtered_df = self.apply_filters(original_df, filters)
        
        # Mostrar conteos
        total_original = len(original_df)
        total_filtered = len(filtered_df)
        
        if total_filtered != total_original:
            reduction_pct = ((total_original - total_filtered) / total_original) * 100
            st.sidebar.metric(
                "Registros Mostrados", 
                f"{total_filtered:,}",
                delta=f"-{reduction_pct:.1f}%"
            )
        else:
            st.sidebar.metric("Registros Mostrados", f"{total_filtered:,}")
        
        st.sidebar.metric("Total Disponible", f"{total_original:,}")
        
        # Mostrar filtros activos
        active_filters = []
        for key, value in filters.items():
            if value and value not in ['Todas', 'Todos', 'Todos']:
                if key == 'date_range' and isinstance(value, tuple):
                    if value[0] != value[1]:
                        active_filters.append(f" {value[0]} - {value[1]}")
                    else:
                        active_filters.append(f" {value[0]}")
                elif key in ['localidad', 'departamento', 'grupo_etario', 'pcr_result']:
                    icons = {'localidad': '🏘️', 'departamento': '', 'grupo_etario': '', 'pcr_result': ''}
                    active_filters.append(f"{icons.get(key, '•')} {value}")
        
        if active_filters:
            st.sidebar.markdown("**Filtros Activos:**")
            for filter_text in active_filters:
                st.sidebar.markdown(f"• {filter_text}")
        else:
            st.sidebar.markdown("*Sin filtros aplicados*")

def get_filter_manager() -> FilterManager:
    """Obtener instancia singleton del gestor de filtros"""
    if 'filter_manager' not in st.session_state:
        st.session_state.filter_manager = FilterManager()
    return st.session_state.filter_manager

def show_data_quality_info(df: pd.DataFrame):
    """Mostrar información de calidad de datos en sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ Calidad de Datos")
    
    if len(df) > 0:
        # Completitud de datos clave
        key_columns = ['edad', 'rt_pcr_tiempo_real_dengue_normalizado', 'localidad_normalizada']
        
        for col in key_columns:
            if col in df.columns:
                completeness = (1 - df[col].isna().sum() / len(df)) * 100
                st.sidebar.progress(completeness / 100, text=f"{col.replace('_', ' ').title()}: {completeness:.1f}%")
        
        # Rango de fechas
        if 'fecha_recepcion' in df.columns and df['fecha_recepcion'].notna().any():
            min_date = df['fecha_recepcion'].min().strftime('%d/%m/%Y')
            max_date = df['fecha_recepcion'].max().strftime('%d/%m/%Y')
            st.sidebar.caption(f" Período: {min_date} - {max_date}")
        
        # Última actualización
        st.sidebar.caption(f"🔄 Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
def create_page_header(title: str, description: str = "", icon: str = ""):
    """Crear header simple para las páginas"""
    st.header(f"{icon} {title}")
    if description:
        st.caption(description)

def show_no_data_message(filter_context: str = "con los filtros seleccionados"):
    """Mostrar mensaje estándar cuando no hay datos"""
    st.warning(f" No hay datos disponibles {filter_context}")
    st.info(" **Sugerencias:**")
    st.info("• Amplíe el rango de fechas")
    st.info("• Seleccione 'Todas/Todos' en los filtros")
    st.info("• Verifique que haya datos cargados en el sistema")
