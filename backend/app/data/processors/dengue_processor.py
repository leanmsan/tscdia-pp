import polars as pl
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict, Any
import logging
from datetime import datetime

from .localidad_processor import normalizar_localidad
from .departamento_processor import normalizar_departamento
from .laboratorio_processor import normalizar_laboratorio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def procesar_chunk_localidades(chunk_data: List[str]) -> List[str]:
    return [normalizar_localidad(loc) for loc in chunk_data]

def procesar_chunk_departamentos(chunk_data: List[str]) -> List[str]:
    return [normalizar_departamento(dept) for dept in chunk_data]

def procesar_chunk_laboratorio(chunk_data: List[str]) -> List[str]:
    return [normalizar_laboratorio(lab) for lab in chunk_data]

def dividir_en_chunks(data: List[Any], chunk_size: int = 1000) -> List[List[Any]]:
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

class DengueDataProcessor:
    def __init__(self, max_workers: int = None, chunk_size: int = 1000):
        self.max_workers = max_workers
        self.chunk_size = chunk_size
        
    def procesar_datos_paralelo(self, df: pl.DataFrame) -> pl.DataFrame:
        logger.info('Iniciando procesamiento paralelo de datos de dengue')
        start_time = datetime.now()
        
        df_processed = df.clone()
        
        if 'localidad' in df.columns:
            logger.info('Procesando localidades...')
            localidades_normalizadas = self._procesar_columna_paralelo(
                df['localidad'].to_list(),
                procesar_chunk_localidades
            )
            df_processed = df_processed.with_columns(
                pl.Series('localidad_normalizada', localidades_normalizadas)
            )
        
        if 'departamento' in df.columns:
            logger.info('Procesando departamentos...')
            departamentos_normalizados = self._procesar_columna_paralelo(
                df['departamento'].to_list(),
                procesar_chunk_departamentos
            )
            df_processed = df_processed.with_columns(
                pl.Series('departamento_normalizado', departamentos_normalizados)
            )
        
        columnas_laboratorio = [
            'rt_pcr_tiempo_real_dengue',
            'serotipo_virus_dengue',
            'igg_test_rapido',
            'ns1_elisa',
            'ig_m_dengue_elisa'
        ]
        
        for col in columnas_laboratorio:
            if col in df.columns:
                logger.info(f'Procesando columna de laboratorio: {col}')
                resultados_normalizados = self._procesar_columna_paralelo(
                    df[col].to_list(),
                    procesar_chunk_laboratorio
                )
                df_processed = df_processed.with_columns(
                    pl.Series(f'{col}_normalizado', resultados_normalizados)
                )
        
        df_processed = self._calcular_campos_derivados(df_processed)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f'Procesamiento completado en {duration:.2f} segundos')
        
        return df_processed
    
    def _procesar_columna_paralelo(self, data: List[Any], func_procesamiento) -> List[Any]:
        if not data:
            return []
        
        chunks = dividir_en_chunks(data, self.chunk_size)
        resultados = [None] * len(chunks)
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_index = {
                executor.submit(func_procesamiento, chunk): i 
                for i, chunk in enumerate(chunks)
            }
            
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    resultados[index] = future.result()
                except Exception as exc:
                    logger.error(f'Chunk {index} generó excepción: {exc}')
                    resultados[index] = ['DESCONOCIDO'] * len(chunks[index])
        
        resultado_final = []
        for chunk_resultado in resultados:
            resultado_final.extend(chunk_resultado)
        
        return resultado_final
    
    def _calcular_campos_derivados(self, df: pl.DataFrame) -> pl.DataFrame:
        df_with_derived = df
        
        fecha_cols = ['fecha_recepcion', 'fecha_procesamiento', 'fecha_inicio_fiebre']
        for col in fecha_cols:
            if col in df.columns:
                try:
                    df_with_derived = df_with_derived.with_columns(
                        pl.coalesce([
                            pl.col(col).str.strptime(pl.Date, format='%Y-%m-%d', strict=False),
                            pl.col(col).str.strptime(pl.Date, format='%d/%m/%Y', strict=False),
                            pl.col(col).str.strptime(pl.Date, format='%Y/%m/%d', strict=False)
                        ]).alias(f'{col}_date')
                    )
                    logger.info(f'Columna {col} convertida exitosamente')
                except Exception as e:
                    logger.warning(f'Error convirtiendo fecha en columna {col}: {e}')
                    df_with_derived = df_with_derived.with_columns(
                        pl.lit(None).cast(pl.Date).alias(f'{col}_date')
                    )
        
        if 'fecha_recepcion_date' in df_with_derived.columns and 'fecha_procesamiento_date' in df_with_derived.columns:
            try:
                df_with_derived = df_with_derived.with_columns([
                    (pl.col('fecha_procesamiento_date') - pl.col('fecha_recepcion_date')).dt.total_days().alias('demora_dias'),
                    ((pl.col('fecha_procesamiento_date') - pl.col('fecha_recepcion_date')).dt.total_days() * 24).alias('demora_horas')
                ])
                logger.info('Demoras calculadas exitosamente')
            except Exception as e:
                logger.warning(f'Error calculando demoras: {e}')
                df_with_derived = df_with_derived.with_columns([
                    pl.lit(None).cast(pl.Float64).alias('demora_dias'),
                    pl.lit(None).cast(pl.Float64).alias('demora_horas')
                ])
        
        if 'fecha_recepcion_date' in df_with_derived.columns:
            try:
                df_with_derived = df_with_derived.with_columns([
                    pl.col('fecha_recepcion_date').dt.year().alias('anio_recepcion'),
                    pl.col('fecha_recepcion_date').dt.month().alias('mes_recepcion'),
                    pl.col('fecha_recepcion_date').dt.week().alias('sem_epid_recepcion')
                ])
                logger.info('Campos temporales calculados exitosamente')
            except Exception as e:
                logger.warning(f'Error calculando campos temporales: {e}')
                df_with_derived = df_with_derived.with_columns([
                    pl.lit(None).cast(pl.Int32).alias('anio_recepcion'),
                    pl.lit(None).cast(pl.Int32).alias('mes_recepcion'),
                    pl.lit(None).cast(pl.Int32).alias('sem_epid_recepcion')
                ])
        
        numeric_cols = ['edad', 'dias_evolucion']
        for col in numeric_cols:
            if col in df.columns:
                try:
                    df_with_derived = df_with_derived.with_columns(
                        pl.col(col).cast(pl.Utf8, strict=False)
                        .str.replace_all(r'[^\d]', '')
                        .cast(pl.Int32, strict=False)
                        .fill_null(0)
                        .alias(col)
                    )
                    logger.info(f'Columna numérica {col} normalizada exitosamente')
                except Exception as e:
                    logger.warning(f'Error normalizando columna numérica {col}: {e}')
                    df_with_derived = df_with_derived.with_columns(
                        pl.lit(0).cast(pl.Int32).alias(col)
                    )
        
        return df_with_derived
