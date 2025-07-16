"""
Funciones para limpieza y transformación de datos
"""

import pandas as pd
import numpy as np
from typing import List, Tuple

def clean_missing_values(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
    """
    Maneja valores faltantes en el DataFrame
    
    Args:
        df: DataFrame de entrada
        strategy: Estrategia para manejar valores faltantes ('drop', 'mean', 'median', 'mode')
        
    Returns:
        pd.DataFrame: DataFrame limpio
    """
    df_clean = df.copy()
    
    if strategy == 'drop':
        df_clean = df_clean.dropna()
    elif strategy == 'mean':
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
    elif strategy == 'median':
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
    elif strategy == 'mode':
        for col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else df_clean[col])
    
    return df_clean

def remove_outliers(df: pd.DataFrame, columns: List[str], method: str = 'iqr') -> pd.DataFrame:
    """
    Remueve outliers de las columnas especificadas
    
    Args:
        df: DataFrame de entrada
        columns: Lista de columnas para remover outliers
        method: Método para detectar outliers ('iqr', 'zscore')
        
    Returns:
        pd.DataFrame: DataFrame sin outliers
    """
    df_clean = df.copy()
    
    for col in columns:
        if method == 'iqr':
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
        elif method == 'zscore':
            z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
            df_clean = df_clean[z_scores < 3]
    
    return df_clean

def normalize_text_columns(df: pd.DataFrame, text_columns: List[str]) -> pd.DataFrame:
    """
    Normaliza columnas de texto (lowercase, strip, etc.)
    
    Args:
        df: DataFrame de entrada
        text_columns: Lista de columnas de texto a normalizar
        
    Returns:
        pd.DataFrame: DataFrame con texto normalizado
    """
    df_clean = df.copy()
    
    for col in text_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.lower().str.strip()
    
    return df_clean
