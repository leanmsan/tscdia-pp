#!/usr/bin/env python3
"""
Script de prueba para verificar la normalización de establecimientos notificadores.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.data.processors.establecimiento_processor import normalizar_establecimiento_notificador

def test_normalizacion():
    """Prueba la normalización con casos de ejemplo."""
    
    casos_prueba = [
        # Casos básicos
        'EL CRUCE- UPA N?1',
        'CTRAL.ARGENTINO-UPA N§2',
        'VILLA GRISELDA- UPA N?3',
        'MISKI MAYU-UPA N?4',
        
        # Hospitales
        'AATUYA HOSPITAL ZONAL',
        'A¤ATUYA HOSPITAL ZONAL',
        'NEUMONOLOGICO DR. GUMERCINDO SAYAGO-HOSPITAL',
        
        # CAPS
        'DR ARCHETTI - CAPS',
        'CAPS N?9 LOS FLORES',
        'JUAN DIAZ SOLIS- CAPS',
        
        # Casos desconocidos
        'DESCONOCIDO',
        'N/A',
        '',
        None,
        
        # Casos con problemas de codificación
        'PARQUE INDRUSTRIAL- UPA No 5- BANDA',
        'BELEN- UPA NØ25',
        'SANTISIMO SACRAMENTO B? BORGES- CAPS',
        
        # Casos en minúscula
        'desconocido',
        'na',
    ]
    
    print("🔬 Probando normalización de establecimientos notificadores...\n")
    
    for i, caso in enumerate(casos_prueba, 1):
        try:
            resultado = normalizar_establecimiento_notificador(caso)
            print(f"{i:2d}. '{caso}' → '{resultado}'")
        except Exception as e:
            print(f"{i:2d}. '{caso}' → ERROR: {e}")
    
    print("\n✅ Prueba completada!")

def test_casos_especificos():
    """Prueba casos específicos mencionados en el mapeo."""
    
    print("\n🎯 Probando casos específicos del mapeo...\n")
    
    casos_especificos = [
        ('EL CRUCE- UPA N?1', 'EL CRUCE - UPA N1'),
        ('CTRAL.ARGENTINO-UPA N§2', 'CENTRAL ARGENTINO - UPA N2'),
        ('MARIANO M-UPA N?1', 'MARIANO MORENO I - UPA'),
        ('AATUYA HOSPITAL ZONAL', 'AÑATUYA - HOSPITAL ZONAL'),
        ('DR ARCHETTI - CAPS', 'DR ARMANDO ARCHETTI - CAPS'),
        ('DESCONOCIDO', 'DESCONOCIDO'),
        ('', 'DESCONOCIDO'),
    ]
    
    for entrada, esperado in casos_especificos:
        resultado = normalizar_establecimiento_notificador(entrada)
        status = "✅" if resultado == esperado else "❌"
        print(f"{status} '{entrada}' → '{resultado}' (esperado: '{esperado}')")

if __name__ == "__main__":
    test_normalizacion()
    test_casos_especificos()
    
    print("\n🚀 Para probar con datos reales, ejecuta el backend y usa el endpoint /laboratorio-dengue/procesados")
