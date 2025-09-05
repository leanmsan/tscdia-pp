import polars as pl
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)

class DengueAnalyzer:
    def __init__(self, df: pl.DataFrame):
        self.df = df
    
    def clean_numeric_data(self) -> 'DengueAnalyzer':
        try:
            df_cleaned = self.df
            
            # Limpiar edad
            if 'edad' in df_cleaned.columns:
                df_cleaned = df_cleaned.with_columns([
                    pl.col('edad')
                    .cast(pl.Int32, strict=False)
                    .fill_null(0)
                    .clip(0, 120)  # Edad entre 0 y 120 años
                    .alias('edad')
                ])
            
            # Limpiar días de evolución
            if 'dias_evolucion' in df_cleaned.columns:
                df_cleaned = df_cleaned.with_columns([
                    pl.col('dias_evolucion')
                    .cast(pl.Int32, strict=False)
                    .fill_null(0)
                    .clip(0, 365)  # Días entre 0 y 365
                    .alias('dias_evolucion')
                ])
            
            # Limpiar demora en días
            if 'demora_dias' in df_cleaned.columns:
                df_cleaned = df_cleaned.with_columns([
                    pl.col('demora_dias')
                    .cast(pl.Float64, strict=False)
                    .fill_null(0.0)
                    .clip(0.0, 365.0)  # Demora entre 0 y 365 días
                    .alias('demora_dias')
                ])
            
            # Procesar fechas para asegurar formato correcto
            date_columns = ['fecha_recepcion', 'fecha_procesamiento', 'fecha_inicio_fiebre']
            for col in date_columns:
                if col in df_cleaned.columns:
                    try:
                        df_cleaned = df_cleaned.with_columns([
                            pl.coalesce([
                                pl.col(col).str.strptime(pl.Date, format='%Y-%m-%d', strict=False),
                                pl.col(col).str.strptime(pl.Date, format='%d/%m/%Y', strict=False),
                                pl.col(col).str.strptime(pl.Date, format='%Y/%m/%d', strict=False),
                                pl.col(col).cast(pl.Date, strict=False)
                            ]).alias(f'{col}_parsed')
                        ])
                    except Exception as date_error:
                        logger.warning(f"Error procesando fecha {col}: {date_error}")
            
            return DengueAnalyzer(df_cleaned)
        except Exception as e:
            logger.error(f"Error limpiando datos numéricos: {e}")
            return self

    def create_age_groups(self) -> 'DengueAnalyzer':
        if 'edad' not in self.df.columns:
            return self
        
        try:
            df_with_groups = self.df.with_columns([
                pl.when(pl.col('edad').is_between(0, 10, closed="left")).then(pl.lit('0-10'))
                .when(pl.col('edad').is_between(11, 20, closed="left")).then(pl.lit('11-20'))
                .when(pl.col('edad').is_between(21, 30, closed="left")).then(pl.lit('21-30'))
                .when(pl.col('edad').is_between(31, 40, closed="left")).then(pl.lit('31-40'))
                .when(pl.col('edad').is_between(41, 50, closed="left")).then(pl.lit('41-50'))
                .when(pl.col('edad').is_between(51, 60, closed="left")).then(pl.lit('51-60'))
                .when(pl.col('edad').is_between(61, 70, closed="left")).then(pl.lit('61-70'))
                .when(pl.col('edad') > 70).then(pl.lit('71+'))
                .otherwise(pl.lit('0-10'))  # Por defecto, grupo más joven
                .alias('grupo_etario')
            ])
            
            return DengueAnalyzer(df_with_groups)
        except Exception as e:
            logger.error(f"Error creando grupos etarios: {e}")
            return self
    
    def get_basic_stats(self) -> Dict[str, Any]:
        try:
            stats = {
                'total_casos': self.df.height,
                'columnas': self.df.columns,
                'fecha_min': None,
                'fecha_max': None,
                'localidades_unicas': 0,
                'departamentos_unicos': 0
            }
            
            # Estadísticas de fechas
            if 'fecha_recepcion' in self.df.columns:
                fecha_col = self.df.select('fecha_recepcion').to_series()
                if not fecha_col.is_empty():
                    stats['fecha_min'] = fecha_col.min()
                    stats['fecha_max'] = fecha_col.max()
            
            # Localidades únicas
            if 'localidad_normalizada' in self.df.columns:
                stats['localidades_unicas'] = self.df.select('localidad_normalizada').n_unique()
            
            # Departamentos únicos
            if 'departamento_normalizado' in self.df.columns:
                stats['departamentos_unicos'] = self.df.select('departamento_normalizado').n_unique()
            
            return stats
        except Exception as e:
            logger.error(f"Error calculando estadísticas básicas: {e}")
            return {'error': str(e)}
    
    def analyze_geographic_distribution(self, top_n: int = 20) -> Dict[str, Any]:
        try:
            result = {}
            
            # Top localidades
            if 'localidad_normalizada' in self.df.columns:
                top_localidades = (
                    self.df
                    .group_by('localidad_normalizada')
                    .agg(pl.count().alias('casos'))
                    .sort('casos', descending=True)
                    .head(top_n)
                    .to_dicts()
                )
                result['top_localidades'] = top_localidades
            
            # Top departamentos
            if 'departamento_normalizado' in self.df.columns:
                top_departamentos = (
                    self.df
                    .group_by('departamento_normalizado')
                    .agg(pl.count().alias('casos'))
                    .sort('casos', descending=True)
                    .head(top_n)
                    .to_dicts()
                )
                result['top_departamentos'] = top_departamentos
            
            # Top establecimientos
            if 'establecimiento_notificador_normalizada' in self.df.columns:
                top_establecimientos = (
                    self.df
                    .group_by('establecimiento_notificador_normalizada')
                    .agg(pl.count().alias('casos'))
                    .sort('casos', descending=True)
                    .head(top_n)
                    .to_dicts()
                )
                result['top_establecimientos'] = top_establecimientos
            
            return result
        except Exception as e:
            logger.error(f"Error en análisis geográfico: {e}")
            return {'error': str(e)}
    
    def analyze_laboratory_results(self) -> Dict[str, Any]:
        try:
            result = {}
            
            # Distribución RT-PCR
            if 'rt_pcr_tiempo_real_dengue_normalizado' in self.df.columns:
                pcr_dist = (
                    self.df
                    .group_by('rt_pcr_tiempo_real_dengue_normalizado')
                    .agg(pl.count().alias('casos'))
                    .sort('casos', descending=True)
                    .to_dicts()
                )
                result['distribucion_pcr'] = pcr_dist
                
                # Tasa de positividad
                total_testeados = self.df.filter(
                    pl.col('rt_pcr_tiempo_real_dengue_normalizado') != 'no realizado'
                ).height
                
                positivos = self.df.filter(
                    pl.col('rt_pcr_tiempo_real_dengue_normalizado') == 'positivo'
                ).height
                
                result['tasa_positividad'] = (positivos / total_testeados * 100) if total_testeados > 0 else 0
                result['casos_positivos'] = positivos
                result['total_testeados'] = total_testeados
                result['no_realizados'] = self.df.height - total_testeados
            
            # Distribución de serotipos
            if 'serotipo_virus_dengue_normalizado' in self.df.columns:
                serotipos = (
                    self.df
                    .filter(pl.col('serotipo_virus_dengue_normalizado').is_not_null())
                    .group_by('serotipo_virus_dengue_normalizado')
                    .agg(pl.count().alias('casos'))
                    .sort('casos', descending=True)
                    .to_dicts()
                )
                result['distribucion_serotipos'] = serotipos
            
            return result
        except Exception as e:
            logger.error(f"Error en análisis de laboratorio: {e}")
            return {'error': str(e)}
    
    def analyze_demographics(self) -> Dict[str, Any]:
        try:
            result = {}
            
            # Estadísticas de edad
            if 'edad' in self.df.columns:
                edad_stats = self.df.select([
                    pl.col('edad').mean().alias('edad_promedio'),
                    pl.col('edad').median().alias('edad_mediana'),
                    pl.col('edad').std().alias('edad_std'),
                    pl.col('edad').min().alias('edad_min'),
                    pl.col('edad').max().alias('edad_max')
                ]).to_dicts()[0]
                
                result['estadisticas_edad'] = edad_stats
            
            # Distribución por grupos etarios
            if 'grupo_etario' in self.df.columns:
                grupos_etarios = (
                    self.df
                    .group_by('grupo_etario')
                    .agg([
                        pl.count().alias('casos'),
                        pl.col('dias_evolucion').mean().alias('dias_evolucion_promedio') if 'dias_evolucion' in self.df.columns else pl.lit(None).alias('dias_evolucion_promedio')
                    ])
                    .sort('casos', descending=True)
                    .to_dicts()
                )
                result['distribucion_grupos_etarios'] = grupos_etarios
            
            # Análisis por sexo si está disponible
            if 'sexo' in self.df.columns:
                distribucion_sexo = (
                    self.df
                    .group_by('sexo')
                    .agg(pl.count().alias('casos'))
                    .to_dicts()
                )
                result['distribucion_sexo'] = distribucion_sexo
            
            return result
        except Exception as e:
            logger.error(f"Error en análisis demográfico: {e}")
            return {'error': str(e)}
    
    def analyze_temporal_trends(self) -> Dict[str, Any]:
        try:
            result = {}
            
            # Usar columnas de fecha ya procesadas por el backend si están disponibles
            if 'anio_recepcion' in self.df.columns and 'mes_recepcion' in self.df.columns:
                try:
                    # Casos por mes usando columnas ya procesadas
                    casos_mensuales = (
                        self.df
                        .filter(pl.col('anio_recepcion').is_not_null() & pl.col('mes_recepcion').is_not_null())
                        .group_by(['anio_recepcion', 'mes_recepcion'])
                        .agg(pl.count().alias('casos'))
                        .sort(['anio_recepcion', 'mes_recepcion'])
                        .rename({'anio_recepcion': 'año', 'mes_recepcion': 'mes'})
                        .to_dicts()
                    )
                    result['casos_mensuales'] = casos_mensuales
                except Exception as e:
                    logger.warning(f"Error procesando casos mensuales: {e}")
                    result['casos_mensuales'] = []
                    
            elif 'fecha_recepcion_date' in self.df.columns:
                try:
                    # Si existe la columna de fecha procesada, usarla
                    casos_mensuales = (
                        self.df
                        .filter(pl.col('fecha_recepcion_date').is_not_null())
                        .with_columns([
                            pl.col('fecha_recepcion_date').dt.year().alias('año'),
                            pl.col('fecha_recepcion_date').dt.month().alias('mes')
                        ])
                        .group_by(['año', 'mes'])
                        .agg(pl.count().alias('casos'))
                        .sort(['año', 'mes'])
                        .to_dicts()
                    )
                    result['casos_mensuales'] = casos_mensuales
                except Exception as e:
                    logger.warning(f"Error procesando fecha_recepcion_date: {e}")
                    result['casos_mensuales'] = []
                    
            elif 'fecha_recepcion' in self.df.columns:
                try:
                    # Procesar fecha_recepcion string usando Polars
                    df_with_dates = self.df.with_columns(
                        pl.coalesce([
                            pl.col('fecha_recepcion').str.strptime(pl.Date, format='%Y-%m-%d', strict=False),
                            pl.col('fecha_recepcion').str.strptime(pl.Date, format='%d/%m/%Y', strict=False),
                            pl.col('fecha_recepcion').str.strptime(pl.Date, format='%Y/%m/%d', strict=False)
                        ]).alias('fecha_parsed')
                    )
                    
                    casos_mensuales = (
                        df_with_dates
                        .filter(pl.col('fecha_parsed').is_not_null())
                        .with_columns([
                            pl.col('fecha_parsed').dt.year().alias('año'),
                            pl.col('fecha_parsed').dt.month().alias('mes')
                        ])
                        .group_by(['año', 'mes'])
                        .agg(pl.count().alias('casos'))
                        .sort(['año', 'mes'])
                        .to_dicts()
                    )
                    result['casos_mensuales'] = casos_mensuales
                except Exception as e:
                    logger.warning(f"Error procesando fechas con Polars: {e}")
                    result['casos_mensuales'] = []
            else:
                result['casos_mensuales'] = []
            
            # Casos por semana epidemiológica
            if 'sem_epid_recepcion' in self.df.columns:
                try:
                    casos_semanales = (
                        self.df
                        .filter(pl.col('sem_epid_recepcion').is_not_null())
                        .group_by('sem_epid_recepcion')
                        .agg(pl.count().alias('casos'))
                        .sort('sem_epid_recepcion')
                        .to_dicts()
                    )
                    result['casos_semanales'] = casos_semanales
                except Exception as sem_error:
                    logger.warning(f"Error procesando semanas epidemiológicas: {sem_error}")
                    result['casos_semanales'] = []
            else:
                result['casos_semanales'] = []
            
            return result
            
        except Exception as e:
            logger.error(f"Error en análisis temporal: {e}")
            return {'error': str(e), 'casos_mensuales': [], 'casos_semanales': []}
    
    def analyze_processing_efficiency(self) -> Dict[str, Any]:
        try:
            result = {}
            
            if 'demora_dias' in self.df.columns:
                # Estadísticas de demora
                demora_stats = self.df.select([
                    pl.col('demora_dias').mean().alias('demora_promedio'),
                    pl.col('demora_dias').median().alias('demora_mediana'),
                    pl.col('demora_dias').std().alias('demora_std'),
                    pl.col('demora_dias').quantile(0.95).alias('demora_p95')
                ]).to_dicts()[0]
                
                result['estadisticas_demora'] = demora_stats
                
                # Eficiencia por categorías
                mismo_dia = self.df.filter(pl.col('demora_dias') == 0).height
                dentro_24h = self.df.filter(pl.col('demora_dias') <= 1).height
                mas_2_dias = self.df.filter(pl.col('demora_dias') > 2).height
                
                result['metricas_eficiencia'] = {
                    'mismo_dia': mismo_dia,
                    'dentro_24h': dentro_24h,
                    'mas_2_dias': mas_2_dias,
                    'porcentaje_mismo_dia': (mismo_dia / self.df.height * 100) if self.df.height > 0 else 0,
                    'porcentaje_24h': (dentro_24h / self.df.height * 100) if self.df.height > 0 else 0,
                    'porcentaje_mas_2': (mas_2_dias / self.df.height * 100) if self.df.height > 0 else 0
                }
                
                # Demora por establecimiento
                if 'establecimiento_notificador_normalizada' in self.df.columns:
                    demora_por_establecimiento = (
                        self.df
                        .group_by('establecimiento_notificador_normalizada')
                        .agg([
                            pl.count().alias('total_muestras'),
                            pl.col('demora_dias').mean().alias('demora_promedio'),
                            pl.col('demora_dias').median().alias('demora_mediana')
                        ])
                        .filter(pl.col('total_muestras') >= 50)  # Solo establecimientos con >= 50 muestras
                        .sort('demora_promedio', descending=True)
                        .to_dicts()
                    )
                    result['demora_por_establecimiento'] = demora_por_establecimiento
            
            return result
        except Exception as e:
            logger.error(f"Error en análisis de eficiencia: {e}")
            return {'error': str(e)}
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        try:
            # Limpiar datos y crear grupos etarios
            analyzer_cleaned = self.clean_numeric_data()
            analyzer_with_groups = analyzer_cleaned.create_age_groups()
            
            report = {
                'metadatos': {
                    'fecha_generacion': datetime.now().isoformat(),
                    'total_registros': self.df.height,
                    'columnas_disponibles': self.df.columns,
                    'validaciones_aplicadas': {
                        'edad_maxima_permitida': 120,
                        'dias_evolucion_maximo': 365,
                        'demora_maxima_permitida': 365
                    }
                },
                'estadisticas_basicas': analyzer_with_groups.get_basic_stats(),
                'distribucion_geografica': analyzer_with_groups.analyze_geographic_distribution(),
                'resultados_laboratorio': analyzer_with_groups.analyze_laboratory_results(),
                'demografia': analyzer_with_groups.analyze_demographics(),
                'tendencias_temporales': analyzer_with_groups.analyze_temporal_trends(),
                'eficiencia_procesamiento': analyzer_with_groups.analyze_processing_efficiency()
            }
            
            return report
        except Exception as e:
            logger.error(f"Error generando reporte integral: {e}")
            return {'error': str(e), 'metadatos': {'fecha_generacion': datetime.now().isoformat()}}

def create_analyzer_from_api_data(api_data: List[Dict[str, Any]]) -> DengueAnalyzer:
    try:
        if not api_data:
            return DengueAnalyzer(pl.DataFrame())
        
        # Crear DataFrame directamente con Polars
        df_polars = pl.DataFrame(api_data)
        
        # El procesamiento de fechas y datos numéricos ya se hace en el backend
        # Simplemente retornamos el analizador
        return DengueAnalyzer(df_polars)
        
    except Exception as e:
        logger.error(f"Error creando analizador desde API: {e}")
        # Fallback: crear con DataFrame vacío
        return DengueAnalyzer(pl.DataFrame())

def filter_data_by_date_range(df: pl.DataFrame, start_date: str, end_date: str, 
                             date_column: str = 'fecha_recepcion') -> pl.DataFrame:
    """Filtrar datos por rango de fechas"""
    try:
        if date_column not in df.columns:
            return df
        
        filtered_df = df.filter(
            (pl.col(date_column) >= start_date) & 
            (pl.col(date_column) <= end_date)
        )
        return filtered_df
    except Exception as e:
        logger.error(f"Error filtrando por fecha: {e}")
        return df

def filter_data_by_location(df: pl.DataFrame, location: str, 
                           location_column: str = 'localidad_normalizada') -> pl.DataFrame:
    try:
        if location_column not in df.columns or location == 'Todas':
            return df
        
        filtered_df = df.filter(pl.col(location_column) == location)
        return filtered_df
    except Exception as e:
        logger.error(f"Error filtrando por localidad: {e}")
        return df
