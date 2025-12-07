"""
DocentIA Backend - Endpoints para Generadores
FastAPI + Anthropic Claude API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
import os
from typing import Optional

# Inicializar FastAPI
app = FastAPI(title="DocentIA API", version="1.0.0")

# CORS - Permitir frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://docentia-frontend.vercel.app",
        "https://docentia-ex.vercel.app",
        "https://beatriz403-v0-education-technology.vercel.app",
        "http://localhost:3000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar Claude
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ============================================
# MODELOS DE DATOS
# ============================================

class BotonEmergenciaRequest(BaseModel):
    nivel: str
    curso: str
    asignatura: str
    situacion: str
    duracion: str

class ExamenRequest(BaseModel):
    nivel: str
    curso: str
    asignatura: str
    tema: str
    tipo_preguntas: str
    num_preguntas: int

class ProblemasMatematicasRequest(BaseModel):
    nivel: str
    curso: str
    tema: str
    num_problemas: int
    dificultad: str
    con_soluciones: bool = True

class RubricaRequest(BaseModel):
    nivel: str
    curso: str
    asignatura: str
    actividad: str
    criterios: Optional[list[str]] = None
    niveles_logro: int = 4  # Insuficiente, Suficiente, Notable, Sobresaliente

class UnidadDidacticaRequest(BaseModel):
    nivel: str
    curso: str
    asignatura: str
    titulo: str
    num_sesiones: int
    trimestre: str

class SituacionAprendizajeRequest(BaseModel):
    nivel: str
    curso: str
    asignatura: str
    tema: str
    duracion_sesiones: int
    competencias_clave: Optional[list[str]] = None

class ProgramacionDidacticaRequest(BaseModel):
    nivel: str
    curso: str
    asignatura: str
    centro: str
    curso_academico: str

class AdaptacionCurricularRequest(BaseModel):
    nivel: str
    curso: str
    asignatura: str
    tipo_adaptacion: str  # ACI, ACIS, Enriquecimiento
    necesidad: str
    medidas: Optional[list[str]] = None

# ============================================
# ENDPOINT: HEALTH CHECK
# ============================================

@app.get("/")
def health_check():
    return {
        "app": "DocentIA",
        "status": "online",
        "provider": "claude",
        "version": "1.0.0",
        "endpoints": [
            "/generar/boton-emergencia",
            "/generar/examen",
            "/generar/problemas-matematicas",
            "/generar/rubrica",
            "/generar/unidad-didactica",
            "/generar/situacion-aprendizaje",
            "/generar/programacion-didactica",
            "/generar/adaptacion-curricular"
        ]
    }

# ============================================
# ENDPOINT: BOTÓN DE EMERGENCIA
# ============================================

@app.post("/generar/boton-emergencia")
async def generar_boton_emergencia(datos: BotonEmergenciaRequest):
    """
    Genera una actividad de emergencia para situaciones imprevistas.
    30 segundos de generación.
    """
    
    try:
        # Construir prompt para Claude
        prompt = f"""Eres un asistente experto en educación española que ayuda a docentes de Extremadura.

TAREA: Generar una actividad de emergencia completa para la siguiente situación:

DATOS:
- Nivel: {datos.nivel}
- Curso: {datos.curso}
- Asignatura: {datos.asignatura}
- Situación urgente: {datos.situacion}
- Duración: {datos.duracion}

INSTRUCCIONES:
1. Crea una actividad COMPLETA lista para usar INMEDIATAMENTE
2. Debe ser apropiada para {datos.curso} de {datos.nivel}
3. Duración exacta: {datos.duracion}
4. Incluye:
   - Título de la actividad
   - Objetivos de aprendizaje (2-3)
   - Desarrollo paso a paso (con tiempos)
   - Materiales necesarios
   - Criterios de evaluación
5. Cumple con LOMLOE 2024
6. Formato claro y profesional
7. Debe resolver la situación: {datos.situacion}

GENERA LA ACTIVIDAD:"""

        # Llamar a Claude
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        contenido = message.content[0].text
        
        return {
            "success": True,
            "contenido": contenido,
            "nivel": datos.nivel,
            "curso": datos.curso,
            "asignatura": datos.asignatura,
            "tipo": "boton-emergencia"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar actividad: {str(e)}")

# ============================================
# ENDPOINT: EXÁMENES
# ============================================

@app.post("/generar/examen")
async def generar_examen(datos: ExamenRequest):
    """
    Genera un examen profesional con criterios de evaluación y rúbricas.
    """
    
    try:
        # Construir prompt para Claude
        prompt = f"""Eres un experto en evaluación educativa española que crea exámenes para docentes.

TAREA: Generar un examen completo para:

DATOS:
- Nivel: {datos.nivel}
- Curso: {datos.curso}
- Asignatura: {datos.asignatura}
- Tema: {datos.tema}
- Tipo de preguntas: {datos.tipo_preguntas}
- Número de preguntas: {datos.num_preguntas}

INSTRUCCIONES:
1. Crea un examen PROFESIONAL listo para imprimir
2. Apropiado para {datos.curso} de {datos.nivel}
3. Incluye:
   - Encabezado (nombre, fecha, curso)
   - {datos.num_preguntas} preguntas de tipo {datos.tipo_preguntas}
   - Criterios de evaluación por pregunta
   - Puntuación total (sobre 10)
   - Rúbrica de corrección
4. Cumple con criterios LOMLOE 2024
5. Formato claro y profesional
6. Dificultad progresiva (fácil → media → difícil)

Si tipo es "test": 4 opciones por pregunta (A, B, C, D)
Si tipo es "desarrollo": preguntas abiertas con criterios detallados
Si tipo es "mixto": combina ambos tipos

GENERA EL EXAMEN:"""

        # Llamar a Claude
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            temperature=0.6,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        contenido = message.content[0].text
        
        return {
            "success": True,
            "contenido": contenido,
            "nivel": datos.nivel,
            "curso": datos.curso,
            "asignatura": datos.asignatura,
            "tema": datos.tema,
            "tipo": "examen"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar examen: {str(e)}")

# ============================================
# ENDPOINT: PROBLEMAS MATEMÁTICAS
# ============================================

@app.post("/generar/problemas-matematicas")
async def generar_problemas_matematicas(datos: ProblemasMatematicasRequest):
    """
    Genera problemas de matemáticas adaptados a nivel con soluciones paso a paso.
    """
    
    try:
        # Construir prompt para Claude
        prompt = f"""Eres un profesor experto en matemáticas que crea problemas para docentes españoles.

TAREA: Generar problemas de matemáticas para:

DATOS:
- Nivel: {datos.nivel}
- Curso: {datos.curso}
- Tema: {datos.tema}
- Número de problemas: {datos.num_problemas}
- Dificultad: {datos.dificultad}
- Con soluciones: {'Sí' if datos.con_soluciones else 'No'}

INSTRUCCIONES:
1. Crea {datos.num_problemas} problemas de dificultad {datos.dificultad}
2. Apropiados para {datos.curso} de {datos.nivel}
3. Tema específico: {datos.tema}
4. Cada problema debe incluir:
   - Enunciado claro y contextualizado
   - Datos necesarios
   - Pregunta específica
   {"- Solución paso a paso con explicaciones" if datos.con_soluciones else ""}
   {"- Resultado final" if datos.con_soluciones else ""}
5. Contextos variados (vida real, cotidianos, interesantes para alumnos)
6. Cumple con currículo LOMLOE 2024
7. Formato claro y profesional

GENERA LOS PROBLEMAS:"""

        # Llamar a Claude
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        contenido = message.content[0].text
        
        return {
            "success": True,
            "contenido": contenido,
            "nivel": datos.nivel,
            "curso": datos.curso,
            "tema": datos.tema,
            "num_problemas": datos.num_problemas,
            "tipo": "problemas-matematicas"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar problemas: {str(e)}")

# ============================================
# ENDPOINT: RÚBRICAS DE EVALUACIÓN
# ============================================

@app.post("/generar/rubrica")
async def generar_rubrica(datos: RubricaRequest):
    """
    Genera una rúbrica de evaluación profesional con niveles de logro.
    """
    
    try:
        criterios_texto = ""
        if datos.criterios and len(datos.criterios) > 0:
            criterios_texto = f"\nCriterios específicos a evaluar:\n" + "\n".join([f"- {c}" for c in datos.criterios])
        
        prompt = f"""Eres un experto en evaluación educativa española que crea rúbricas profesionales.

TAREA: Generar una rúbrica de evaluación completa para:

DATOS:
- Nivel: {datos.nivel}
- Curso: {datos.curso}
- Asignatura: {datos.asignatura}
- Actividad/Tarea: {datos.actividad}
- Niveles de logro: {datos.niveles_logro}
{criterios_texto}

INSTRUCCIONES:
1. Crea una rúbrica PROFESIONAL lista para usar
2. Apropiada para {datos.curso} de {datos.nivel}
3. Incluye:
   - Título de la rúbrica
   - Criterios de evaluación (mínimo 5)
   - {datos.niveles_logro} niveles de logro para cada criterio
   - Descriptores claros y específicos por nivel
   - Puntuación asociada a cada nivel
   - Ponderación de criterios
4. Niveles típicos: Insuficiente, Suficiente, Notable, Sobresaliente
5. Cumple con LOMLOE 2024
6. Formato tabla clara y profesional
7. Incluye instrucciones de uso

GENERA LA RÚBRICA:"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,
            temperature=0.5,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        contenido = message.content[0].text
        
        return {
            "success": True,
            "contenido": contenido,
            "nivel": datos.nivel,
            "curso": datos.curso,
            "asignatura": datos.asignatura,
            "tipo": "rubrica"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar rúbrica: {str(e)}")

# ============================================
# ENDPOINT: UNIDADES DIDÁCTICAS
# ============================================

@app.post("/generar/unidad-didactica")
async def generar_unidad_didactica(datos: UnidadDidacticaRequest):
    """
    Genera una unidad didáctica completa con todas las sesiones.
    """
    
    try:
        prompt = f"""Eres un experto en programación didáctica española que crea unidades completas.

TAREA: Generar una unidad didáctica completa para:

DATOS:
- Nivel: {datos.nivel}
- Curso: {datos.curso}
- Asignatura: {datos.asignatura}
- Título: {datos.titulo}
- Número de sesiones: {datos.num_sesiones}
- Trimestre: {datos.trimestre}

INSTRUCCIONES:
1. Crea una unidad didáctica COMPLETA lista para implementar
2. Apropiada para {datos.curso} de {datos.nivel}
3. Incluye:
   - Justificación y contextualización
   - Objetivos didácticos (5-7)
   - Competencias clave LOMLOE
   - Saberes básicos / Contenidos
   - Metodología
   - Temporalización ({datos.num_sesiones} sesiones detalladas)
   - Recursos y materiales
   - Evaluación (criterios, instrumentos)
   - Atención a la diversidad
   - Bibliografía
4. Cada sesión debe incluir:
   - Objetivos específicos
   - Actividades (inicio, desarrollo, cierre)
   - Tiempo estimado
   - Recursos necesarios
5. Cumple con LOMLOE 2024 y currículo de Extremadura
6. Formato profesional y estructurado

GENERA LA UNIDAD DIDÁCTICA:"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            temperature=0.6,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        contenido = message.content[0].text
        
        return {
            "success": True,
            "contenido": contenido,
            "nivel": datos.nivel,
            "curso": datos.curso,
            "asignatura": datos.asignatura,
            "titulo": datos.titulo,
            "tipo": "unidad-didactica"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar unidad didáctica: {str(e)}")

# ============================================
# ENDPOINT: SITUACIONES DE APRENDIZAJE
# ============================================

@app.post("/generar/situacion-aprendizaje")
async def generar_situacion_aprendizaje(datos: SituacionAprendizajeRequest):
    """
    Genera una situación de aprendizaje competencial completa.
    """
    
    try:
        competencias_texto = ""
        if datos.competencias_clave and len(datos.competencias_clave) > 0:
            competencias_texto = f"\nCompetencias clave a trabajar:\n" + "\n".join([f"- {c}" for c in datos.competencias_clave])
        
        prompt = f"""Eres un experto en diseño de situaciones de aprendizaje competenciales según LOMLOE.

TAREA: Generar una situación de aprendizaje completa para:

DATOS:
- Nivel: {datos.nivel}
- Curso: {datos.curso}
- Asignatura: {datos.asignatura}
- Tema/Reto: {datos.tema}
- Duración: {datos.duracion_sesiones} sesiones
{competencias_texto}

INSTRUCCIONES:
1. Crea una situación de aprendizaje COMPETENCIAL completa
2. Apropiada para {datos.curso} de {datos.nivel}
3. Debe incluir:
   - Identificación de la SA
   - Justificación (¿Por qué es relevante?)
   - Descripción del reto/problema
   - Objetivos de aprendizaje
   - Competencias específicas y clave
   - Saberes básicos
   - Metodología (ABP, cooperativo, etc.)
   - Secuencia didáctica ({datos.duracion_sesiones} sesiones detalladas)
   - Producto final
   - Evaluación (criterios, instrumentos, rúbrica)
   - Recursos y materiales
   - Atención a la diversidad
4. Debe ser contextualizada, significativa y motivadora
5. Enfoque competencial (aprender haciendo)
6. Cumple con LOMLOE 2024
7. Formato profesional

GENERA LA SITUACIÓN DE APRENDIZAJE:"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3500,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        contenido = message.content[0].text
        
        return {
            "success": True,
            "contenido": contenido,
            "nivel": datos.nivel,
            "curso": datos.curso,
            "asignatura": datos.asignatura,
            "tema": datos.tema,
            "tipo": "situacion-aprendizaje"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar situación de aprendizaje: {str(e)}")

# ============================================
# ENDPOINT: PROGRAMACIONES DIDÁCTICAS
# ============================================

@app.post("/generar/programacion-didactica")
async def generar_programacion_didactica(datos: ProgramacionDidacticaRequest):
    """
    Genera una programación didáctica anual completa.
    """
    
    try:
        prompt = f"""Eres un experto en programación didáctica española que crea programaciones anuales completas.

TAREA: Generar una programación didáctica anual para:

DATOS:
- Nivel: {datos.nivel}
- Curso: {datos.curso}
- Asignatura: {datos.asignatura}
- Centro educativo: {datos.centro}
- Curso académico: {datos.curso_academico}

INSTRUCCIONES:
1. Crea una programación didáctica COMPLETA para el curso completo
2. Apropiada para {datos.curso} de {datos.nivel}
3. Debe incluir:
   
   A. INTRODUCCIÓN Y CONTEXTUALIZACIÓN
   - Características del centro ({datos.centro})
   - Características del alumnado
   - Marco legal (LOMLOE, LOE, decretos autonómicos)
   
   B. OBJETIVOS
   - Objetivos de etapa
   - Objetivos de la asignatura
   - Contribución a competencias clave
   
   C. COMPETENCIAS
   - Competencias clave (CCL, CP, STEM, CD, CPSAA, CC, CE, CCEC)
   - Competencias específicas de la asignatura
   - Descriptores operativos
   
   D. SABERES BÁSICOS / CONTENIDOS
   - Organizados por trimestres
   - Bloques temáticos
   - Secuenciación y temporalización
   
   E. UNIDADES DIDÁCTICAS
   - Mínimo 9 unidades (3 por trimestre)
   - Título, temporalización, objetivos
   
   F. METODOLOGÍA
   - Principios metodológicos
   - Estrategias didácticas
   - Organización espacios y tiempos
   - Materiales y recursos
   
   G. EVALUACIÓN
   - Criterios de evaluación
   - Instrumentos de evaluación
   - Criterios de calificación
   - Recuperación
   
   H. ATENCIÓN A LA DIVERSIDAD
   - Medidas ordinarias
   - Medidas específicas
   - Adaptaciones
   
   I. ACTIVIDADES COMPLEMENTARIAS
   
4. Cumple con LOMLOE 2024 y Decreto de Extremadura
5. Formato profesional y estructurado
6. Listo para entregar a inspección

GENERA LA PROGRAMACIÓN DIDÁCTICA:"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            temperature=0.5,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        contenido = message.content[0].text
        
        return {
            "success": True,
            "contenido": contenido,
            "nivel": datos.nivel,
            "curso": datos.curso,
            "asignatura": datos.asignatura,
            "centro": datos.centro,
            "tipo": "programacion-didactica"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar programación didáctica: {str(e)}")

# ============================================
# ENDPOINT: ADAPTACIONES CURRICULARES
# ============================================

@app.post("/generar/adaptacion-curricular")
async def generar_adaptacion_curricular(datos: AdaptacionCurricularRequest):
    """
    Genera una adaptación curricular individualizada.
    """
    
    try:
        medidas_texto = ""
        if datos.medidas and len(datos.medidas) > 0:
            medidas_texto = f"\nMedidas específicas a considerar:\n" + "\n".join([f"- {m}" for m in datos.medidas])
        
        prompt = f"""Eres un experto en atención a la diversidad que crea adaptaciones curriculares.

TAREA: Generar una adaptación curricular para:

DATOS:
- Nivel: {datos.nivel}
- Curso: {datos.curso}
- Asignatura: {datos.asignatura}
- Tipo de adaptación: {datos.tipo_adaptacion}
- Necesidad específica: {datos.necesidad}
{medidas_texto}

INSTRUCCIONES:
1. Crea una adaptación curricular COMPLETA y profesional
2. Apropiada para {datos.curso} de {datos.nivel}
3. Debe incluir:
   
   A. DATOS DE IDENTIFICACIÓN
   - Alumno/a (datos anónimos)
   - Curso y grupo
   - Asignatura
   - Tipo de adaptación: {datos.tipo_adaptacion}
   
   B. INFORMACIÓN RELEVANTE
   - Necesidad específica: {datos.necesidad}
   - Nivel de competencia curricular
   - Estilo de aprendizaje
   - Intereses y motivación
   
   C. OBJETIVOS
   - Objetivos generales adaptados
   - Objetivos específicos
   - Priorización de objetivos
   
   D. COMPETENCIAS
   - Competencias a desarrollar
   - Nivel de logro esperado
   
   E. CONTENIDOS
   - Contenidos priorizados
   - Contenidos modificados
   - Contenidos ampliados (si enriquecimiento)
   
   F. METODOLOGÍA
   - Estrategias específicas
   - Recursos adaptados
   - Apoyo necesario
   - Organización del aula
   
   G. EVALUACIÓN
   - Criterios de evaluación adaptados
   - Instrumentos específicos
   - Procedimientos
   
   H. MEDIDAS Y RECURSOS
   - Medidas organizativas
   - Recursos personales
   - Recursos materiales
   - Apoyos necesarios
   
   I. COLABORACIÓN CON LA FAMILIA
   
   J. SEGUIMIENTO Y REVISIÓN
   
4. Cumple con normativa de atención a la diversidad
5. Formato profesional
6. Lenguaje claro y específico

GENERA LA ADAPTACIÓN CURRICULAR:"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3500,
            temperature=0.6,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        contenido = message.content[0].text
        
        return {
            "success": True,
            "contenido": contenido,
            "nivel": datos.nivel,
            "curso": datos.curso,
            "asignatura": datos.asignatura,
            "tipo_adaptacion": datos.tipo_adaptacion,
            "tipo": "adaptacion-curricular"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar adaptación curricular: {str(e)}")

# ============================================
# ENDPOINT DE PRUEBA
# ============================================

@app.get("/test/{generador}")
async def test_endpoint(generador: str):
    """
    Endpoint de prueba para verificar que todo funciona.
    """
    return {
        "message": f"Endpoint {generador} está activo",
        "status": "ready",
        "backend": "DocentIA v1.0.0"
    }

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
