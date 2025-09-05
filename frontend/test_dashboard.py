# Script de prueba para verificar el funcionamiento del dashboard
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Verificar que todas las dependencias se puedan importar"""
    print(" Verificando imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit OK")
    except ImportError as e:
        print(f"❌ Streamlit ERROR: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas OK")
    except ImportError as e:
        print(f"❌ Pandas ERROR: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ Plotly OK")
    except ImportError as e:
        print(f"❌ Plotly ERROR: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests OK")
    except ImportError as e:
        print(f"❌ Requests ERROR: {e}")
        return False
    
    return True

def test_backend_connection():
    """Verificar conexión con el backend"""
    print("\n🔗 Verificando conexión con backend...")
    
    try:
        import requests
        from config import BACKEND_URL, REQUEST_TIMEOUT
        
        response = requests.get(f"{BACKEND_URL}/laboratorio-dengue/kpis", timeout=5)
        if response.status_code == 200:
            print("✅ Backend disponible")
            data = response.json()
            print(f"    Total casos: {data.get('total_casos', 'N/A')}")
            return True
        else:
            print(f"❌ Backend respondió con código: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend no disponible - Asegúrese de que esté corriendo en http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error conectando con backend: {e}")
        return False

def test_config_files():
    """Verificar que los archivos de configuración existan"""
    print("\n📄 Verificando archivos de configuración...")
    
    files_to_check = [
        'config.py',
        'utils.py', 
        'streamlit_app.py',
        'requirements.txt'
    ]
    
    all_ok = True
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file} existe")
        else:
            print(f"❌ {file} no encontrado")
            all_ok = False
    
    return all_ok

def test_sample_data_processing():
    """Probar el procesamiento de datos con datos de muestra"""
    print("\n Probando procesamiento de datos...")
    
    try:
        import pandas as pd
        from config import AGE_BINS, AGE_LABELS
        
        # Crear datos de muestra
        sample_data = {
            'edad': [25, 45, None, 67, 12, 89, 34],
            'dias_evolucion': [3, 5, None, 7, 2, 4, 6],
            'rt_pcr_tiempo_real_dengue_normalizado': ['positivo', 'negativo', 'no realizado', 'positivo', 'negativo', 'positivo', 'negativo'],
            'localidad_normalizada': ['SANTIAGO DEL ESTERO', 'LA BANDA', 'TERMAS DE RIO HONDO', 'FERNANDEZ', 'AÑATUYA', 'SANTIAGO DEL ESTERO', 'LA BANDA']
        }
        
        df = pd.DataFrame(sample_data)
        print("✅ DataFrame de muestra creado")
        
        # Probar creación de grupos etarios
        df['grupo_etario'] = pd.cut(df['edad'], bins=AGE_BINS, labels=AGE_LABELS, right=False)
        print("✅ Grupos etarios creados")
        
        # Probar conteos
        pcr_counts = df['rt_pcr_tiempo_real_dengue_normalizado'].value_counts()
        print(f"✅ Conteos RT-PCR: {len(pcr_counts)} categorías")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en procesamiento de datos: {e}")
        return False

def test_plotting_functions():
    """Probar que las funciones de gráficos no fallen"""
    print("\n Verificando funciones de visualización...")
    
    try:
        import pandas as pd
        import plotly.express as px
        from config import PCR_COLORS, DEFAULT_CHART_HEIGHT
        
        # Datos de muestra
        sample_data = pd.DataFrame({
            'edad': [25, 45, 67, 12, 89, 34],
            'rt_pcr_tiempo_real_dengue_normalizado': ['positivo', 'negativo', 'positivo', 'negativo', 'positivo', 'negativo']
        })
        
        # Probar histograma
        fig = px.histogram(sample_data, x='edad', title='Test Histogram')
        print("✅ Histograma OK")
        
        # Probar pie chart
        pcr_counts = sample_data['rt_pcr_tiempo_real_dengue_normalizado'].value_counts()
        fig = px.pie(values=pcr_counts.values, names=pcr_counts.index, title='Test Pie Chart')
        print("✅ Pie chart OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en funciones de visualización: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando pruebas del dashboard de Dengue\n")
    print("="*50)
    
    tests = [
        ("Imports", test_imports),
        ("Archivos de configuración", test_config_files),
        ("Procesamiento de datos", test_sample_data_processing),
        ("Funciones de visualización", test_plotting_functions),
        ("Conexión backend", test_backend_connection)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            results[test_name] = False
    
    print("\n" + "="*50)
    print("📋 RESUMEN DE PRUEBAS:")
    print("="*50)
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 TODAS LAS PRUEBAS PASARON")
        print("\nPuede ejecutar el dashboard con:")
        print("   streamlit run streamlit_app.py")
    else:
        print("  ALGUNAS PRUEBAS FALLARON")
        print("\nSoluciones recomendadas:")
        if not results.get("Imports", True):
            print("   - Ejecute: pip install -r requirements.txt")
        if not results.get("Conexión backend", True):
            print("   - Inicie el backend: cd ../backend && python main.py")
        if not results.get("Archivos de configuración", True):
            print("   - Verifique que todos los archivos estén presentes")
    
    print("="*50)

if __name__ == "__main__":
    main()
