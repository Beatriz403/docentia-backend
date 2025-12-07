"""
Modelos Pydantic para DocentIA
"""
from .requests import (
    UnidadDidacticaRequest,
    RubricaRequest,
    ExamenRequest,
    SituacionAprendizajeRequest,
    InformeFamiliaRequest,
    IdeasRequest
)

from .responses import (
    GeneracionResponse,
    DocumentoGenerado
)

__all__ = [
    # Requests
    "UnidadDidacticaRequest",
    "RubricaRequest",
    "ExamenRequest",
    "SituacionAprendizajeRequest",
    "InformeFamiliaRequest",
    "IdeasRequest",
    # Responses
    "GeneracionResponse",
    "DocumentoGenerado"
]