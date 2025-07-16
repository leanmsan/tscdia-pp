"""
Funciones para carga de datos desde diferentes fuentes
"""

import pandas as pd
import yaml
from pathlib import Path

def load_config(config_path: str = "config.yaml") -> dict:
    """
    Carga la configuración del proyecto desde un archivo YAML
    
    Args:
        config_path: Ruta al archivo de configuración
        
    Returns:
        dict: Configuración del proyecto
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def load_csv_data(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Carga datos desde un archivo CSV
    
    Args:
        file_path: Ruta al archivo CSV
        **kwargs: Argumentos adicionales para pd.read_csv()
        
    Returns:
        pd.DataFrame: Datos cargados
    """
    return pd.read_csv(file_path, **kwargs)

def save_processed_data(df: pd.DataFrame, file_name: str, output_dir: str = "data/processed/"):
    """
    Guarda datos procesados en formato CSV
    
    Args:
        df: DataFrame a guardar
        file_name: Nombre del archivo
        output_dir: Directorio de salida
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    file_path = Path(output_dir) / file_name
    df.to_csv(file_path, index=False)
    print(f"Datos guardados en: {file_path}")
