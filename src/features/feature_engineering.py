"""
Funciones para creación y transformación de características (features)
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from typing import List, Tuple

def create_polynomial_features(df: pd.DataFrame, columns: List[str], degree: int = 2) -> pd.DataFrame:
    """
    Crea características polinomiales para las columnas especificadas
    
    Args:
        df: DataFrame de entrada
        columns: Lista de columnas numéricas
        degree: Grado del polinomio
        
    Returns:
        pd.DataFrame: DataFrame con nuevas características
    """
    df_features = df.copy()
    
    for col in columns:
        if col in df_features.columns:
            for d in range(2, degree + 1):
                df_features[f"{col}_poly_{d}"] = df_features[col] ** d
    
    return df_features

def create_interaction_features(df: pd.DataFrame, column_pairs: List[Tuple[str, str]]) -> pd.DataFrame:
    """
    Crea características de interacción entre pares de columnas
    
    Args:
        df: DataFrame de entrada
        column_pairs: Lista de tuplas con pares de columnas
        
    Returns:
        pd.DataFrame: DataFrame con características de interacción
    """
    df_features = df.copy()
    
    for col1, col2 in column_pairs:
        if col1 in df_features.columns and col2 in df_features.columns:
            df_features[f"{col1}_{col2}_interaction"] = df_features[col1] * df_features[col2]
    
    return df_features

def encode_categorical_variables(df: pd.DataFrame, categorical_columns: List[str], 
                                method: str = 'onehot') -> Tuple[pd.DataFrame, dict]:
    """
    Codifica variables categóricas
    
    Args:
        df: DataFrame de entrada
        categorical_columns: Lista de columnas categóricas
        method: Método de codificación ('onehot', 'label')
        
    Returns:
        Tuple[pd.DataFrame, dict]: DataFrame codificado y diccionario de encoders
    """
    df_encoded = df.copy()
    encoders = {}
    
    for col in categorical_columns:
        if col in df_encoded.columns:
            if method == 'onehot':
                encoder = OneHotEncoder(drop='first', sparse_output=False)
                encoded_cols = encoder.fit_transform(df_encoded[[col]])
                feature_names = [f"{col}_{cat}" for cat in encoder.categories_[0][1:]]
                encoded_df = pd.DataFrame(encoded_cols, columns=feature_names, index=df_encoded.index)
                df_encoded = pd.concat([df_encoded.drop(col, axis=1), encoded_df], axis=1)
            elif method == 'label':
                encoder = LabelEncoder()
                df_encoded[col] = encoder.fit_transform(df_encoded[col])
            
            encoders[col] = encoder
    
    return df_encoded, encoders

def scale_numerical_features(df: pd.DataFrame, numerical_columns: List[str]) -> Tuple[pd.DataFrame, StandardScaler]:
    """
    Escala características numéricas usando StandardScaler
    
    Args:
        df: DataFrame de entrada
        numerical_columns: Lista de columnas numéricas
        
    Returns:
        Tuple[pd.DataFrame, StandardScaler]: DataFrame escalado y scaler
    """
    df_scaled = df.copy()
    scaler = StandardScaler()
    
    df_scaled[numerical_columns] = scaler.fit_transform(df_scaled[numerical_columns])
    
    return df_scaled, scaler
