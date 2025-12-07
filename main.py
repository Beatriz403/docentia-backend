"""
DocentIA - Aplicación principal FastAPI
Genera documentación didáctica adaptada a LOMLOE y decretos de Extremadura
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
import uvicorn

# Importar configuración
from config import settings

# Importar servicios
from app.services.ia_service import ia_service
from app.services.document_service import document_service
from app.services.export_service import export_service

# Importar modelos
from app.models.requests import (
    UnidadDidacticaRequest,
    RubricaRequest,
    ExamenRequest,
    SituacionAprendizajeRequest,
    InformeFamiliaRequest,
    IdeasRequest
)
from app.models.responses import GeneracionResponse, DocumentoGenerado


# ============================================
# LIFECYCLE EVENTS
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos del ciclo de vida de la aplicación"""
    # Startup
    print("\n" + "="*60)
    print(f"  🎓 {settings.APP_NAME} v{settings.APP_VERSION}")
    print("="*60)
    print(f"  📡 Servidor: http://{settings.HOST}:{settings.PORT}")
    print(f"  📚 Documentación: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"  🤖 Proveedor IA: {settings.AI_PROVIDER.upper()}")
    print("="*60 + "\n")
    
    yield
    
    # Shutdown
    print("\n👋 Cerrando DocentIA...")


# ============================================
# CREAR APLICACIÓN
# ============================================

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para generar documentación didáctica con IA",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# ENDPOINTS DE GENERACIÓN
# ============================================

@app.post("/api/generar/unidad", response_model=GeneracionResponse)
async def generar_unidad_didactica(request: UnidadDidacticaRequest):
    """Genera una Unidad Didáctica completa"""
    try:
        print(f"\n📚 Generando Unidad Didáctica: {request.asignatura} - {request.curso}")
        
        resultado = await document_service.generar_unidad_didactica(request)
        
        documento = DocumentoGenerado(**resultado)
        
        return GeneracionResponse(
            success=True,
            data=documento,
            message="Unidad didáctica generada correctamente",
            timestamp=datetime.now()
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generar/rubrica", response_model=GeneracionResponse)
async def generar_rubrica(request: RubricaRequest):
    """Genera una Rúbrica de Evaluación"""
    try:
        print(f"\n📋 Generando Rúbrica: {request.asignatura} - {request.tema}")
        
        resultado = await document_service.generar_rubrica(request)
        
        documento = DocumentoGenerado(**resultado)
        
        return GeneracionResponse(
            success=True,
            data=documento,
            message="Rúbrica generada correctamente",
            timestamp=datetime.now()
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generar/examen", response_model=GeneracionResponse)
async def generar_examen(request: ExamenRequest):
    """Genera un Examen completo"""
    try:
        print(f"\n📝 Generando Examen: {request.asignatura} - {request.tipo_examen}")
        
        resultado = await document_service.generar_examen(request)
        
        documento = DocumentoGenerado(**resultado)
        
        return GeneracionResponse(
            success=True,
            data=documento,
            message="Examen generado correctamente",
            timestamp=datetime.now()
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generar/situacion", response_model=GeneracionResponse)
async def generar_situacion_aprendizaje(request: SituacionAprendizajeRequest):
    """Genera una Situación de Aprendizaje LOMLOE"""
    try:
        print(f"\n🎯 Generando Situación de Aprendizaje: {request.asignatura}")
        
        resultado = await document_service.generar_situacion_aprendizaje(request)
        
        documento = DocumentoGenerado(**resultado)
        
        return GeneracionResponse(
            success=True,
            data=documento,
            message="Situación de aprendizaje generada correctamente",
            timestamp=datetime.now()
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generar/informe", response_model=GeneracionResponse)
async def generar_informe_familia(request: InformeFamiliaRequest):
    """Genera un Informe a Familias"""
    try:
        print(f"\n📧 Generando Informe a Familias: {request.nombre_alumno}")
        
        resultado = await document_service.generar_informe_familia(request)
        
        documento = DocumentoGenerado(**resultado)
        
        return GeneracionResponse(
            success=True,
            data=documento,
            message="Informe generado correctamente",
            timestamp=datetime.now()
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generar/ideas", response_model=GeneracionResponse)
async def generar_ideas(request: IdeasRequest):
    """Genera Ideas didácticas creativas"""
    try:
        print(f"\n💡 Generando Ideas: {request.asignatura} - {request.tema}")
        
        resultado = await document_service.generar_ideas(request)
        
        documento = DocumentoGenerado(**resultado)
        
        return GeneracionResponse(
            success=True,
            data=documento,
            message="Ideas generadas correctamente",
            timestamp=datetime.now()
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# ENDPOINT PARA EXPORTAR A WORD
# ============================================

@app.post("/api/exportar/word")
async def exportar_word(contenido: str, titulo: str = "Documento DocentIA"):
    """Exporta contenido markdown a Word (.docx)"""
    try:
        print(f"\n📄 Exportando a Word: {titulo}")
        
        # Crear documento Word
        doc = export_service.markdown_to_docx(contenido, titulo)
        
        # Guardar temporalmente
        nombre_archivo = f"{titulo.replace(' ', '_')}.docx"
        ruta = export_service.guardar_temporal(doc, nombre_archivo)
        
        print(f"   ✅ Documento creado: {nombre_archivo}")
        
        # Devolver archivo
        return FileResponse(
            ruta,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=nombre_archivo
        )
        
    except Exception as e:
        print(f"❌ Error al exportar: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# ENDPOINTS DE INFORMACIÓN
# ============================================

@app.get("/")
async def root():
    """Endpoint raíz - información de la API"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "provider": settings.AI_PROVIDER,
        "docs": "/docs",
        "message": "DocentIA API funcionando correctamente"
    }


@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    status = ia_service.get_status()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ia_providers": status
    }


@app.get("/api/test")
async def test_ia():
    """Prueba rápida de conexión con IA"""
    try:
        resultado = await ia_service.generate(
            system_prompt="Eres un asistente útil.",
            user_prompt="Responde solo con: OK",
            max_tokens=10,
            temperature=0
        )
        
        return {
            "success": True,
            "provider": resultado["proveedor"],
            "model": resultado["modelo"],
            "response": resultado["contenido"]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================
# EJECUTAR SERVIDOR
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info"
    )
