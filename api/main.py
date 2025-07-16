"""
API de ejemplo usando FastAPI para servir modelos de ML
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear instancia de FastAPI
app = FastAPI(
    title="TSCDIA ML API",
    description="API para servir modelos de Machine Learning del proyecto TSCDIA",
    version="1.0.0"
)

# Modelos cargados (se cargan al iniciar la aplicación)
models = {}

class PredictionRequest(BaseModel):
    """Schema para requests de predicción"""
    features: Dict[str, Any]

class PredictionResponse(BaseModel):
    """Schema para respuestas de predicción"""
    prediction: Any
    probability: List[float] = None
    model_version: str

@app.on_event("startup")
async def load_models():
    """Cargar modelos al iniciar la aplicación"""
    try:
        # Ejemplo: cargar modelo guardado
        # models['classifier'] = joblib.load('../models/random_forest_final.joblib')
        logger.info("Modelos cargados exitosamente")
    except Exception as e:
        logger.error(f"Error cargando modelos: {e}")

@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "TSCDIA ML API",
        "status": "running",
        "available_endpoints": [
            "/docs",
            "/health",
            "/predict",
            "/model/info"
        ]
    }

@app.get("/health")
async def health_check():
    """Endpoint para verificar salud de la API"""
    return {
        "status": "healthy",
        "models_loaded": len(models),
        "version": "1.0.0"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Realizar predicción usando el modelo cargado
    """
    try:
        if 'classifier' not in models:
            raise HTTPException(status_code=503, detail="Modelo no disponible")
        
        # Convertir features a DataFrame
        df = pd.DataFrame([request.features])
        
        # Realizar predicción
        model = models['classifier']
        prediction = model.predict(df)[0]
        
        # Obtener probabilidades si están disponibles
        probabilities = None
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(df)[0].tolist()
        
        return PredictionResponse(
            prediction=prediction,
            probability=probabilities,
            model_version="1.0.0"
        )
        
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
async def model_info():
    """Información sobre el modelo cargado"""
    if 'classifier' not in models:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    model = models['classifier']
    
    return {
        "model_type": type(model).__name__,
        "model_params": model.get_params() if hasattr(model, 'get_params') else {},
        "features": getattr(model, 'feature_names_in_', []),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
