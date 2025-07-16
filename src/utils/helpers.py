"""
Funciones auxiliares y herramientas de soporte
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path
from typing import List, Dict, Any

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configura el sistema de logging
    
    Args:
        log_level: Nivel de logging
        
    Returns:
        Logger configurado
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('project.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def create_directory_structure(base_path: str, directories: List[str]):
    """
    Crea estructura de directorios
    
    Args:
        base_path: Ruta base
        directories: Lista de directorios a crear
    """
    base = Path(base_path)
    for directory in directories:
        (base / directory).mkdir(parents=True, exist_ok=True)

def generate_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Genera un resumen completo de un DataFrame
    
    Args:
        df: DataFrame a analizar
        
    Returns:
        Dict: Resumen de los datos
    """
    summary = {
        'shape': df.shape,
        'columns': list(df.columns),
        'data_types': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
        'numerical_summary': df.describe().to_dict(),
        'memory_usage': df.memory_usage(deep=True).to_dict()
    }
    return summary

def plot_missing_values(df: pd.DataFrame, figsize: tuple = (12, 8)):
    """
    Visualiza valores faltantes en el DataFrame
    
    Args:
        df: DataFrame a analizar
        figsize: Tamaño de la figura
    """
    plt.figure(figsize=figsize)
    sns.heatmap(df.isnull(), yticklabels=False, cbar=True, cmap='viridis')
    plt.title('Valores Faltantes por Columna')
    plt.tight_layout()
    plt.show()

def plot_correlation_matrix(df: pd.DataFrame, figsize: tuple = (12, 10)):
    """
    Visualiza matriz de correlación
    
    Args:
        df: DataFrame con variables numéricas
        figsize: Tamaño de la figura
    """
    correlation_matrix = df.select_dtypes(include=['number']).corr()
    
    plt.figure(figsize=figsize)
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5)
    plt.title('Matriz de Correlación')
    plt.tight_layout()
    plt.show()

def print_metrics(metrics: Dict[str, float], title: str = "Métricas del Modelo"):
    """
    Imprime métricas de manera formateada
    
    Args:
        metrics: Diccionario de métricas
        title: Título a mostrar
    """
    print(f"\n{title}")
    print("=" * len(title))
    for metric, value in metrics.items():
        print(f"{metric.capitalize()}: {value:.4f}")
    print()

def save_figure(fig, filename: str, output_dir: str = "output/figures/"):
    """
    Guarda una figura en el directorio especificado
    
    Args:
        fig: Figura de matplotlib
        filename: Nombre del archivo
        output_dir: Directorio de salida
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    file_path = Path(output_dir) / filename
    fig.savefig(file_path, dpi=300, bbox_inches='tight')
    print(f"Figura guardada en: {file_path}")
