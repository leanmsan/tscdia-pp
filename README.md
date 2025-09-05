# 🦠 Sistema de Análisis de Datos - Dengue Santiago del Estero

Proyecto integral con **FastAPI** (backend), **Streamlit** (dashboard interactivo), y **Polars** para análisis de datos epidemiológicos de dengue.

## 🚀 Inicio Rápido

### 1. Iniciar Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 2. Iniciar Dashboard Streamlit
```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### 3. Acceder a las Aplicaciones
- **Dashboard Streamlit:** http://localhost:8501
- **API Backend:** http://localhost:8000
- **Documentación API:** http://localhost:8000/docs

## 📊 Dashboard de Análisis

El dashboard de Streamlit replica **EXACTAMENTE** todos los gráficos del análisis original:

### ✅ Gráficos Implementados (13 visualizaciones)
1. **Distribución de la Edad** (Histograma)
2. **Distribución de Días de Evolución** (Histograma)  
3. **Dispersión Edad vs Días de Evolución** (Scatter plot)
4. **Frecuencia de Establecimientos** (Barras horizontales)
5. **Top 10 Establecimientos** (Barras horizontales)
6. **Top 20 Localidades** (Barras horizontales)
7. **Distribución RT-PCR** (Pie chart con colores personalizados)
8. **Distribución de Serotipos** (Barras con anotaciones)
9. **Tendencia Mensual** (Líneas con marcadores)
10. **Efectividad de Detección** (Barras múltiples)
11. **Grupos Etarios** (Barras con porcentajes)
12. **Días Evolución por Edad** (Box plots)
13. **Análisis Integral de Demoras** (Múltiples visualizaciones)

### 🎛️ Características Interactivas
- **Filtros en tiempo real:** Fecha, localidad, departamento, grupo etario
- **Métricas dinámicas:** KPIs actualizados según filtros
- **Visualizaciones Plotly:** Zoom, pan, tooltips, exportación
- **Cache inteligente:** Actualización automática cada 5 minutos
- **Responsive:** Adaptado para diferentes tamaños de pantalla

## 📁 Estructura del Proyecto

```
tscdia-pp/
│
├── backend/                           # 🔧 FastAPI Backend
│   ├── app/
│   │   ├── main.py                   # Punto de entrada FastAPI
│   │   ├── api/
│   │   │   ├── routes.py             # Endpoints REST
│   │   │   └── laboratorio_dengue.py # Endpoints específicos dengue
│   │   ├── core/
│   │   │   └── config.py             # Configuración
│   │   ├── services/
│   │   │   └── laboratorio_dengue_service.py
│   │   └── data/
│   │       ├── connection.py         # Conexión DB
│   │       ├── repositories/         # Acceso a datos
│   │       └── processors/           # Procesamiento con Polars
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                          # 📊 Streamlit Dashboard  
│   ├── streamlit_app.py              # ⭐ NUEVA APP PRINCIPAL
│   ├── dengue_analyzer.py            # Clases de análisis
│   ├── requirements.txt              # Dependencias Streamlit
│   ├── run_dashboard.bat             # Script Windows
│   ├── run_dashboard.sh              # Script Linux/Mac
│   └── README_STREAMLIT.md           # Documentación detallada
│
├── docker-compose.yml                # Orquestación completa
└── README.md                         # Este archivo
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI:** API REST moderna y rápida
- **Polars:** Procesamiento de datos ultra-rápido
- **AsyncPG:** Conexión asíncrona a PostgreSQL
- **Pydantic:** Validación de datos

### Frontend
- **Streamlit:** Dashboard interactivo
- **Plotly:** Visualizaciones avanzadas e interactivas
- **Pandas:** Manipulación de datos
- **Requests:** Comunicación con backend

### Base de Datos
- **PostgreSQL:** Base de datos principal
- **Normalización:** Localidades, departamentos, establecimientos
- **Índices optimizados** para consultas rápidas

## 📈 Análisis Implementado

### Replicación Exacta del Script Original
El dashboard implementa **TODOS** los análisis del script `análisis_de_datos.py`:

| Análisis Original | Implementación Dashboard | Estado |
|------------------|-------------------------|---------|
| Estadísticas básicas | Métricas en tiempo real | ✅ |
| Distribución edad | `plot_age_distribution()` | ✅ |
| Días de evolución | `plot_evolution_days_distribution()` | ✅ |
| Scatter edad/días | `plot_age_vs_evolution_scatter()` | ✅ |
| Establecimientos | `plot_establishments_frequency()` | ✅ |
| Top 10 establecimientos | `plot_top_10_establishments()` | ✅ |
| Top localidades | `plot_top_20_localities()` | ✅ |
| Distribución PCR | `plot_pcr_distribution()` | ✅ |
| Serotipos | `plot_serotype_distribution()` | ✅ |
| Tendencia temporal | `plot_monthly_trend()` | ✅ |
| Efectividad detección | `plot_testing_effectiveness()` | ✅ |
| Grupos etarios | `plot_age_group_distribution()` | ✅ |
| Análisis demoras | `plot_processing_delay_analysis()` | ✅ |

### KPIs Clave
- **Casos totales** y distribución geográfica
- **Tasa de positividad** ((Positivos/Testeados) × 100)
- **Cobertura de testeo** ((Testeados/Total) × 100)
- **Demora promedio** en procesamiento de muestras
- **Eficiencia** (% procesadas el mismo día)
- **Distribución de serotipos** (DEN-1, DEN-2, etc.)

## 🔌 API Endpoints

### Principales Endpoints
```
GET /laboratorio-dengue/procesados    # Datos procesados y normalizados
GET /laboratorio-dengue/raw          # Datos sin procesar  
GET /laboratorio-dengue/kpis         # KPIs básicos calculados
```

### Procesamiento de Datos
- **Normalización** de localidades, departamentos, establecimientos
- **Validación** de tipos de datos (edad, fechas, demoras)
- **Cálculo automático** de métricas derivadas
- **Grupos etarios** generados dinámicamente
- **Filtros** aplicados sin modificar datos base

## 🚀 Despliegue

### Desarrollo Local
```bash
# Backend
cd backend && python main.py

# Frontend  
cd frontend && streamlit run streamlit_app.py
```

### Docker Compose
```bash
docker-compose up -d
```

### Scripts de Conveniencia
```bash
# Windows
frontend/run_dashboard.bat

# Linux/Mac
chmod +x frontend/run_dashboard.sh
./frontend/run_dashboard.sh
```

## 📝 Uso del Dashboard

### 1. Análisis Exploratorio
- Visualizar distribuciones de edad y días de evolución
- Identificar patrones en scatter plots
- Revisar estadísticas básicas en tiempo real

### 2. Análisis Geográfico  
- Identificar localidades con mayor incidencia
- Evaluar carga por establecimiento notificador
- Mapear distribución departamental

### 3. Análisis Clínico
- Monitorear tasa de positividad RT-PCR
- Analizar distribución de serotipos circulantes
- Evaluar efectividad del sistema diagnóstico

### 4. Análisis Temporal
- Identificar tendencias y picos estacionales
- Monitorear evolución mensual de casos
- Detectar patrones temporales

### 5. Eficiencia Operativa
- Evaluar demoras en procesamiento
- Identificar establecimientos con problemas
- Optimizar flujos de trabajo

## 🎯 Próximas Funcionalidades

- [ ] **Mapas interactivos** con distribución geográfica
- [ ] **Alertas automáticas** por umbrales configurables  
- [ ] **Exportación** de reportes en PDF/Excel
- [ ] **Comparación temporal** entre períodos
- [ ] **Predicciones** usando machine learning
- [ ] **Dashboard móvil** responsivo
- [ ] **Integración** con sistemas externos de salud

## 💡 Contribución

1. Fork del proyecto
2. Crear branch para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📞 Soporte

- **Documentación completa:** `frontend/README_STREAMLIT.md`
- **Issues:** Reportar en GitHub Issues
- **Logs:** Revisar terminal de Streamlit/FastAPI

---

**Desarrollado para:** Ministerio de Salud - Santiago del Estero  
**Contacto:** Equipo de Desarrollo - Sistema de Vigilancia Epidemiológica