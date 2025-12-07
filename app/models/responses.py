"""
Modelos Pydantic para las respuestas (responses) de la API
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class DocumentoGenerado(BaseModel):
    """Documento generado por la IA"""
    contenido: str = Field(..., description="Contenido del documento en formato markdown")
    proveedor: str = Field(..., description="Proveedor de IA utilizado (claude, openai, gemini)")
    modelo: str = Field(..., description="Modelo específico utilizado")
    tiempo_generacion: float = Field(..., description="Tiempo de generación en segundos")
    tokens_usados: Optional[int] = Field(None, description="Tokens consumidos (si está disponible)")


class GeneracionResponse(BaseModel):
    """Respuesta estándar de generación de documentos"""
    success: bool = Field(..., description="Indica si la generación fue exitosa")
    data: Optional[DocumentoGenerado] = Field(None, description="Datos del documento generado")
    message: str = Field(..., description="Mensaje descriptivo")
    timestamp: datetime = Field(default_factory=datetime.now, description="Marca de tiempo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "contenido": "# Unidad Didáctica\n\n## Introducción\n...",
                    "proveedor": "claude",
                    "modelo": "claude-sonnet-4-20250514",
                    "tiempo_generacion": 15.3,
                    "tokens_usados": 2500
                },
                "message": "Documento generado correctamente",
                "timestamp": "2025-12-06T10:30:00"
            }
        }