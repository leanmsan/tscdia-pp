import re
import unicodedata
from typing import Optional

def quitar_tildes(texto: str) -> str:
    if not isinstance(texto, str):
        return str(texto)
    
    texto = texto.replace('ñ', '__enie__').replace('Ñ', '__ENIE__')
    nfkd = unicodedata.normalize('NFKD', texto)
    sin_tildes = ''.join(c for c in nfkd if not unicodedata.combining(c))
    return sin_tildes.replace('__enie__', 'ñ').replace('__ENIE__', 'Ñ')

def limpiar_basico(texto: str) -> str:
    if not isinstance(texto, str) or not texto.strip():
        return ""
    
    s = str(texto).strip()
    
    # Arreglos típicos de mala codificación
    s = s.replace('?A', 'Á').replace('?E', 'É').replace('?I', 'Í').replace('?O', 'Ó').replace('?U', 'Ú')
    s = s.replace('A?', 'Á').replace('E?', 'É').replace('I?', 'Í').replace('O?', 'Ó').replace('U?', 'Ú')
    s = s.replace('NU?EZ', 'NUÑEZ').replace('A?ATUYA', 'AÑATUYA').replace('CA?ADA', 'CAÑADA')
    # Muy común: Ñ rota como "?" o "§"
    s = s.replace('N?', 'Ñ').replace('N§', 'Ñ')
    
    s = re.sub(r'\s+', ' ', s)
    s = s.upper()
    
    return s

def normalizar_texto_base(valor: Optional[str], mapeo: dict, quitar_tildes_flag: bool = True) -> str:
    if not valor or str(valor).strip() == '':
        return 'DESCONOCIDO'
    
    v = limpiar_basico(valor)
    
    if quitar_tildes_flag:
        v = quitar_tildes(v)
    
    v = re.sub(r'\s+', ' ', v).strip()
    
    if v in mapeo:
        return mapeo[v]
    
    return v
