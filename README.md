# 🎓 DocentIA - Asistente IA para Profesores

**Recupera tu tiempo. Automatiza tu burocracia docente.**

Plataforma web que genera automáticamente documentación didáctica adaptada a LOMLOE y legislación de Extremadura usando Inteligencia Artificial.

---

## ⚠️ IMPORTANTE - VERSIÓN DE PYTHON

### **Requisito CRÍTICO:**

```
✅ USAR: Python 3.9, 3.10 o 3.11 (RECOMENDADO: 3.11)
❌ NO USAR: Python 3.12 o superior
```

**Razón:** La librería `python-docx` (para generar archivos Word) tiene incompatibilidades con Python 3.12+. Si usas Python 3.12, los documentos Word NO se generarán correctamente.

**Comprobar tu versión:**

```bash
python --version
```

Debe mostrar: `Python 3.11.x` o `Python 3.10.x` o `Python 3.9.x`

Si tienes Python 3.12+, consulta la sección [Instalar Python 3.11](#instalar-python-311) más abajo.

---

## 🚀 Características Principales

### ⚡ **Botón de Emergencia** (Diferenciador clave)

Genera actividades de aula completas en **30 segundos** para situaciones urgentes.

### 📚 **6 Generadores Profesionales:**

1. **Unidades Didácticas** completas y estructuradas
2. **Exámenes** con hoja de respuestas
3. **Rúbricas** de evaluación detalladas
4. **Situaciones de Aprendizaje** LOMLOE
5. **Informes a Familias** personalizados
6. **Generador de Ideas** didácticas creativas

---

## 🎯 Problema que Resuelve

Los profesores dedican **cientos de horas anuales** a documentación administrativa:

- Unidades didácticas
- Programaciones
- Exámenes y rúbricas
- Informes a familias
- Adaptaciones curriculares

**DocentIA automatiza este trabajo** respetando la legislación vigente de Extremadura.

---

## 📋 Requisitos del Sistema

### **Python:**

- ✅ **Python 3.9, 3.10 o 3.11** (RECOMENDADO: **3.11**)
- ❌ **NO usar Python 3.12+** (incompatibilidad con python-docx)
- ❌ **NO usar Python 3.8 o inferior** (desactualizado)

### **Otros requisitos:**

- Cuenta de Claude/OpenAI/Gemini (API key)
- 1GB de espacio en disco
- Conexión a internet (para llamadas a la API de IA)

---

## 🛠️ Instalación

### **Paso 1: Verificar versión de Python**

```bash
python --version
```

Si muestra `Python 3.12.x` o superior, **necesitas instalar Python 3.11** (ver sección abajo).

### **Paso 2: Clonar o descargar el proyecto**

```bash
# Si usas Git
git clone https://github.com/tuusuario/docentia.git
cd docentia

# O descarga el ZIP y descomprímelo
```

### **Paso 3: Crear entorno virtual**

**Windows:**

```powershell
# Si tienes Python 3.11
py -3.11 -m venv venv

# O simplemente
python -m venv venv

# Activar
venv\Scripts\activate
```

**Mac/Linux:**

```bash
# Si tienes Python 3.11
python3.11 -m venv venv

# O simplemente
python3 -m venv venv

# Activar
source venv/bin/activate
```

Verás `(venv)` al inicio de la línea del terminal.

### **Paso 4: Instalar dependencias**

```bash
pip install -r requirements.txt
```

Esto tardará 2-3 minutos.

### **Paso 5: Configurar variables de entorno**

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Windows:
copy .env.example .env
```

Edita el archivo `.env` y añade tu API key:

```bash
# Editar con VSCode, nano, notepad, etc.
# Reemplaza sk-ant-api03-xxxxx con tu API key real
ANTHROPIC_API_KEY=sk-ant-api03-tu_api_key_real_aqui
AI_PROVIDER=claude
```

### **Paso 6: Ejecutar la aplicación**

```bash
python main.py
```

Deberías ver:

```
====================================================
  🎓 DocentIA v1.0.0
====================================================
  📡 Servidor: http://0.0.0.0:8000
  📚 Documentación: http://0.0.0.0:8000/docs
  🤖 Proveedor IA: CLAUDE
====================================================
```

### **Paso 7: Abrir en el navegador**

Abre: **http://localhost:8000/docs**

Verás la documentación interactiva de la API donde puedes probar todos los endpoints.

---

## 🔧 Instalar Python 3.11

### **Si tienes Python 3.12+ y necesitas Python 3.11:**

#### **Windows:**

1. Ve a: https://www.python.org/downloads/
2. Busca **Python 3.11** (última versión 3.11.x)
3. Descarga e instala
4. **IMPORTANTE:** Durante la instalación marca "Add Python to PATH"
5. Verifica: `py -3.11 --version`

#### **Mac:**

```bash
# Usando Homebrew
brew install python@3.11

# Verificar
python3.11 --version
```

#### **Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# Verificar
python3.11 --version
```

Después, vuelve al **Paso 3** de la instalación usando `python3.11` específicamente.

---

## 🔑 Configuración de API Keys

### **Opción 1: Claude (Anthropic) - RECOMENDADO**

1. Crea cuenta en: https://console.anthropic.com/
2. Genera una API key
3. En tu archivo `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-tu_key_aqui
AI_PROVIDER=claude
CLAUDE_MODEL=claude-sonnet-4-20250514
```

### **Opción 2: OpenAI**

```bash
OPENAI_API_KEY=sk-tu_key_aqui
AI_PROVIDER=openai
OPENAI_MODEL=gpt-4o
```

### **Opción 3: Gemini (Google)**

```bash
GOOGLE_API_KEY=AIzaSy_tu_key_aqui
AI_PROVIDER=gemini
GEMINI_MODEL=gemini-pro
```

---

## 📂 Estructura del Proyecto

```
docentia/
├── app/
│   ├── models/           # Modelos Pydantic (requests/responses)
│   ├── services/         # Lógica de negocio (IA, documentos, export)
│   └── prompts/          # Prompts optimizados para cada generador
├── templates/            # HTML templates (generadores web)
├── static/               # CSS, JS, imágenes
├── main.py               # Punto de entrada FastAPI
├── config.py             # Configuración global
├── requirements.txt      # Dependencias Python
├── .env                  # Variables de entorno (TU API KEY)
├── .env.example          # Plantilla de .env
└── README.md             # Este archivo
```

---

## 🎨 Tecnologías

### **Backend:**

- **FastAPI** - Framework web moderno y rápido
- **Python 3.11** - Lenguaje principal
- **Anthropic Claude** - IA principal (recomendado)
- **python-docx** - Generación de archivos Word
- **Pydantic** - Validación de datos

### **Frontend:**

- **HTML5/CSS3** - Interfaz web
- **JavaScript Vanilla** - Sin frameworks pesados
- **Tailwind CSS** - Estilado moderno (opcional)

---

## 📖 Uso

### **1. Acceder a la API**

Abre `http://localhost:8000/docs` en tu navegador

### **2. Probar un endpoint**

Por ejemplo, generar una unidad didáctica:

**Endpoint:** `POST /api/generar/unidad`

**Body:**

```json
{
  "nivel": "Primaria",
  "curso": "3º de Primaria",
  "asignatura": "Lengua Castellana y Literatura",
  "tema": "El sustantivo y sus clases",
  "caracteristicas_grupo": "Grupo de 25 alumnos, 2 ACNEAE"
}
```

**Respuesta:**

```json
{
  "success": true,
  "data": {
    "contenido": "# Unidad Didáctica\n\n## 1. DATOS IDENTIFICATIVOS...",
    "proveedor": "claude",
    "modelo": "claude-sonnet-4-20250514",
    "tiempo_generacion": 15.3,
    "tokens_usados": 2500
  },
  "message": "Unidad didáctica generada correctamente",
  "timestamp": "2025-12-06T14:30:00"
}
```

### **3. Exportar a Word**

**Endpoint:** `POST /api/exportar/word`

Envía el contenido markdown generado y obtendrás un archivo .docx descargable.

---

## 🎓 Legislación Soportada

- ✅ **LOMLOE** (Ley Orgánica 3/2020)
- ✅ **Real Decreto 157/2022** (Currículo Primaria)
- ✅ **Real Decreto 217/2022** (Currículo ESO)
- ✅ **Decreto 107/2022** (Currículo Primaria Extremadura)
- ✅ **Decreto 110/2022** (Currículo ESO Extremadura)

---

## 🚀 Despliegue en Producción

### **Backend: Render (Gratuito)**

1. Crea cuenta en https://render.com
2. Conecta tu repositorio GitHub
3. Configura:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Añade variables de entorno (API keys)
5. Deploy

**URL resultante:** `https://docentia-api.onrender.com`

### **Frontend: Vercel (Gratuito)**

1. Sube tus HTML a Vercel
2. Actualiza la URL del backend en los archivos JavaScript
3. Deploy automático

**Más info:** Ver `docs/DESPLIEGUE.md` (próximamente)

---

## 🐛 Solución de Problemas

### **Error: "ModuleNotFoundError: No module named 'docx'"**

```bash
pip install python-docx
```

### **Error: "ANTHROPIC_API_KEY no configurada"**

- Revisa tu archivo `.env`
- Asegúrate de que la API key es correcta
- Verifica que el archivo `.env` está en la raíz del proyecto

### **Error: "collections.abc" o problemas con python-docx**

- **Causa:** Estás usando Python 3.12+
- **Solución:** Instala Python 3.11 y recrea el entorno virtual

### **El servidor no arranca**

```bash
# Verifica que estás en el entorno virtual
which python  # Mac/Linux
where python  # Windows

# Debe apuntar a tu carpeta venv

# Reinstala dependencias
pip install --upgrade -r requirements.txt
```

### **"Address already in use"**

```bash
# Puerto 8000 ocupado, usa otro:
uvicorn main:app --port 8001
```

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

---

## 👥 Autor

**Beatriz** - Creadora de DocentIA

- Proyecto FEUP Talent School 2025
- Email: contacto@docentia.com

---

## 🙏 Agradecimientos

- Profesores beta testers de Extremadura
- FEUP Talent School
- Comunidad educativa

---

## 📱 Contacto y Soporte

- **Web:** https://docentia.vercel.app
- **Email:** contacto@docentia.com
- **GitHub Issues:** Para reportar bugs o sugerir mejoras

---

## ⭐ Roadmap

### **Versión 1.0 (Actual - MVP)**

- [x] 6 Generadores básicos funcionando
- [x] Botón de Emergencia
- [x] Exportación Word
- [x] Legislación Extremadura
- [x] API REST completa

### **Versión 1.1 (Próximos meses)**

- [ ] Exportación PDF mejorada
- [ ] Más comunidades autónomas
- [ ] Generación de imágenes con IA
- [ ] Frontend completo con interfaz web
- [ ] Banco de actividades reutilizables

### **Versión 2.0 (Futuro)**

- [ ] App móvil (iOS/Android)
- [ ] Colaboración entre profesores
- [ ] IA personalizada por profesor
- [ ] Integración con plataformas educativas (Moodle, Google Classroom)

---

## 📊 Estado del Proyecto

- **Backend:** ✅ Completo y funcional
- **Frontend:** 🟡 En desarrollo (generadores HTML)
- **Testing:** 🟡 En progreso
- **Documentación:** ✅ Completa
- **Despliegue:** 🟡 Preparado (pendiente subir)

---

## ❓ FAQ

### **¿Cuánto cuesta usar DocentIA?**

El software es gratuito. Solo pagas por el uso de la API de IA:

- Claude: ~$0.003 por generación (~3€/1000 documentos)
- Costo estimado: 5-10€/mes para uso normal

### **¿Funciona sin internet?**

No, requiere conexión a internet para llamar a la API de IA.

### **¿Qué pasa con mis datos?**

- Los prompts se envían a Claude/OpenAI/Gemini
- No se almacenan datos personales de alumnos
- Los documentos generados son solo tuyos

### **¿Puedo usar DocentIA en otras comunidades?**

Sí, aunque está optimizado para Extremadura, puedes adaptarlo editando los prompts en `app/prompts/`

### **¿Necesito saber programar?**

No para usar la aplicación. Sí para modificarla o desplegarla.

---

**¿Listo para recuperar tu tiempo?** 🚀

[Empezar ahora](#instalación) | [Ver demo](#) | [Contacto](#contacto)

---

_Última actualización: 6 de diciembre de 2025_
_Versión: 1.0.0_
