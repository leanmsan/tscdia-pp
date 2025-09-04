import polars as pl
from typing import List, Dict, Any
import logging
from datetime import datetime

from app.data.repositories.laboratorio_dengue_repository import get_laboratorio_dengue_data
from app.data.processors.dengue_processor import DengueDataProcessor

logger = logging.getLogger(__name__)

class LaboratorioDengueService:
    def __init__(self, max_workers: int = None, chunk_size: int = 1000):
        self.processor = DengueDataProcessor(max_workers=max_workers, chunk_size=chunk_size)
    
    async def obtener_datos_procesados(self) -> List[Dict[str, Any]]:
        logger.info('Obteniendo datos raw de la base de datos')
        
        raw_data = await get_laboratorio_dengue_data()
        
        if not raw_data:
            logger.warning('No se encontraron datos en la base de datos')
            return []
        
        logger.info(f'Convirtiendo {len(raw_data)} registros a DataFrame de Polars')
        
        def normalizar_valor(valor):
            if valor is None:
                return None
            if hasattr(valor, 'strftime'):
                return valor.strftime('%Y-%m-%d')
            return valor
        
        data_dicts = []
        for row in raw_data:
            row_dict = {}
            for key, value in row._mapping.items():
                row_dict[key] = normalizar_valor(value)
            data_dicts.append(row_dict)
        
        try:
            df = pl.DataFrame(data_dicts, infer_schema_length=None)
            logger.info('DataFrame creado exitosamente con inferencia automática')
        except Exception as e:
            logger.warning(f'Error con inferencia automática: {e}')
            try:
                logger.info('Intentando crear DataFrame con todos los valores como string')
                
                data_dicts_str = []
                for row_dict in data_dicts:
                    str_dict = {}
                    for key, value in row_dict.items():
                        if value is None:
                            str_dict[key] = None
                        else:
                            str_dict[key] = str(value)
                    data_dicts_str.append(str_dict)
                
                df = pl.DataFrame(data_dicts_str)
                logger.info('DataFrame creado exitosamente con conversión a string')
                
            except Exception as e2:
                logger.error(f'Error crítico creando DataFrame: {e2}')
                raise e2
        
        logger.info(f'DataFrame creado con shape: {df.shape}')
        
        df_processed = self.processor.procesar_datos_paralelo(df)
        
        result = df_processed.to_dicts()
        
        logger.info(f'Procesamiento completado. {len(result)} registros procesados')
        
        return result
    
    async def obtener_datos_raw(self) -> List[Dict[str, Any]]:
        raw_data = await get_laboratorio_dengue_data()
        
        if not raw_data:
            return []
        
        return [dict(row._mapping) for row in raw_data]
    
    async def obtener_kpis_basicos(self) -> Dict[str, Any]:
        datos_procesados = await self.obtener_datos_procesados()
        
        if not datos_procesados:
            return {'error': 'No hay datos disponibles'}
        
        df = pl.DataFrame(datos_procesados)
        
        total_casos = len(df)
        
        top_localidades = (
            df.group_by('localidad_normalizada')
            .agg(pl.count().alias('casos'))
            .sort('casos', descending=True)
            .head(10)
            .to_dicts()
        )
        
        distribucion_pcr = (
            df.group_by('rt_pcr_tiempo_real_dengue_normalizado')
            .agg(pl.count().alias('casos'))
            .sort('casos', descending=True)
            .to_dicts()
        )
        
        demora_promedio = None
        if 'demora_dias' in df.columns:
            try:
                demora_promedio = df.select(pl.col('demora_dias').mean()).item()
            except Exception as e:
                logger.warning(f'Error calculando demora promedio: {e}')
        
        return {
            'total_casos': total_casos,
            'top_localidades': top_localidades,
            'distribucion_pcr': distribucion_pcr,
            'demora_promedio_dias': round(demora_promedio, 2) if demora_promedio else None,
            'fecha_procesamiento': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
