"""
Módulo para trabajar con PySpark y bases de datos
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql.functions import col, when, isnan, count, desc, asc
import yaml
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SparkDataLoader:
    """Clase para manejar operaciones con Spark y bases de datos"""
    
    def __init__(self, app_name: str = "TSCDIA-DataProcessing", config_path: str = "config.yaml"):
        """
        Inicializar SparkSession
        
        Args:
            app_name: Nombre de la aplicación Spark
            config_path: Ruta al archivo de configuración
        """
        self.config = self._load_config(config_path)
        self.spark = self._create_spark_session(app_name)
        
    def _load_config(self, config_path: str) -> dict:
        """Cargar configuración desde YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {}
    
    def _create_spark_session(self, app_name: str) -> SparkSession:
        """
        Crear y configurar SparkSession
        
        Args:
            app_name: Nombre de la aplicación
            
        Returns:
            SparkSession configurada
        """
        builder = SparkSession.builder.appName(app_name)
        
        # Configuraciones básicas
        builder = builder.config("spark.sql.adaptive.enabled", "true")
        builder = builder.config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        
        # Configurar drivers de bases de datos
        # PostgreSQL
        builder = builder.config("spark.jars.packages", 
                               "org.postgresql:postgresql:42.5.4")
        
        # MySQL (opcional)
        # builder = builder.config("spark.jars.packages", 
        #                        "mysql:mysql-connector-java:8.0.33")
        
        # SQL Server (opcional)
        # builder = builder.config("spark.jars.packages", 
        #                        "com.microsoft.sqlserver:mssql-jdbc:11.2.3.jre8")
        
        return builder.getOrCreate()
    
    def read_from_postgres(self, query: str, **connection_params) -> 'DataFrame':
        """
        Leer datos desde PostgreSQL
        
        Args:
            query: Query SQL o nombre de tabla
            **connection_params: Parámetros de conexión
            
        Returns:
            Spark DataFrame
        """
        default_params = {
            "url": "jdbc:postgresql://localhost:5432/database",
            "user": "username",
            "password": "password",
            "driver": "org.postgresql.Driver"
        }
        
        # Merge con parámetros personalizados
        conn_params = {**default_params, **connection_params}
        
        # Si es una tabla completa
        if not query.strip().upper().startswith('SELECT'):
            return self.spark.read.format("jdbc") \
                .option("url", conn_params["url"]) \
                .option("dbtable", query) \
                .option("user", conn_params["user"]) \
                .option("password", conn_params["password"]) \
                .option("driver", conn_params["driver"]) \
                .load()
        
        # Si es una query personalizada
        return self.spark.read.format("jdbc") \
            .option("url", conn_params["url"]) \
            .option("query", query) \
            .option("user", conn_params["user"]) \
            .option("password", conn_params["password"]) \
            .option("driver", conn_params["driver"]) \
            .load()
    
    def read_from_mysql(self, table_or_query: str, **connection_params) -> 'DataFrame':
        """
        Leer datos desde MySQL
        
        Args:
            table_or_query: Nombre de tabla o query SQL
            **connection_params: Parámetros de conexión
            
        Returns:
            Spark DataFrame
        """
        default_params = {
            "url": "jdbc:mysql://localhost:3306/database",
            "user": "username",
            "password": "password",
            "driver": "com.mysql.cj.jdbc.Driver"
        }
        
        conn_params = {**default_params, **connection_params}
        
        return self.spark.read.format("jdbc") \
            .option("url", conn_params["url"]) \
            .option("dbtable", table_or_query) \
            .option("user", conn_params["user"]) \
            .option("password", conn_params["password"]) \
            .option("driver", conn_params["driver"]) \
            .load()
    
    def read_partitioned_table(self, table: str, partition_column: str, 
                             num_partitions: int = 4, **connection_params) -> 'DataFrame':
        """
        Leer tabla con particionado para mejor rendimiento
        
        Args:
            table: Nombre de la tabla
            partition_column: Columna para particionar
            num_partitions: Número de particiones
            **connection_params: Parámetros de conexión
            
        Returns:
            Spark DataFrame particionado
        """
        conn_params = {
            "url": "jdbc:postgresql://localhost:5432/database",
            "user": "username", 
            "password": "password",
            "driver": "org.postgresql.Driver",
            **connection_params
        }
        
        return self.spark.read.format("jdbc") \
            .option("url", conn_params["url"]) \
            .option("dbtable", table) \
            .option("user", conn_params["user"]) \
            .option("password", conn_params["password"]) \
            .option("driver", conn_params["driver"]) \
            .option("partitionColumn", partition_column) \
            .option("numPartitions", num_partitions) \
            .load()
    
    def write_to_database(self, df: 'DataFrame', table: str, mode: str = "overwrite", 
                         **connection_params):
        """
        Escribir DataFrame a base de datos
        
        Args:
            df: Spark DataFrame
            table: Nombre de la tabla destino
            mode: Modo de escritura (overwrite, append, ignore, error)
            **connection_params: Parámetros de conexión
        """
        conn_params = {
            "url": "jdbc:postgresql://localhost:5432/database",
            "user": "username",
            "password": "password", 
            "driver": "org.postgresql.Driver",
            **connection_params
        }
        
        df.write.format("jdbc") \
            .option("url", conn_params["url"]) \
            .option("dbtable", table) \
            .option("user", conn_params["user"]) \
            .option("password", conn_params["password"]) \
            .option("driver", conn_params["driver"]) \
            .mode(mode) \
            .save()
    
    def basic_data_quality_check(self, df: 'DataFrame') -> Dict[str, Any]:
        """
        Realizar checks básicos de calidad de datos
        
        Args:
            df: Spark DataFrame
            
        Returns:
            Dict con métricas de calidad
        """
        total_rows = df.count()
        total_cols = len(df.columns)
        
        # Contar nulls por columna
        null_counts = {}
        for col_name in df.columns:
            null_count = df.filter(col(col_name).isNull()).count()
            null_counts[col_name] = {
                'null_count': null_count,
                'null_percentage': (null_count / total_rows) * 100
            }
        
        return {
            'total_rows': total_rows,
            'total_columns': total_cols,
            'null_analysis': null_counts,
            'schema': str(df.schema)
        }
    
    def save_to_parquet(self, df: 'DataFrame', path: str, partition_by: Optional[str] = None):
        """
        Guardar DataFrame como Parquet
        
        Args:
            df: Spark DataFrame
            path: Ruta de destino
            partition_by: Columna para particionar (opcional)
        """
        writer = df.write.mode("overwrite").option("compression", "snappy")
        
        if partition_by:
            writer = writer.partitionBy(partition_by)
            
        writer.parquet(path)
        logger.info(f"Datos guardados en: {path}")
    
    def stop_spark(self):
        """Detener SparkSession"""
        if self.spark:
            self.spark.stop()
            logger.info("SparkSession detenida")

# Funciones de utilidad
def create_spark_loader(app_name: str = "TSCDIA", config_path: str = "config.yaml") -> SparkDataLoader:
    """
    Factory function para crear SparkDataLoader
    
    Args:
        app_name: Nombre de la aplicación
        config_path: Ruta al archivo de configuración
        
    Returns:
        Instancia de SparkDataLoader
    """
    return SparkDataLoader(app_name, config_path)
