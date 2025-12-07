"""
Servicio de Generación de Documentos
Coordina la generación de todos los tipos de documentos educativos
"""
from typing import Dict, Any
from app.services.ia_service import ia_service
from app.prompts import (
    PROMPT_UNIDAD_DIDACTICA,
    PROMPT_RUBRICA,
    PROMPT_EXAMEN,
    PROMPT_SITUACION_APRENDIZAJE,
    PROMPT_INFORME_FAMILIA,
    PROMPT_GENERADOR_IDEAS
)
from app.models.requests import (
    UnidadDidacticaRequest,
    RubricaRequest,
    ExamenRequest,
    SituacionAprendizajeRequest,
    InformeFamiliaRequest,
    IdeasRequest
)


class DocumentService:
    """Servicio para coordinar la generación de documentos educativos"""
    
    @staticmethod
    async def generar_unidad_didactica(request: UnidadDidacticaRequest) -> Dict[str, Any]:
        """Genera una Unidad Didáctica completa"""
        
        user_prompt = f"""
Genera una Unidad Didáctica con estos datos:

- **Nivel:** {request.nivel}
- **Curso:** {request.curso}
- **Asignatura:** {request.asignatura}
- **Tema:** {request.tema}
- **Características del grupo:** {request.caracteristicas_grupo or 'Grupo estándar'}

Importante: Usa la legislación de Extremadura (Decreto 107/2022 para Primaria o 110/2022 para ESO según corresponda).
"""
        
        return await ia_service.generate(
            system_prompt=PROMPT_UNIDAD_DIDACTICA,
            user_prompt=user_prompt,
            max_tokens=4096,
            temperature=0.7
        )
    
    @staticmethod
    async def generar_rubrica(request: RubricaRequest) -> Dict[str, Any]:
        """Genera una Rúbrica de Evaluación"""
        
        user_prompt = f"""
Genera una Rúbrica de Evaluación con estos datos:

- **Nivel:** {request.nivel}
- **Curso:** {request.curso}
- **Asignatura:** {request.asignatura}
- **Tema a evaluar:** {request.tema}
- **Tipo de evaluación:** {request.tipo_evaluacion}

Usa los criterios de evaluación del currículo de Extremadura.
"""
        
        return await ia_service.generate(
            system_prompt=PROMPT_RUBRICA,
            user_prompt=user_prompt,
            max_tokens=3000,
            temperature=0.6
        )
    
    @staticmethod
    async def generar_examen(request: ExamenRequest) -> Dict[str, Any]:
        """Genera un Examen completo"""
        
        user_prompt = f"""
Genera un Examen con estos datos:

- **Nivel:** {request.nivel}
- **Curso:** {request.curso}
- **Asignatura:** {request.asignatura}
- **Tema:** {request.tema}
- **Tipo de examen:** {request.tipo_examen}
- **Dificultad:** {request.dificultad}
- **Duración:** {request.duracion}

IMPORTANTE: 
- Adapta el lenguaje y la complejidad al nivel educativo ({request.curso})
- Incluye la hoja de respuestas separada
- Las preguntas deben poder responderse en {request.duracion}
"""
        
        return await ia_service.generate(
            system_prompt=PROMPT_EXAMEN,
            user_prompt=user_prompt,
            max_tokens=4096,
            temperature=0.6
        )
    
    @staticmethod
    async def generar_situacion_aprendizaje(request: SituacionAprendizajeRequest) -> Dict[str, Any]:
        """Genera una Situación de Aprendizaje LOMLOE"""
        
        competencias_str = ", ".join(request.competencias_clave)
        
        user_prompt = f"""
Genera una Situación de Aprendizaje con estos datos:

- **Nivel:** {request.nivel}
- **Curso:** {request.curso}
- **Asignatura:** {request.asignatura}
- **Contexto/Situación real:** {request.contexto}
- **Metodología:** {request.metodologia}
- **Duración:** {request.duracion_sesiones} sesiones
- **Competencias clave a trabajar:** {competencias_str}

IMPORTANTE: Usa la legislación de Extremadura y enfoque LOMLOE.
"""
        
        return await ia_service.generate(
            system_prompt=PROMPT_SITUACION_APRENDIZAJE,
            user_prompt=user_prompt,
            max_tokens=4096,
            temperature=0.7
        )
    
    @staticmethod
    async def generar_informe_familia(request: InformeFamiliaRequest) -> Dict[str, Any]:
        """Genera un Informe a Familias"""
        
        user_prompt = f"""
Genera un Informe a Familias con estos datos:

- **Nivel:** {request.nivel}
- **Curso:** {request.curso}
- **Asignatura:** {request.asignatura}
- **Nombre del alumno:** {request.nombre_alumno}
- **Aspectos positivos:** {request.aspectos_positivos}
- **Aspectos a mejorar:** {request.aspectos_mejora}
- **Tono deseado:** {request.tono}

IMPORTANTE: 
- Usa un lenguaje {request.tono}
- Sé específico pero constructivo
- Incluye recomendaciones para las familias
"""
        
        return await ia_service.generate(
            system_prompt=PROMPT_INFORME_FAMILIA,
            user_prompt=user_prompt,
            max_tokens=2000,
            temperature=0.7
        )
    
    @staticmethod
    async def generar_ideas(request: IdeasRequest) -> Dict[str, Any]:
        """Genera Ideas didácticas creativas"""
        
        user_prompt = f"""
Genera ideas didácticas creativas con estos datos:

- **Nivel:** {request.nivel}
- **Curso:** {request.curso}
- **Asignatura:** {request.asignatura}
- **Tema:** {request.tema}
- **Tipo de actividad deseada:** {request.tipo_actividad}

IMPORTANTE: 
- Proporciona 5 ideas diferentes
- Cada idea debe ser original y práctica
- Adaptadas al nivel y al contexto actual
"""
        
        return await ia_service.generate(
            system_prompt=PROMPT_GENERADOR_IDEAS,
            user_prompt=user_prompt,
            max_tokens=2500,
            temperature=0.8
        )


# Instancia global del servicio
document_service = DocumentService()