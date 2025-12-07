"""
Modelos Pydantic para las peticiones (requests) a la API
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class UnidadDidacticaRequest(BaseModel):
    """Modelo para solicitar generación de Unidad Didáctica"""
    nivel: str = Field(..., description="Nivel educativo (Primaria/ESO)")
    curso: str = Field(..., description="Curso específico (1º, 2º, etc.)")
    asignatura: str = Field(..., description="Asignatura")
    tema: str = Field(..., description="Tema o título de la unidad")
    caracteristicas_grupo: Optional[str] = Field(None, description="Características del grupo-clase")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nivel": "Primaria",
                "curso": "3º de Primaria",
                "asignatura": "Lengua Castellana y Literatura",
                "tema": "El sustantivo y sus clases",
                "caracteristicas_grupo": "Grupo de 25 alumnos, 2 ACNEAE"
            }
        }


class RubricaRequest(BaseModel):
    """Modelo para solicitar generación de Rúbrica"""
    nivel: str = Field(..., description="Nivel educativo")
    curso: str = Field(..., description="Curso")
    asignatura: str = Field(..., description="Asignatura")
    tema: str = Field(..., description="Tema a evaluar")
    tipo_evaluacion: str = Field(..., description="Tipo de evaluación (Actividad, Proyecto, Examen, etc.)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nivel": "ESO",
                "curso": "1º ESO",
                "asignatura": "Matemáticas",
                "tema": "Ecuaciones de primer grado",
                "tipo_evaluacion": "Actividad práctica"
            }
        }


class ExamenRequest(BaseModel):
    """Modelo para solicitar generación de Examen"""
    nivel: str = Field(..., description="Nivel educativo")
    curso: str = Field(..., description="Curso")
    asignatura: str = Field(..., description="Asignatura")
    tema: str = Field(..., description="Tema del examen")
    tipo_examen: str = Field(..., description="Tipo (Test, Desarrollo, Mixto)")
    dificultad: str = Field(..., description="Dificultad (Fácil, Media, Difícil)")
    duracion: str = Field(..., description="Duración del examen")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nivel": "Primaria",
                "curso": "5º de Primaria",
                "asignatura": "Ciencias Naturales",
                "tema": "El sistema solar",
                "tipo_examen": "Mixto",
                "dificultad": "Media",
                "duracion": "45 minutos"
            }
        }


class SituacionAprendizajeRequest(BaseModel):
    """Modelo para solicitar generación de Situación de Aprendizaje"""
    nivel: str = Field(..., description="Nivel educativo")
    curso: str = Field(..., description="Curso")
    asignatura: str = Field(..., description="Asignatura")
    contexto: str = Field(..., description="Contexto o situación real")
    metodologia: str = Field(..., description="Metodología a aplicar")
    duracion_sesiones: int = Field(..., description="Número de sesiones")
    competencias_clave: List[str] = Field(..., description="Competencias clave a trabajar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nivel": "ESO",
                "curso": "2º ESO",
                "asignatura": "Geografía e Historia",
                "contexto": "Organizar una visita virtual a un museo",
                "metodologia": "Aprendizaje basado en proyectos",
                "duracion_sesiones": 8,
                "competencias_clave": ["CCL", "CD", "CCEC"]
            }
        }


class InformeFamiliaRequest(BaseModel):
    """Modelo para solicitar generación de Informe a Familias"""
    nivel: str = Field(..., description="Nivel educativo")
    curso: str = Field(..., description="Curso")
    asignatura: str = Field(..., description="Asignatura")
    nombre_alumno: str = Field(..., description="Nombre del alumno")
    aspectos_positivos: str = Field(..., description="Aspectos positivos del alumno")
    aspectos_mejora: str = Field(..., description="Aspectos a mejorar")
    tono: str = Field(..., description="Tono del informe (Formal, Cercano, Motivador)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nivel": "Primaria",
                "curso": "4º de Primaria",
                "asignatura": "Matemáticas",
                "nombre_alumno": "Ana García",
                "aspectos_positivos": "Participa activamente, comprende conceptos rápidamente",
                "aspectos_mejora": "Necesita mejorar la atención en los problemas largos",
                "tono": "Cercano"
            }
        }


class IdeasRequest(BaseModel):
    """Modelo para solicitar generación de Ideas didácticas"""
    nivel: str = Field(..., description="Nivel educativo")
    curso: str = Field(..., description="Curso")
    asignatura: str = Field(..., description="Asignatura")
    tema: str = Field(..., description="Tema")
    tipo_actividad: str = Field(..., description="Tipo de actividad deseada")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nivel": "Primaria",
                "curso": "6º de Primaria",
                "asignatura": "Ciencias Sociales",
                "tema": "La Edad Media",
                "tipo_actividad": "Actividad práctica o juego"
            }
        }