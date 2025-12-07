# 📁 FRONTEND DOCENTIA - ESTRUCTURA

## 📂 Estructura de carpetas

```
frontend/
│
├── index.html                      # Página principal con menú
│
├── generadores/                    # Generadores HTML
│   ├── boton-emergencia.html
│   ├── problemas-matematicas.html
│   ├── unidades-didacticas.html (pendiente)
│   ├── examenes.html (pendiente)
│   ├── rubricas.html (pendiente)
│   ├── situaciones-aprendizaje.html (pendiente)
│   ├── informes-familias.html (pendiente)
│   └── ideas.html (pendiente)
│
└── assets/
    ├── css/
    │   └── common.css              # Estilos compartidos
    │
    ├── js/
    │   ├── common.js               # Funciones JavaScript compartidas
    │   ├── boton-emergencia.js     # JS específico botón emergencia
    │   └── problemas-matematicas.js # JS específico problemas
    │
    └── images/
        └── (logos, iconos, etc.)
```

---

## 🎨 CSS COMÚN (common.css)

Incluye todos los estilos compartidos:
- ✅ Reset y tipografía base
- ✅ Navbar
- ✅ Page headers
- ✅ Cards
- ✅ Formularios (inputs, selects, textareas)
- ✅ Botones
- ✅ Estados de carga (spinner)
- ✅ Alertas
- ✅ Footer
- ✅ Responsive design

**Ventajas:**
- Un solo archivo CSS para mantener
- Estilos consistentes en todos los generadores
- Cambios centralizados

---

## ⚙️ JAVASCRIPT COMÚN (common.js)

Funciones reutilizables disponibles globalmente:

### **Funciones de UI:**
```javascript
mostrarAlerta(mensaje, tipo, duracion)  // Muestra alertas temporales
mostrarLoading()                         // Muestra estado de carga
ocultarLoading()                         // Oculta estado de carga
mostrarFormulario()                      // Muestra el formulario
mostrarResultado(contenido)              // Muestra el resultado generado
limpiarFormulario(form)                  // Resetea el formulario
```

### **Funciones de API:**
```javascript
generarContenido(endpoint, datos)       // Llama al backend
descargarDocumento(titulo)               // Descarga Word
```

### **Funciones de formularios:**
```javascript
configurarDesplegablesRelacionados(datos) // Nivel → Curso → Asignatura
configurarOtroEspecificar(selectId, containerId, inputId) // Campo "Otro"
validarFormulario(form)                  // Valida campos requeridos
validarOtro(selectId, inputId)          // Valida campo "Otro"
obtenerValorConOtro(selectId, inputId)  // Obtiene valor final
```

### **Objeto global:**
```javascript
DocentIA = {
    API_URL: "http://localhost:8000",   // URL del backend
    documentoGenerado: null              // Documento actual
}
```

---

## 📄 JAVASCRIPT ESPECÍFICO

Cada generador tiene su propio archivo JS con:
- **Datos específicos** (temáticas, opciones, etc.)
- **Inicialización** del formulario
- **Handlers** de eventos (submit, clicks, etc.)

### **Ejemplo: boton-emergencia.js**
```javascript
// Datos educativos (Primaria, ESO, asignaturas)
const datosEducativos = { ... };

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    configurarDesplegablesRelacionados(datosEducativos);
    // ... más configuración
});

// Handlers
async function handleSubmit(e) {
    // Lógica específica del generador
}
```

---

## 🔗 CÓMO ENLAZAR EN HTML

### **En cada HTML de generador:**

```html
<head>
    <!-- CSS Común -->
    <link rel="stylesheet" href="../assets/css/common.css">
</head>

<body>
    <!-- Contenido HTML aquí -->
    
    <!-- JavaScript al final del body -->
    <script src="../assets/js/common.js"></script>
    <script src="../assets/js/nombre-generador.js"></script>
</body>
```

**IMPORTANTE:**
- CSS en `<head>`
- JavaScript al final del `<body>`
- Primero `common.js`, luego el específico

---

## 🚀 CÓMO CREAR UN NUEVO GENERADOR

### **1. Crear HTML**
```html
<!-- frontend/generadores/mi-generador.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi Generador - DocentIA</title>
    <link rel="stylesheet" href="../assets/css/common.css">
</head>
<body>
    <!-- Navbar, header, formulario, etc. -->
    
    <script src="../assets/js/common.js"></script>
    <script src="../assets/js/mi-generador.js"></script>
</body>
</html>
```

### **2. Crear JavaScript específico**
```javascript
// frontend/assets/js/mi-generador.js

// Datos específicos
const misDatos = { ... };

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('miForm');
    form.addEventListener('submit', handleSubmit);
});

// Handler de submit
async function handleSubmit(e) {
    e.preventDefault();
    
    const datos = {
        campo1: document.getElementById('campo1').value,
        campo2: document.getElementById('campo2').value
    };
    
    try {
        const response = await generarContenido('/api/mi-endpoint', datos);
        mostrarResultado(response.data.contenido);
    } catch (error) {
        mostrarAlerta('Error al generar', 'error');
    }
}
```

### **3. Añadir al menú**
```html
<!-- frontend/index.html -->
<a href="generadores/mi-generador.html" class="card">
    <h2>🎯 Mi Generador</h2>
    <p>Descripción breve</p>
</a>
```

---

## 🎯 VENTAJAS DE ESTA ESTRUCTURA

### ✅ **Mantenibilidad:**
- Cambios de estilo en un solo archivo
- Funciones reutilizables centralizadas
- Código organizado y limpio

### ✅ **Escalabilidad:**
- Fácil añadir nuevos generadores
- No duplicar código
- Módulos independientes

### ✅ **Rendimiento:**
- CSS y JS se cachean en el navegador
- Carga más rápida en navegaciones posteriores

### ✅ **DRY (Don't Repeat Yourself):**
- Sin código duplicado
- Cambios propagados automáticamente

---

## 🔧 CONFIGURACIÓN

### **Cambiar URL del backend:**

Edita `frontend/assets/js/common.js`:

```javascript
const DocentIA = {
    API_URL: "https://tu-backend-produccion.com",  // Cambiar aquí
    documentoGenerado: null
};
```

### **Añadir estilos específicos:**

Si un generador necesita estilos únicos:

```html
<head>
    <link rel="stylesheet" href="../assets/css/common.css">
    <style>
        /* Estilos específicos aquí */
        .mi-clase-especial {
            color: red;
        }
    </style>
</head>
```

O crear archivo CSS específico:
```html
<link rel="stylesheet" href="../assets/css/mi-generador.css">
```

---

## 📋 CHECKLIST PARA NUEVOS GENERADORES

- [ ] Crear HTML en `generadores/`
- [ ] Enlazar `common.css`
- [ ] Crear JS específico en `assets/js/`
- [ ] Enlazar `common.js` y JS específico
- [ ] Añadir al menú principal (`index.html`)
- [ ] Probar funcionalidad completa
- [ ] Verificar responsive design

---

## 🐛 DEBUGGING

### **Si no funciona el CSS:**
1. Verificar ruta: `../assets/css/common.css`
2. Abrir DevTools (F12) → Network → Ver si carga el CSS
3. Verificar ruta relativa desde donde está el HTML

### **Si no funciona el JavaScript:**
1. Abrir Console (F12) → Ver errores
2. Verificar que `common.js` carga primero
3. Verificar rutas relativas
4. Comprobar que funciones están en `window`

### **Si no conecta con el backend:**
1. Verificar `DocentIA.API_URL` en `common.js`
2. Verificar CORS en backend
3. Verificar que backend está corriendo
4. Ver Console → Network → Ver respuestas de la API

---

## 💡 TIPS

1. **Siempre** carga `common.js` antes que los específicos
2. **Siempre** pon JavaScript al final del `<body>`
3. **Usa** funciones globales de `common.js` para mantener consistencia
4. **Reutiliza** las clases CSS de `common.css`
5. **Testea** en modo responsive (DevTools → Toggle device toolbar)

---

## 📞 SOPORTE

Si tienes dudas:
1. Revisa este README
2. Mira ejemplos existentes (`boton-emergencia.html`)
3. Consulta `common.js` para funciones disponibles
4. Revisa Console del navegador para errores

---

**¡Estructura lista para escalar! 🚀**
