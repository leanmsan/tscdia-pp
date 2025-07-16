"""
Funciones para entrenamiento y evaluación de modelos
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from typing import Dict, Any, Tuple

def split_data(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, 
               random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Divide los datos en conjuntos de entrenamiento y prueba
    
    Args:
        X: Características
        y: Variable objetivo
        test_size: Proporción del conjunto de prueba
        random_state: Semilla aleatoria
        
    Returns:
        Tuple: X_train, X_test, y_train, y_test
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_classification_model(X_train: pd.DataFrame, y_train: pd.Series, 
                             model_type: str = 'random_forest', **kwargs) -> Any:
    """
    Entrena un modelo de clasificación
    
    Args:
        X_train: Características de entrenamiento
        y_train: Etiquetas de entrenamiento
        model_type: Tipo de modelo a entrenar
        **kwargs: Parámetros adicionales del modelo
        
    Returns:
        Modelo entrenado
    """
    if model_type == 'random_forest':
        model = RandomForestClassifier(random_state=42, **kwargs)
    else:
        raise ValueError(f"Tipo de modelo no soportado: {model_type}")
    
    model.fit(X_train, y_train)
    return model

def train_regression_model(X_train: pd.DataFrame, y_train: pd.Series, 
                          model_type: str = 'random_forest', **kwargs) -> Any:
    """
    Entrena un modelo de regresión
    
    Args:
        X_train: Características de entrenamiento
        y_train: Valores objetivo de entrenamiento
        model_type: Tipo de modelo a entrenar
        **kwargs: Parámetros adicionales del modelo
        
    Returns:
        Modelo entrenado
    """
    if model_type == 'random_forest':
        model = RandomForestRegressor(random_state=42, **kwargs)
    else:
        raise ValueError(f"Tipo de modelo no soportado: {model_type}")
    
    model.fit(X_train, y_train)
    return model

def evaluate_classification_model(model: Any, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
    """
    Evalúa un modelo de clasificación
    
    Args:
        model: Modelo entrenado
        X_test: Características de prueba
        y_test: Etiquetas de prueba
        
    Returns:
        Dict: Métricas de evaluación
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }
    
    return metrics

def evaluate_regression_model(model: Any, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
    """
    Evalúa un modelo de regresión
    
    Args:
        model: Modelo entrenado
        X_test: Características de prueba
        y_test: Valores objetivo de prueba
        
    Returns:
        Dict: Métricas de evaluación
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        'mse': mean_squared_error(y_test, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'r2_score': r2_score(y_test, y_pred)
    }
    
    return metrics

def save_model(model: Any, file_path: str):
    """
    Guarda un modelo entrenado
    
    Args:
        model: Modelo a guardar
        file_path: Ruta del archivo
    """
    joblib.dump(model, file_path)
    print(f"Modelo guardado en: {file_path}")

def load_model(file_path: str) -> Any:
    """
    Carga un modelo guardado
    
    Args:
        file_path: Ruta del archivo del modelo
        
    Returns:
        Modelo cargado
    """
    return joblib.load(file_path)
