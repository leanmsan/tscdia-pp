Proyecto con FastAPI, PySpark, y Streamlit


## Estructura

```
project-root/
│
├── backend/                  # FastAPI
│   ├── app/
│   │   ├── main.py            # Punto de entrada FastAPI
│   │   ├── api/
│   │   │   ├── routes.py      # Endpoints REST
│   │   ├── core/
│   │   │   ├── config.py      # Configuración (puertos, DB, Spark)
│   │   ├── services/
│   │   ├── data/
│   │   │   ├── connection.py  # Conexión a la Base de Datos          
│   │   └── __init__.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                  # Streamlit
│   ├── app.py                 # Entrada Streamlit
│   ├── pages/                 # Páginas adicionales
│   ├── components/            # Componentes reutilizables
│   ├── requirements.txt
│   └── Dockerfile
│
├── shared/                    # Código común
│   ├── schemas.py              # Pydantic models (compartidos FastAPI/Streamlit)
│   ├── constants.py
│   └── __init__.py
│
├── docker-compose.yml          # Levantar todo junto
├── README.md
└── requirements.txt            # Dependencias comunes
```