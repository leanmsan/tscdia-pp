# Dashboards y Visualizaciones

Este directorio contiene dashboards interactivos y reportes de visualización.

## Opciones de tecnología

### Streamlit
- Ideal para prototipos rápidos
- Sintaxis simple en Python
- Buena integración con pandas/matplotlib

### Dash (Plotly)
- Más control sobre el diseño
- Componentes interactivos avanzados
- Mejor para aplicaciones complejas

### Power BI / Tableau
- Para usuarios de negocio
- Archivos .pbix o .twb
- Conexiones a bases de datos

## Estructura sugerida
- `streamlit/` - Aplicaciones Streamlit
- `dash/` - Aplicaciones Dash
- `powerbi/` - Archivos de Power BI
- `static/` - Reportes estáticos (HTML, PDF)

## Ejemplo de ejecución
```bash
# Streamlit
streamlit run dashboard.py

# Dash
python dash_app.py
```
