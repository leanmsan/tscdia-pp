# TSCDIA - Práctica Profesionalizante

Repositorio correspondiente a la Práctica Profesionalizante de la Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial del Instituto Tecnológico de Santiago del Estero.

## 📁 Estructura del Proyecto

```
tscdia-pp/
│
├── data/                   # Gestión de datos
│   ├── raw/               # Descripción de datos crudos
│   └── processed/         # Scripts y datos transformados
│
├── notebooks/             # Análisis exploratorio y prototipado
│   ├── 01_eda.ipynb      # Análisis exploratorio de datos
│   ├── 02_modelos.ipynb  # Desarrollo de modelos
│   ├── 03_pyspark.ipynb  # Procesamiento con PySpark
│   └── 04_mysql_spark.ipynb # PySpark + MySQL especializado
│
├── src/                   # Código fuente modularizado
│   ├── etl/              # Funciones de carga y limpieza
│   ├── features/         # Feature engineering
│   ├── models/           # Entrenamiento y evaluación
│   └── utils/            # Funciones auxiliares
│
├── tests/                 # Unit tests
├── dashboards/           # Reportes interactivos
├── api/                  # Despliegue de modelos via API
│
├── config.yaml           # Configuración del proyecto
├── requirements.txt      # Dependencias
├── LICENSE              # Licencia del proyecto
└── README.md            # Este archivo
```

## 🚀 Inicio Rápido

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/leanmsan/tscdia-pp.git
cd tscdia-pp

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Uso
```bash
# Ejecutar notebooks
jupyter notebook notebooks/

# Configurar PySpark + MySQL (primera vez)
python setup_mysql_spark.py

# Ejecutar tests
pytest tests/

# Ejecutar API (ejemplo)
uvicorn api.main:app --reload
```

## 📊 Flujo de Trabajo

1. **Exploración**: Usar `notebooks/01_eda.ipynb` para análisis inicial
2. **Limpieza**: Implementar funciones en `src/etl/`
3. **Features**: Crear características en `src/features/`
4. **Modelado**: Entrenar modelos en `notebooks/02_modelos.ipynb`
5. **Testing**: Escribir tests en `tests/`
6. **Deploy**: Configurar API en `api/` o dashboard en `dashboards/`

## 🛠️ Tecnologías Utilizadas

- **Análisis**: pandas, numpy, scipy
- **Visualización**: matplotlib, seaborn, plotly
- **Machine Learning**: scikit-learn, xgboost, lightgbm
- **Big Data**: PySpark, findspark
- **Bases de Datos**: PostgreSQL, MySQL, SQLAlchemy
- **Notebooks**: Jupyter
- **Testing**: pytest
- **API**: FastAPI, uvicorn
- **Dashboards**: Streamlit, Dash

## 📝 Convenciones

### Código
- Usar docstrings en todas las funciones
- Seguir PEP 8 para estilo de código
- Incluir type hints cuando sea posible
- Escribir tests para funciones críticas

### Datos
- No subir datasets grandes al repositorio
- Documentar todas las fuentes de datos
- Usar nomenclatura descriptiva para archivos
- Mantener metadatos actualizados

### Git
- Usar commits descriptivos
- Crear branches para features nuevas
- Hacer code review antes de merge

## 🔧 Configuración

El archivo `config.yaml` contiene la configuración principal del proyecto:
- Rutas de datos
- Parámetros de modelos
- Configuración de logging
- Parámetros de visualización

## 📈 Métricas y Monitoreo

- Métricas de modelos guardadas en formato JSON
- Logs del proyecto en `project.log`
- Resultados de tests con coverage

## 🤝 Contribución

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Instituto Tecnológico de Santiago del Estero**
- **Tecnicatura Superior en Ciencia de Datos e IA**

## 📞 Contacto

Para preguntas o sugerencias, contactar a través de los canales oficiales del Instituto Tecnológico de Santiago del Estero.
