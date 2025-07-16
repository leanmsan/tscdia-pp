"""
Script de configuración automática para PySpark + MySQL
Ejecutar antes del primer uso para verificar configuración
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_java():
    """Verificar que Java esté instalado"""
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ Java está instalado")
            return True
    except FileNotFoundError:
        logger.error("❌ Java no encontrado")
        logger.info("💡 Instalar Java 8 o superior: https://www.oracle.com/java/technologies/downloads/")
        return False

def check_python_packages():
    """Verificar que los paquetes necesarios estén instalados"""
    required_packages = [
        'pyspark',
        'mysql-connector-python', 
        'findspark',
        'pyyaml'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            logger.info(f"✅ {package} instalado")
        except ImportError:
            missing_packages.append(package)
            logger.warning(f"❌ {package} no encontrado")
    
    if missing_packages:
        logger.info("💡 Instalar paquetes faltantes:")
        logger.info(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def test_mysql_connection():
    """Probar conexión básica a MySQL"""
    try:
        import mysql.connector
        
        # Configuración de ejemplo (ajustar según necesidad)
        config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',  # Cambiar por tu usuario
            'password': '',  # Cambiar por tu password
            'connection_timeout': 5
        }
        
        logger.info("🔍 Probando conexión a MySQL...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            logger.info(f"✅ MySQL conectado. Versión: {version}")
            connection.close()
            return True
            
    except Exception as e:
        logger.warning(f"⚠️  Conexión MySQL falló: {e}")
        logger.info("💡 Ajustar credenciales en config.yaml")
        return False

def test_spark_setup():
    """Probar configuración básica de Spark"""
    try:
        import findspark
        findspark.init()
        
        from pyspark.sql import SparkSession
        
        logger.info("🔍 Probando configuración de Spark...")
        
        # Crear SparkSession básica
        spark = SparkSession.builder \
            .appName("ConfigTest") \
            .config("spark.jars.packages", "mysql:mysql-connector-java:8.0.33") \
            .getOrCreate()
        
        # Probar funcionalidad básica
        test_df = spark.sql("SELECT 1 as test")
        result = test_df.collect()[0]['test']
        
        if result == 1:
            logger.info("✅ Spark configurado correctamente")
            logger.info(f"   Versión: {spark.version}")
            logger.info(f"   UI: {spark.sparkContext.uiWebUrl}")
            
        spark.stop()
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en configuración Spark: {e}")
        return False

def create_sample_config():
    """Crear archivo de configuración de ejemplo"""
    config_path = Path("config.yaml")
    
    if config_path.exists():
        logger.info("✅ config.yaml ya existe")
        return True
    
    sample_config = """# Configuración de Spark
spark:
  app_name: "TSCDIA-MySQL-Processing"
  master: "local[*]"
  executor_memory: "4g"
  driver_memory: "2g"
  max_result_size: "2g"
  sql_adaptive_enabled: true
  mysql_jar_packages: "mysql:mysql-connector-java:8.0.33"

# Configuración de MySQL
databases:
  mysql:
    host: "localhost"
    port: 3306
    database: "tu_database"
    user: "tu_usuario"
    password: "tu_password"
    driver: "com.mysql.cj.jdbc.Driver"
    
    connection_options:
      useSSL: false
      allowPublicKeyRetrieval: true
      serverTimezone: "UTC"
      characterEncoding: "utf8"
      useUnicode: true
      autoReconnect: true
      
    performance:
      fetchSize: 1000
      batchSize: 1000
      queryTimeout: 3600
"""
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(sample_config)
        logger.info("✅ config.yaml creado")
        logger.info("💡 Ajustar credenciales MySQL en config.yaml")
        return True
    except Exception as e:
        logger.error(f"❌ Error creando config.yaml: {e}")
        return False

def main():
    """Función principal de verificación"""
    logger.info("🚀 VERIFICACIÓN DE CONFIGURACIÓN PYSPARK + MYSQL")
    logger.info("=" * 50)
    
    checks = [
        ("Java", check_java),
        ("Paquetes Python", check_python_packages),
        ("Configuración", create_sample_config),
        ("Spark", test_spark_setup),
        ("MySQL", test_mysql_connection)
    ]
    
    results = {}
    
    for name, check_func in checks:
        logger.info(f"\n🔍 Verificando {name}...")
        results[name] = check_func()
    
    # Resumen
    logger.info("\n" + "=" * 50)
    logger.info("📊 RESUMEN DE VERIFICACIÓN")
    logger.info("=" * 50)
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ OK" if passed else "❌ FALLA"
        logger.info(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        logger.info("\n🎉 ¡CONFIGURACIÓN COMPLETA!")
        logger.info("💡 Puedes usar notebooks/04_mysql_spark.ipynb")
    else:
        logger.info("\n⚠️  CONFIGURACIÓN INCOMPLETA")
        logger.info("💡 Revisar elementos marcados como FALLA")
    
    logger.info("\n📚 RECURSOS ÚTILES:")
    logger.info("   - Notebook: notebooks/04_mysql_spark.ipynb")
    logger.info("   - Módulo: src/etl/mysql_spark.py")
    logger.info("   - Config: config.yaml")

if __name__ == "__main__":
    main()
