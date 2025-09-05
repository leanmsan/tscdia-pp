# Streamlit Dashboard - Análisis de Datos Dengue

Este dashboard de Streamlit replica **EXACTAMENTE** todos los gráficos del script de análisis original, consultando datos directamente desde el backend FastAPI.

## 🚀 Configuración y Ejecución

### 1. Instalar Dependencias

```bash
cd frontend
pip install -r requirements.txt
```

### 2. Configurar Backend

Asegúrate de que el backend esté corriendo en `http://localhost:8000`. Si está en otra URL, modifica la variable `BACKEND_URL` en `streamlit_app.py`.

### 3. Ejecutar Dashboard

```bash
streamlit run streamlit_app.py
```

El dashboard estará disponible en `http://localhost:8501`

## 📊 Gráficos Incluidos

El dashboard incluye **TODOS** los gráficos del análisis original:

### 1. Análisis Exploratorio
- ✅ Distribución de la Edad (Histograma)
- ✅ Distribución de Días de Evolución (Histograma)  
- ✅ Dispersión Edad vs Días de Evolución (Scatter plot)

### 2. Análisis Geográfico
- ✅ Frecuencia de Establecimientos Notificadores (Barras)
- ✅ Top 10 Establecimientos Notificadores (Barras)
- ✅ Top 20 Localidades más Frecuentes (Barras)

### 3. Análisis de Laboratorio
- ✅ Distribución de Resultados RT-PCR Dengue (Pie chart)
- ✅ Distribución de Serotipos (Barras)
- ✅ Efectividad en la Detección (Barras múltiples)

### 4. Análisis Temporal
- ✅ Tendencia Mensual de Casos (Líneas)
- ✅ Demora en Procesamiento (Histograma + métricas)

### 5. Análisis Demográfico
- ✅ Distribución por Grupos Etarios (Barras + porcentajes)
- ✅ Días de Evolución por Grupo Etario (Box plots)

### 6. Análisis de Eficiencia
- ✅ Análisis Integral de Demoras por Establecimiento
- ✅ Evolución Temporal de Demoras
- ✅ Métricas de Eficiencia del Sistema

## 🎛️ Características Interactivas

### Filtros Disponibles
- **Rango de Fechas:** Filtra por período específico
- **Localidad:** Selecciona localidad específica o "Todas"
- **Departamento:** Selecciona departamento específico o "Todos"  
- **Grupo Etario:** Filtra por rango de edad específico

### Métricas en Tiempo Real
- Total de casos (con filtros aplicados)
- Tasa de positividad
- Cobertura de testeo
- Demoras promedio
- Distribución geográfica

### Visualizaciones Interactivas
- Zoom y pan en todos los gráficos
- Tooltips con información detallada
- Descarga de gráficos en PNG/SVG
- Tablas ordenables y filtrables

## 🔧 Configuración Backend

El dashboard consume los siguientes endpoints:

```
GET /laboratorio-dengue/procesados  # Datos procesados y normalizados
GET /laboratorio-dengue/raw        # Datos sin procesar (opcional)
GET /laboratorio-dengue/kpis       # KPIs básicos (opcional)
```

### Modificar URL del Backend

En `streamlit_app.py`, línea 25:
```python
BACKEND_URL = "http://localhost:8000"  # Cambiar aquí
```

## 📈 Replicación del Análisis Original

### Correspondencia de Gráficos

| Gráfico Original | Función Streamlit | Estado |
|-----------------|------------------|--------|
| `plt.hist(df['edad'])` | `plot_age_distribution()` | ✅ |
| `plt.hist(df['dias_evolucion'])` | `plot_evolution_days_distribution()` | ✅ |
| `plt.scatter(edad, dias_evolucion)` | `plot_age_vs_evolution_scatter()` | ✅ |
| `value_counts().plot(kind='bar')` establecimientos | `plot_establishments_frequency()` | ✅ |
| Top 10 establecimientos | `plot_top_10_establishments()` | ✅ |
| Top 20 localidades | `plot_top_20_localities()` | ✅ |
| `plt.pie()` distribución PCR | `plot_pcr_distribution()` | ✅ |
| Distribución serotipos | `plot_serotype_distribution()` | ✅ |
| Casos mensuales | `plot_monthly_trend()` | ✅ |
| Efectividad detección | `plot_testing_effectiveness()` | ✅ |
| Grupos etarios | `plot_age_group_distribution()` | ✅ |
| Box plots por edad | `plot_age_group_distribution()` | ✅ |
| Análisis demoras | `plot_processing_delay_analysis()` | ✅ |

### Datos Utilizados
- **Fuente:** Backend FastAPI con datos procesados por Polars
- **Normalización:** Igual que el script original (localidades, departamentos, establecimientos)
- **Filtros:** Aplicados en tiempo real sin afectar datos base
- **Cálculos:** Métricas idénticas (demoras, tasas, porcentajes)

## 🎯 KPIs Implementados

### Indicadores Clave
- **Total de casos:** Cantidad total de registros
- **Tasa de positividad:** (Positivos / Total testeados) × 100
- **Cobertura de testeo:** (Total testeados / Total casos) × 100  
- **Demora promedio:** Promedio de días entre recepción y procesamiento
- **Eficiencia:** % procesadas el mismo día

### Análisis Geográfico
- Top localidades por casos
- Top establecimientos por volumen
- Distribución departamental

### Análisis Temporal
- Tendencias mensuales
- Picos estacionales
- Evolución de demoras

### Análisis Clínico
- Distribución de serotipos
- Grupos etarios afectados
- Días de evolución promedio

## 💡 Uso Recomendado

### 1. Análisis Rutinario
- Ejecutar diariamente para monitoreo
- Revisar KPIs principales en resumen ejecutivo
- Identificar tendencias en gráfico temporal

### 2. Análisis Específico
- Usar filtros para investigar brotes locales
- Analizar eficiencia por establecimiento
- Evaluar cobertura diagnóstica

### 3. Reportes Ejecutivos
- Usar métricas del resumen ejecutivo
- Exportar gráficos para presentaciones
- Generar alertas según umbrales

## 🚨 Solución de Problemas

### Error de Conexión Backend
```
Error: No se pudieron cargar los datos desde el backend
```
**Solución:** Verificar que el backend esté corriendo en la URL configurada.

### Dashboard Lento
**Solución:** Usar filtros para reducir cantidad de datos. El cache está configurado por 5 minutos.

### Gráficos No Aparecen
**Solución:** Verificar que los datos tengan las columnas requeridas después de filtrar.

### Datos Desactualizados
**Solución:** El cache se actualiza automáticamente cada 5 minutos. Para forzar actualización, cambiar filtros.

## 📝 Mantenimiento

### Actualizar Dependencias
```bash
pip install -r requirements.txt --upgrade
```

### Logs de Depuración
Los logs se muestran en la terminal donde se ejecuta `streamlit run`.

### Modificar Visualizaciones
- Cada gráfico está en una función independiente
- Modificar colores en las constantes de cada función
- Agregar nuevos filtros en `create_sidebar_filters()`

---

**Desarrollado para:** Ministerio de Salud - Santiago del Estero  
**Tecnologías:** Streamlit, Plotly, Pandas, FastAPI  
**Autor:** Análisis replicado del script original
