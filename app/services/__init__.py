"""
Servicios de DocentIA
Lógica de negocio de la aplicación
"""
from .ia_service import IAService, ia_service
from .document_service import DocumentService, document_service
from .export_service import ExportService, export_service

__all__ = [
    "IAService",
    "ia_service",
    "DocumentService",
    "document_service",
    "ExportService",
    "export_service"
]