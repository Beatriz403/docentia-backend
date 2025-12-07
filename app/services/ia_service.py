"""
Servicio de Inteligencia Artificial
Gestiona las llamadas a diferentes proveedores de IA (Claude, OpenAI, Gemini)
"""
import time
from typing import Dict, Any, Optional
from config import settings


class IAService:
    """Servicio para gestionar llamadas a diferentes proveedores de IA"""
    
    def __init__(self):
        self.claude_client = None
        self.openai_client = None
        self.gemini_client = None
        self.initialize_clients()
    
    def initialize_clients(self):
        """Inicializa los clientes de IA disponibles"""
        print("\n🔄 Inicializando clientes de IA...")
        
        # Claude
        if settings.ANTHROPIC_API_KEY:
            try:
                import anthropic
                self.claude_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                print("  ✅ Claude inicializado")
            except Exception as e:
                print(f"  ⚠️ Error inicializando Claude: {e}")
                self.claude_client = None
        
        # OpenAI (solo inicializar si está configurado)
        if settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                print("  ✅ OpenAI inicializado")
            except Exception as e:
                print(f"  ⚠️ Error inicializando OpenAI: {e}")
                self.openai_client = None
        
        # Gemini (solo inicializar si está configurado)
        if settings.GOOGLE_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.gemini_client = genai
                print("  ✅ Gemini inicializado")
            except Exception as e:
                print(f"  ⚠️ Error inicializando Gemini: {e}")
                self.gemini_client = None
    
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Genera contenido usando el proveedor de IA configurado
        
        Args:
            system_prompt: Instrucciones del sistema
            user_prompt: Prompt del usuario
            max_tokens: Máximo de tokens a generar
            temperature: Temperatura (creatividad) 0.0-1.0
        
        Returns:
            Dict con contenido, proveedor, modelo, tiempo, etc.
        """
        provider = settings.AI_PROVIDER.lower()
        
        if provider == "claude":
            return await self._generate_claude(system_prompt, user_prompt, max_tokens, temperature)
        elif provider == "openai":
            return await self._generate_openai(system_prompt, user_prompt, max_tokens, temperature)
        elif provider == "gemini":
            return await self._generate_gemini(system_prompt, user_prompt, max_tokens, temperature)
        else:
            raise ValueError(f"Proveedor no soportado: {provider}")
    
    async def _generate_claude(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float
    ) -> Dict[str, Any]:
        """Genera contenido usando Claude (Anthropic)"""
        
        if not self.claude_client:
            raise Exception("Cliente de Claude no inicializado. Verifica ANTHROPIC_API_KEY")
        
        inicio = time.time()
        
        try:
            print(f"\n🤖 Generando con Claude...")
            print(f"   Max tokens: {max_tokens}")
            print(f"   Temperature: {temperature}")
            
            response = self.claude_client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            tiempo_generacion = time.time() - inicio
            
            contenido = response.content[0].text
            tokens_usados = response.usage.input_tokens + response.usage.output_tokens
            
            print(f"   ✅ Generado en {tiempo_generacion:.2f}s")
            print(f"   📊 Tokens: {tokens_usados}")
            
            return {
                "contenido": contenido,
                "proveedor": "claude",
                "modelo": settings.CLAUDE_MODEL,
                "tiempo_generacion": tiempo_generacion,
                "tokens_usados": tokens_usados,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
            
        except Exception as e:
            print(f"   ❌ Error en Claude: {str(e)}")
            raise Exception(f"Error al generar con Claude: {str(e)}")
    
    async def _generate_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float
    ) -> Dict[str, Any]:
        """Genera contenido usando OpenAI"""
        
        if not self.openai_client:
            raise Exception("Cliente de OpenAI no inicializado. Verifica OPENAI_API_KEY")
        
        inicio = time.time()
        
        try:
            print(f"\n🤖 Generando con OpenAI...")
            
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            tiempo_generacion = time.time() - inicio
            
            contenido = response.choices[0].message.content
            tokens_usados = response.usage.total_tokens
            
            print(f"   ✅ Generado en {tiempo_generacion:.2f}s")
            print(f"   📊 Tokens: {tokens_usados}")
            
            return {
                "contenido": contenido,
                "proveedor": "openai",
                "modelo": settings.OPENAI_MODEL,
                "tiempo_generacion": tiempo_generacion,
                "tokens_usados": tokens_usados,
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens
            }
            
        except Exception as e:
            print(f"   ❌ Error en OpenAI: {str(e)}")
            raise Exception(f"Error al generar con OpenAI: {str(e)}")
    
    async def _generate_gemini(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float
    ) -> Dict[str, Any]:
        """Genera contenido usando Gemini"""
        
        if not self.gemini_client:
            raise Exception("Cliente de Gemini no inicializado. Verifica GOOGLE_API_KEY")
        
        inicio = time.time()
        
        try:
            print(f"\n🤖 Generando con Gemini...")
            
            model = self.gemini_client.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                }
            )
            
            # Combinar system y user prompt para Gemini
            prompt_completo = f"{system_prompt}\n\n{user_prompt}"
            
            response = model.generate_content(prompt_completo)
            
            tiempo_generacion = time.time() - inicio
            
            contenido = response.text
            
            print(f"   ✅ Generado en {tiempo_generacion:.2f}s")
            
            return {
                "contenido": contenido,
                "proveedor": "gemini",
                "modelo": settings.GEMINI_MODEL,
                "tiempo_generacion": tiempo_generacion,
                "tokens_usados": None  # Gemini no siempre proporciona esta info
            }
            
        except Exception as e:
            print(f"   ❌ Error en Gemini: {str(e)}")
            raise Exception(f"Error al generar con Gemini: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna el estado de los clientes de IA"""
        return {
            "provider_actual": settings.AI_PROVIDER,
            "claude": {
                "configurado": bool(settings.ANTHROPIC_API_KEY),
                "inicializado": self.claude_client is not None,
                "modelo": settings.CLAUDE_MODEL
            },
            "openai": {
                "configurado": bool(settings.OPENAI_API_KEY),
                "inicializado": self.openai_client is not None,
                "modelo": settings.OPENAI_MODEL
            },
            "gemini": {
                "configurado": bool(settings.GOOGLE_API_KEY),
                "inicializado": self.gemini_client is not None,
                "modelo": settings.GEMINI_MODEL
            }
        }


# Instancia global del servicio
ia_service = IAService()
