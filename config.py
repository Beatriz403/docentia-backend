"""
Configuración global de DocentIA
Gestiona variables de entorno y settings del sistema
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # === INFORMACIÓN DE LA APP ===
    APP_NAME: str = os.getenv("APP_NAME", "DocentIA")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    
    # === SERVIDOR ===
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # === RUTAS ===
    TEMPLATES_DIR: str = os.getenv("TEMPLATES_DIR", "templates")
    STATIC_DIR: str = os.getenv("STATIC_DIR", "static")
    
    # === CORS ===
    CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://docentia-frontend.vercel.app"
]    
    # === PROVEEDORES DE IA ===
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "claude")  # claude, openai, gemini
    
    # Claude (Anthropic)
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Gemini (Google)
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-pro")
    
    def validate_api_keys(self):
        """Valida que al menos una API key esté configurada"""
        if self.AI_PROVIDER == "claude" and not self.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY no configurada")
        if self.AI_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no configurada")
        if self.AI_PROVIDER == "gemini" and not self.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY no configurada")
    
    def get_provider_info(self):
        """Retorna información del proveedor actual"""
        providers = {
            "claude": {"name": "Claude (Anthropic)", "model": self.CLAUDE_MODEL, "configured": bool(self.ANTHROPIC_API_KEY)},
            "openai": {"name": "OpenAI GPT-4", "model": self.OPENAI_MODEL, "configured": bool(self.OPENAI_API_KEY)},
            "gemini": {"name": "Google Gemini", "model": self.GEMINI_MODEL, "configured": bool(self.GOOGLE_API_KEY)}
        }
        return providers
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()

# Validar configuración al iniciar
try:
    settings.validate_api_keys()
    print(f"✅ Configuración válida - Proveedor: {settings.AI_PROVIDER}")
except ValueError as e:
    print(f"⚠️ Advertencia: {e}")
    print("   Por favor configura tu API key en el archivo .env")
