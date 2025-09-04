import re
from typing import Optional

def normalizar_laboratorio(valor: Optional[str]) -> str:
    if not valor or str(valor).strip() in ['', '-', '--', '?']:
        return 'no realizado'

    val = str(valor).strip().lower()

    if re.search(r'no detectable|no detectado|negativo|non detectable', val):
        return 'negativo'

    if re.search(r'detectable|positivo|positiva', val):
        return 'positivo'

    if 'en proceso' in val or 'en estudio' in val:
        return 'en proceso'

    if 'no realizado' in val or 'no relizado' in val or 'no procesado' in val or 'no procesada' in val:
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

    return val
