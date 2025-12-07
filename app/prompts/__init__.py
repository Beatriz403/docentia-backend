"""
Prompts de IA para DocentIA
Prompts optimizados para cada tipo de generación
"""
from .unidades import PROMPT_UNIDAD_DIDACTICA
from .rubricas import PROMPT_RUBRICA
from .examenes import PROMPT_EXAMEN
from .situaciones import PROMPT_SITUACION_APRENDIZAJE
from .informes import PROMPT_INFORME_FAMILIA
from .ideas import PROMPT_GENERADOR_IDEAS

__all__ = [
    "PROMPT_UNIDAD_DIDACTICA",
    "PROMPT_RUBRICA",
    "PROMPT_EXAMEN",
    "PROMPT_SITUACION_APRENDIZAJE",
    "PROMPT_INFORME_FAMILIA",
    "PROMPT_GENERADOR_IDEAS"
]