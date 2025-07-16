# API para Deploy de Modelos

Este directorio contiene el código para desplegar modelos via API REST.

## Estructura sugerida
- `main.py` - Aplicación principal FastAPI/Flask
- `models/` - Modelos serializados
- `schemas/` - Schemas de entrada y salida
- `utils/` - Utilidades para la API
- `Dockerfile` - Para containerización
- `requirements_api.txt` - Dependencias específicas de la API

## Tecnologías recomendadas
- **FastAPI**: Para APIs modernas y rápidas
- **Flask**: Para APIs simples y ligeras
- **Docker**: Para containerización
- **Uvicorn**: Servidor ASGI para FastAPI

## Ejemplo de uso
```bash
# Instalar dependencias
pip install fastapi uvicorn

# Ejecutar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
