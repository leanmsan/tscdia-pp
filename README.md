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
│   │   │   ├── spark_jobs.py  # Funciones que ejecutan tareas PySpark
│   │   └── __init__.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── data/           # Lógica de PySpark
│   ├── jobs/
│   │   ├── process_dataset.py # Procesos ETL
│   │   ├── clustering.py      # Modelos ML o clustering
│   │   └── utils.py
│   ├── config/
│   │   ├── spark_session.py   # Inicialización de SparkSession
│   └── __init__.py
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