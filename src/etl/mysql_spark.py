"""
Módulo especializado para PySpark con MySQL
Configuración optimizada y sin problemas de conectividad
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import yaml
import mysql.connector
from urllib.parse import quote_plus
import logging
from typing import Dict, Any, Optional, List
import os

logger = logging.getLogger(__name__)

class MySQLSparkConnector:
    """Conector especializado para MySQL con PySpark"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Inicializar conector MySQL + Spark
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        self.config = self._load_config(config_path)
        self.spark = None
        self.mysql_config = self.config.get('databases', {}).get('mysql', {})
        self._setup_spark()
        
    def _load_config(self, config_path: str) -> dict:
        """Cargar configuración desde YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Configuración por defecto"""
        return {
            'spark': {
                'app_name': 'TSCDIA-MySQL',
                'master': 'local[*]',
                'executor_memory': '4g',
                'driver_memory': '2g'
            },
            'databases': {
                'mysql': {
                    'host': 'localhost',
                    'port': 3306,
                    'database': 'tscdia_db',
                    'user': 'root',
                    'password': 'password'
                }
            }
        }
    
    def _setup_spark(self):
        """Configurar SparkSession optimizado para MySQL"""
        spark_config = self.config.get('spark', {})
        
        # Crear SparkSession con configuración MySQL
        builder = SparkSession.builder.appName(spark_config.get('app_name', 'TSCDIA-MySQL'))
        
        # Configuraciones de memoria y performance
        builder = builder.config("spark.driver.memory", spark_config.get('driver_memory', '2g'))
        builder = builder.config("spark.executor.memory", spark_config.get('executor_memory', '4g'))
        builder = builder.config("spark.sql.adaptive.enabled", "true")
        builder = builder.config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        
        # IMPORTANTE: Configurar el driver MySQL automáticamente
        builder = builder.config("spark.jars.packages", "mysql:mysql-connector-java:8.0.33")
        
        # Configuraciones adicionales para mejor rendimiento con MySQL
        builder = builder.config("spark.sql.execution.arrow.pyspark.enabled", "true")
        builder = builder.config("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB")
        
        try:
            self.spark = builder.getOrCreate()
            self.spark.sparkContext.setLogLevel("WARN")  # Reducir logs verbosos
            logger.info("✅ SparkSession creada exitosamente para MySQL")
        except Exception as e:
            logger.error(f"❌ Error creando SparkSession: {e}")
            raise
    
    def test_mysql_connection(self) -> bool:
        """
        Probar conectividad directa a MySQL
        
        Returns:
            bool: True si la conexión es exitosa
        """
        try:
            connection = mysql.connector.connect(
                host=self.mysql_config.get('host', 'localhost'),
                port=self.mysql_config.get('port', 3306),
                user=self.mysql_config.get('user', 'root'),
                password=self.mysql_config.get('password', ''),
                database=self.mysql_config.get('database', 'test'),
                connection_timeout=10
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                logger.info(f"✅ Conexión MySQL exitosa. Versión: {version}")
                connection.close()
                return True
                
        except Exception as e:
            logger.error(f"❌ Error conectando a MySQL: {e}")
            return False
    
    def get_mysql_url(self) -> str:
        """
        Construir URL de conexión MySQL para Spark
        
        Returns:
            str: URL de conexión JDBC
        """
        host = self.mysql_config.get('host', 'localhost')
        port = self.mysql_config.get('port', 3306)
        database = self.mysql_config.get('database', 'test')
        
        # Opciones de conexión
        options = self.mysql_config.get('connection_options', {})
        option_str = "&".join([f"{k}={v}" for k, v in options.items()])
        
        base_url = f"jdbc:mysql://{host}:{port}/{database}"
        if option_str:
            base_url += f"?{option_str}"
            
        return base_url
    
    def get_connection_properties(self) -> Dict[str, str]:
        """
        Obtener propiedades de conexión para Spark
        
        Returns:
            Dict con propiedades de conexión
        """
        return {
            "user": self.mysql_config.get('user', 'root'),
            "password": self.mysql_config.get('password', ''),
            "driver": "com.mysql.cj.jdbc.Driver",
            "fetchsize": str(self.mysql_config.get('performance', {}).get('fetchSize', 1000)),
            "batchsize": str(self.mysql_config.get('performance', {}).get('batchSize', 1000))
        }
    
    def read_table(self, table_name: str, sample_fraction: float = None) -> 'DataFrame':
        """
        Leer tabla completa de MySQL
        
        Args:
            table_name: Nombre de la tabla
            sample_fraction: Fracción para sampling (0.0 a 1.0)
            
        Returns:
            Spark DataFrame
        """
        try:
            url = self.get_mysql_url()
            properties = self.get_connection_properties()
            
            df = self.spark.read.jdbc(
                url=url,
                table=table_name,
                properties=properties
            )
            
            if sample_fraction and 0 < sample_fraction < 1:
                df = df.sample(fraction=sample_fraction, seed=42)
                
            logger.info(f"✅ Tabla '{table_name}' cargada exitosamente")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error leyendo tabla '{table_name}': {e}")
            raise
    
    def read_query(self, query: str) -> 'DataFrame':
        """
        Ejecutar query personalizada en MySQL
        
        Args:
            query: Query SQL a ejecutar
            
        Returns:
            Spark DataFrame
        """
        try:
            url = self.get_mysql_url()
            properties = self.get_connection_properties()
            
            # Para queries personalizadas, usar subquery
            subquery = f"({query}) as subquery"
            
            df = self.spark.read.jdbc(
                url=url,
                table=subquery,
                properties=properties
            )
            
            logger.info("✅ Query ejecutada exitosamente")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error ejecutando query: {e}")
            raise
    
    def read_partitioned(self, table_name: str, partition_column: str, 
                        lower_bound: int, upper_bound: int, 
                        num_partitions: int = 4) -> 'DataFrame':
        """
        Leer tabla con particionado para mejor rendimiento
        
        Args:
            table_name: Nombre de la tabla
            partition_column: Columna numérica para particionar
            lower_bound: Valor mínimo de la columna
            upper_bound: Valor máximo de la columna
            num_partitions: Número de particiones
            
        Returns:
            Spark DataFrame particionado
        """
        try:
            url = self.get_mysql_url()
            properties = self.get_connection_properties()
            
            df = self.spark.read.jdbc(
                url=url,
                table=table_name,
                column=partition_column,
                lowerBound=lower_bound,
                upperBound=upper_bound,
                numPartitions=num_partitions,
                properties=properties
            )
            
            logger.info(f"✅ Tabla '{table_name}' cargada con {num_partitions} particiones")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error leyendo tabla particionada: {e}")
            raise
    
    def write_table(self, df: 'DataFrame', table_name: str, 
                   mode: str = "overwrite", batch_size: int = 1000):
        """
        Escribir DataFrame a MySQL
        
        Args:
            df: Spark DataFrame
            table_name: Nombre de la tabla destino
            mode: Modo de escritura (overwrite, append, ignore, error)
            batch_size: Tamaño del batch
        """
        try:
            url = self.get_mysql_url()
            properties = self.get_connection_properties()
            properties["batchsize"] = str(batch_size)
            
            df.write.jdbc(
                url=url,
                table=table_name,
                mode=mode,
                properties=properties
            )
            
            logger.info(f"✅ Datos escritos en tabla '{table_name}' exitosamente")
            
        except Exception as e:
            logger.error(f"❌ Error escribiendo a tabla '{table_name}': {e}")
            raise
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Obtener información sobre una tabla
        
        Args:
            table_name: Nombre de la tabla
            
        Returns:
            Dict con información de la tabla
        """
        try:
            # Leer muestra pequeña para obtener schema
            sample_df = self.read_query(f"SELECT * FROM {table_name} LIMIT 1")
            
            # Obtener conteo total
            count_df = self.read_query(f"SELECT COUNT(*) as total FROM {table_name}")
            total_rows = count_df.collect()[0]['total']
            
            return {
                'table_name': table_name,
                'total_rows': total_rows,
                'columns': sample_df.columns,
                'schema': sample_df.schema,
                'dtypes': sample_df.dtypes
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo info de tabla '{table_name}': {e}")
            return {}
    
    def list_tables(self, database: str = None) -> List[str]:
        """
        Listar todas las tablas disponibles
        
        Args:
            database: Base de datos específica (opcional)
            
        Returns:
            Lista de nombres de tablas
        """
        try:
            if database:
                query = f"SHOW TABLES FROM {database}"
            else:
                query = "SHOW TABLES"
                
            tables_df = self.read_query(query)
            tables = [row[0] for row in tables_df.collect()]
            
            logger.info(f"✅ Encontradas {len(tables)} tablas")
            return tables
            
        except Exception as e:
            logger.error(f"❌ Error listando tablas: {e}")
            return []
    
    def optimize_dataframe(self, df: 'DataFrame', cache: bool = True) -> 'DataFrame':
        """
        Optimizar DataFrame para mejor rendimiento
        
        Args:
            df: Spark DataFrame
            cache: Si cachear el DataFrame
            
        Returns:
            DataFrame optimizado
        """
        # Coalesce particiones si hay muchas pequeñas
        partition_count = df.rdd.getNumPartitions()
        if partition_count > 200:
            df = df.coalesce(partition_count // 4)
        
        # Cache si se solicita
        if cache:
            df = df.cache()
            
        return df
    
    def close(self):
        """Cerrar SparkSession"""
        if self.spark:
            self.spark.stop()
            logger.info("✅ SparkSession cerrada")

# Función helper para crear conector fácilmente
def create_mysql_spark_connector(config_path: str = "config.yaml") -> MySQLSparkConnector:
    """
    Factory function para crear MySQLSparkConnector
    
    Args:
        config_path: Ruta al archivo de configuración
        
    Returns:
        MySQLSparkConnector configurado
    """
    return MySQLSparkConnector(config_path)
