"""
Tests para el módulo ETL
"""

import pytest
import pandas as pd
import numpy as np
from src.etl.data_cleaner import clean_missing_values, remove_outliers, normalize_text_columns

def test_clean_missing_values_drop():
    """Test para limpieza con estrategia drop"""
    df = pd.DataFrame({
        'A': [1, 2, np.nan, 4],
        'B': [1, np.nan, 3, 4]
    })
    
    result = clean_missing_values(df, strategy='drop')
    
    assert len(result) == 2  # Solo 2 filas sin NaN
    assert not result.isnull().any().any()

def test_clean_missing_values_mean():
    """Test para limpieza con estrategia mean"""
    df = pd.DataFrame({
        'A': [1.0, 2.0, np.nan, 4.0],
        'B': [1.0, np.nan, 3.0, 4.0]
    })
    
    result = clean_missing_values(df, strategy='mean')
    
    assert not result.isnull().any().any()
    assert result['A'].iloc[2] == 2.5  # (1+2+4)/3

def test_remove_outliers_iqr():
    """Test para remoción de outliers con IQR"""
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5, 100],  # 100 es outlier
        'B': [1, 2, 3, 4, 5, 6]
    })
    
    result = remove_outliers(df, columns=['A'], method='iqr')
    
    assert len(result) < len(df)  # Se removieron outliers
    assert 100 not in result['A'].values

def test_normalize_text_columns():
    """Test para normalización de texto"""
    df = pd.DataFrame({
        'text_col': ['  HELLO  ', 'World', '  TEST  '],
        'other_col': [1, 2, 3]
    })
    
    result = normalize_text_columns(df, text_columns=['text_col'])
    
    assert result['text_col'].iloc[0] == 'hello'
    assert result['text_col'].iloc[1] == 'world'
    assert result['text_col'].iloc[2] == 'test'
