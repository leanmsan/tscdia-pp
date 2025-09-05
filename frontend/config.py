# Configuración del Dashboard Streamlit
# Modificar estos valores según la configuración del entorno

# =================================
# CONFIGURACIÓN DEL BACKEND
# =================================

# URL base del backend FastAPI
BACKEND_URL = "http://localhost:8000"

# Timeout para requests al backend (segundos)
REQUEST_TIMEOUT = 30

# Intervalo de cache para datos (segundos)
CACHE_TTL = 300  # 5 minutos

# =================================
# CONFIGURACIÓN DE VISUALIZACIÓN
# =================================

# Colores para gráficos
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#4CAF50',
    'warning': '#FFD600',
    'danger': '#FF5252',
    'info': '#9C27B0',
    'light': '#BDBDBD',
    'dark': '#666666'
}

# Colores específicos para RT-PCR
PCR_COLORS = {
    'positivo': '#FF5252',
    'negativo': '#4CAF50', 
    'no realizado': '#BDBDBD',
    'en proceso': '#FFD600',
    'DEN-1': '#9C27B0',
    'DEN-2': '#FF5722',
    'DEN-3': '#FF9800',
    'DEN-4': '#00BCD4'
}

# Altura por defecto de gráficos
DEFAULT_CHART_HEIGHT = 500

# Número máximo de elementos en gráficos de barras
MAX_BARS_DISPLAY = 20

# =================================
# CONFIGURACIÓN DE FILTROS
# =================================

# Grupos etarios (bins y etiquetas)
AGE_BINS = [0, 10, 20, 30, 40, 50, 60, 70, 100]
AGE_LABELS = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']

# Valor por defecto para datos numéricos faltantes
DEFAULT_NUMERIC_VALUE = 0

# Valor máximo permitido para edad (para limpieza de datos)
MAX_AGE = 120

# Valor máximo permitido para días de evolución
MAX_EVOLUTION_DAYS = 365

# Valor máximo permitido para demora en procesamiento
MAX_DELAY_DAYS = 365

# =================================
# CONFIGURACIÓN DE STREAMLIT
# =================================

# Configuración de página
PAGE_CONFIG = {
    "page_title": "Análisis de Datos - Dengue Santiago del Estero",
    "page_icon": "🦠",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Mensajes de la aplicación
MESSAGES = {
    'loading': '🔄 Cargando datos desde el backend...',
    'success': '✅ Datos cargados exitosamente',
    'no_data_filters': ' No hay datos disponibles con los filtros seleccionados.',
    'filter_suggestion': ' **Sugerencia:** Intente ampliar los filtros o seleccionar \'Todas/Todos\' en las opciones.',
    'backend_error': '🔌 Error de conexión con el backend',
    'no_data_column': ' No hay datos disponibles para mostrar en esta columna.'
}

# =================================
# CONFIGURACIÓN DE LOGGING
# =================================

# Nivel de logging
LOG_LEVEL = "INFO"

# Formato de logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# =================================
# CONFIGURACIÓN DE ENDPOINTS
# =================================

# Endpoints del backend
ENDPOINTS = {
    'processed': 'procesados',
    'raw': 'raw', 
    'kpis': 'kpis'
}

# =================================
# CONFIGURACIÓN DE ARCHIVOS
# =================================

# Extensión por defecto para descargas
DOWNLOAD_FORMAT = 'csv'

# Nombre base para archivos descargados
DOWNLOAD_FILENAME_BASE = 'dengue_data'

# =================================
# CONFIGURACIÓN DE PERFORMANCE
# =================================

# Número mínimo de registros para mostrar warning de rendimiento
PERFORMANCE_WARNING_THRESHOLD = 50000

# Número de registros para muestreo en gráficos pesados
SAMPLING_THRESHOLD = 10000

# Tamaño de muestra para gráficos pesados
SAMPLE_SIZE = 5000
