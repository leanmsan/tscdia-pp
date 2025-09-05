import re
from typing import Optional

def normalizar_laboratorio(valor: Optional[str]) -> str:
    if not valor or str(valor).strip() in ['', '-', '--', '?']:
        return 'no realizado'

    # Limpiar espacios múltiples, normalizar y eliminar caracteres especiales
    val = str(valor).strip()
    val = re.sub(r'\s+', ' ', val)  # Espacios múltiples -> un espacio
    val = val.lower()
    val = re.sub(r'[^\w\s\-]', '', val)  # Eliminar caracteres especiales excepto guiones

    if re.search(r'no detectable|no detectado|negativo|non detectable', val):
        return 'negativo'

    if re.search(r'detectable|positivo|positiva', val):
        return 'positivo'

    if 'en proceso' in val or 'en estudio' in val:
        return 'en proceso'

    # Capturar variaciones de "no realizado" incluyendo typos comunes y espacios extra
    if re.search(r'no\s+(realizado|relizado|realiado|realzado|realisado)', val) or \
       re.search(r'no\s+(procesado|procesada|efectuado|efectuada)', val) or \
       re.search(r'sin\s+(realizar|procesar)', val) or \
       val in ['no realizado', 'no  realizado', 'no   realizado', 'no realiado', 'no relizado']:
        return 'no realizado'

    if 'indeterminado' in val:
        return 'indeterminado'

    match = re.search(r'den[\s\-_.]*([1-4])', val)
    if match:
        return f'DEN-{match.group(1)}'

    if 'den' in val and 'y' in val:
        return 'DEN-1 y DEN-2'

    if val in ['den_', 'den-', 'den']:
        return 'DEN-1'
    if val in ['de-2', '25']:
        return 'DEN-2'

    # Fallback: si contiene variaciones de "no realizado" que se escaparon
    if 'no' in val and ('real' in val or 'reliz' in val or 'proces' in val):
        return 'no realizado'

    return val
