/**
 * ========================================
 * DOCENTIA - JAVASCRIPT COMÚN
 * Versión para Vercel (con detección automática)
 * ========================================
 */

// ========================================
// CONFIGURACIÓN GLOBAL CON DETECCIÓN DE ENTORNO
// ========================================

const DocentIA = {
    // Detecta automáticamente el entorno
    API_URL: (() => {
        // Si está en producción (Vercel), usa la variable de entorno
        if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
            // En Vercel, la URL del backend de producción
            return "https://docentia-api.onrender.com"; // ← CAMBIAR POR TU URL DE RENDER
        }
        // Si está en desarrollo local, usa localhost
        return "http://localhost:8000";
    })(),
    
    // Estado global
    documentoGenerado: null,
    
    // Información del entorno (útil para debugging)
    isDevelopment: typeof window !== 'undefined' && window.location.hostname === 'localhost',
    isProduction: typeof window !== 'undefined' && window.location.hostname !== 'localhost'
};

// Log de configuración (solo en desarrollo)
if (DocentIA.isDevelopment) {
    console.log('🔧 DocentIA en modo DESARROLLO');
    console.log('📡 API URL:', DocentIA.API_URL);
}

// ========================================
// FUNCIONES DE UTILIDAD
// ========================================

/**
 * Muestra una alerta temporal
 * @param {string} mensaje - Texto a mostrar
 * @param {string} tipo - 'error', 'success', 'info'
 * @param {number} duracion - Milisegundos (default: 5000)
 */
function mostrarAlerta(mensaje, tipo, duracion = 5000) {
    const alert = document.getElementById('alert');
    if (!alert) return;
    
    alert.textContent = mensaje;
    alert.className = `alert alert-${tipo} active`;
    
    setTimeout(() => {
        alert.classList.remove('active');
    }, duracion);
}

/**
 * Muestra el estado de carga
 */
function mostrarLoading() {
    const formulario = document.getElementById('formulario');
    const loading = document.getElementById('loading');
    const resultado = document.getElementById('resultado');
    
    if (formulario) formulario.style.display = 'none';
    if (loading) loading.classList.add('active');
    if (resultado) resultado.classList.remove('active');
}

/**
 * Oculta el estado de carga
 */
function ocultarLoading() {
    const loading = document.getElementById('loading');
    if (loading) loading.classList.remove('active');
}

/**
 * Muestra el formulario
 */
function mostrarFormulario() {
    const formulario = document.getElementById('formulario');
    const loading = document.getElementById('loading');
    const resultado = document.getElementById('resultado');
    
    if (formulario) formulario.style.display = 'block';
    if (loading) loading.classList.remove('active');
    if (resultado) resultado.classList.remove('active');
}

/**
 * Muestra el resultado
 * @param {string} contenido - Contenido generado
 */
function mostrarResultado(contenido) {
    const loading = document.getElementById('loading');
    const resultado = document.getElementById('resultado');
    const resultadoTexto = document.getElementById('resultadoTexto');
    
    if (loading) loading.classList.remove('active');
    if (resultado) resultado.classList.add('active');
    if (resultadoTexto) resultadoTexto.textContent = contenido;
    
    // Guardar para descarga
    DocentIA.documentoGenerado = contenido;
}

/**
 * Limpia y resetea el formulario
 * @param {HTMLFormElement} form - Formulario a limpiar
 */
function limpiarFormulario(form) {
    if (!form) return;
    
    form.reset();
    
    // Resetear selects dependientes
    const selects = form.querySelectorAll('select[disabled]');
    selects.forEach(select => {
        select.innerHTML = '<option value="">Selecciona primero...</option>';
    });
    
    // Ocultar campos "otro"
    const otrosContainers = form.querySelectorAll('.otro-especificar');
    otrosContainers.forEach(container => {
        container.classList.remove('visible');
        const input = container.querySelector('input');
        if (input) input.required = false;
    });
    
    mostrarFormulario();
    window.scrollTo(0, 0);
}

// ========================================
// MANEJO DE DESPLEGABLES RELACIONADOS
// ========================================

/**
 * Configura desplegables relacionados (Nivel → Curso → Asignatura)
 * @param {Object} datos - Objeto con la estructura de datos
 */
function configurarDesplegablesRelacionados(datos) {
    const nivelSelect = document.getElementById('nivel');
    const cursoSelect = document.getElementById('curso');
    const asignaturaSelect = document.getElementById('asignatura');
    
    if (!nivelSelect || !cursoSelect || !asignaturaSelect) return;
    
    // Cuando cambia el NIVEL
    nivelSelect.addEventListener('change', function() {
        const nivel = this.value;
        
        // Resetear curso y asignatura
        cursoSelect.innerHTML = '<option value="">Selecciona un curso</option>';
        asignaturaSelect.innerHTML = '<option value="">Selecciona primero un curso</option>';
        asignaturaSelect.disabled = true;
        
        if (nivel && datos[nivel]) {
            cursoSelect.disabled = false;
            
            // Llenar cursos
            datos[nivel].cursos.forEach(curso => {
                const option = document.createElement('option');
                option.value = curso;
                option.textContent = curso;
                cursoSelect.appendChild(option);
            });
        } else {
            cursoSelect.disabled = true;
        }
    });
    
    // Cuando cambia el CURSO
    cursoSelect.addEventListener('change', function() {
        const nivel = nivelSelect.value;
        const curso = this.value;
        
        // Resetear asignatura
        asignaturaSelect.innerHTML = '<option value="">Selecciona una asignatura</option>';
        
        if (nivel && curso && datos[nivel].asignaturas[curso]) {
            asignaturaSelect.disabled = false;
            
            // Llenar asignaturas
            datos[nivel].asignaturas[curso].forEach(asignatura => {
                const option = document.createElement('option');
                option.value = asignatura;
                option.textContent = asignatura;
                asignaturaSelect.appendChild(option);
            });
        } else {
            asignaturaSelect.disabled = true;
        }
    });
}

/**
 * Configura desplegable con opción "Otro"
 * @param {string} selectId - ID del select
 * @param {string} containerId - ID del contenedor del input "otro"
 * @param {string} inputId - ID del input "otro"
 */
function configurarOtroEspecificar(selectId, containerId, inputId) {
    const select = document.getElementById(selectId);
    const container = document.getElementById(containerId);
    const input = document.getElementById(inputId);
    
    if (!select || !container || !input) return;
    
    select.addEventListener('change', function() {
        if (this.value === "Otro (especificar)") {
            container.classList.add('visible');
            input.required = true;
        } else {
            container.classList.remove('visible');
            input.required = false;
            input.value = '';
        }
    });
}

// ========================================
// LLAMADAS A LA API
// ========================================

/**
 * Genera contenido llamando al backend
 * @param {string} endpoint - Endpoint de la API (ej: '/api/generar/unidad')
 * @param {Object} datos - Datos a enviar
 * @returns {Promise<Object>} Respuesta del servidor
 */
async function generarContenido(endpoint, datos) {
    mostrarLoading();
    
    try {
        const url = `${DocentIA.API_URL}${endpoint}`;
        
        // Log en desarrollo
        if (DocentIA.isDevelopment) {
            console.log('📤 Enviando a:', url);
            console.log('📦 Datos:', datos);
        }
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error al generar el contenido');
        }
        
        const data = await response.json();
        
        // Log en desarrollo
        if (DocentIA.isDevelopment) {
            console.log('📥 Respuesta recibida:', data);
        }
        
        return data;
        
    } catch (error) {
        console.error('❌ Error:', error);
        ocultarLoading();
        mostrarFormulario();
        
        // Mensaje de error más descriptivo
        if (error.message.includes('Failed to fetch')) {
            throw new Error('No se pudo conectar con el servidor. Verifica que el backend esté funcionando.');
        }
        
        throw error;
    }
}

/**
 * Descarga el documento generado en formato Word
 * @param {string} titulo - Título del archivo
 */
async function descargarDocumento(titulo) {
    if (!DocentIA.documentoGenerado) {
        mostrarAlerta('❌ No hay documento para descargar', 'error');
        return;
    }
    
    try {
        const url = `${DocentIA.API_URL}/api/exportar/word`;
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contenido: DocentIA.documentoGenerado,
                titulo: titulo
            })
        });
        
        if (!response.ok) {
            throw new Error('Error al descargar el documento');
        }
        
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `${titulo}_${new Date().getTime()}.docx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);
        
        mostrarAlerta('✅ Documento descargado correctamente', 'success');
        
    } catch (error) {
        console.error('Error:', error);
        mostrarAlerta('❌ Error al descargar el documento', 'error');
    }
}

// ========================================
// VALIDACIÓN DE FORMULARIOS
// ========================================

/**
 * Valida que todos los campos requeridos estén completos
 * @param {HTMLFormElement} form - Formulario a validar
 * @returns {boolean} true si es válido
 */
function validarFormulario(form) {
    const campos = form.querySelectorAll('[required]');
    let valido = true;
    
    campos.forEach(campo => {
        if (!campo.value.trim()) {
            valido = false;
            campo.style.borderColor = '#ef4444';
        } else {
            campo.style.borderColor = '#e5e7eb';
        }
    });
    
    return valido;
}

/**
 * Valida campo "Otro" si está seleccionado
 * @param {string} selectId - ID del select
 * @param {string} inputId - ID del input "otro"
 * @returns {boolean} true si es válido
 */
function validarOtro(selectId, inputId) {
    const select = document.getElementById(selectId);
    const input = document.getElementById(inputId);
    
    if (!select || !input) return true;
    
    if (select.value === "Otro (especificar)" && !input.value.trim()) {
        mostrarAlerta('❌ Por favor especifica la opción', 'error');
        input.focus();
        return false;
    }
    
    return true;
}

// ========================================
// HELPERS DE DATOS
// ========================================

/**
 * Obtiene el valor final de un campo con opción "Otro"
 * @param {string} selectId - ID del select
 * @param {string} inputId - ID del input "otro"
 * @returns {string} Valor final
 */
function obtenerValorConOtro(selectId, inputId) {
    const select = document.getElementById(selectId);
    const input = document.getElementById(inputId);
    
    if (!select) return '';
    
    if (select.value === "Otro (especificar)" && input) {
        return input.value.trim();
    }
    
    return select.value;
}

// ========================================
// INICIALIZACIÓN
// ========================================

/**
 * Inicializa comportamientos comunes al cargar la página
 */
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar información del entorno en consola
    if (DocentIA.isDevelopment) {
        console.log('🎓 DocentIA Frontend cargado');
        console.log('🌍 Entorno:', DocentIA.isDevelopment ? 'DESARROLLO' : 'PRODUCCIÓN');
        console.log('📡 API:', DocentIA.API_URL);
    }
    
    // Botón limpiar (si existe)
    const btnLimpiar = document.getElementById('btnLimpiar');
    if (btnLimpiar) {
        const form = document.getElementById('problemasForm') || 
                     document.getElementById('emergenciaForm') ||
                     document.querySelector('form');
        
        btnLimpiar.addEventListener('click', function() {
            limpiarFormulario(form);
        });
    }
    
    // Botón nueva generación (si existe)
    const btnNuevos = document.getElementById('btnNuevos') || 
                      document.getElementById('btnNueva');
    if (btnNuevos) {
        const form = document.getElementById('problemasForm') || 
                     document.getElementById('emergenciaForm') ||
                     document.querySelector('form');
        
        btnNuevos.addEventListener('click', function() {
            limpiarFormulario(form);
        });
    }
});

// ========================================
// EXPORTAR FUNCIONES GLOBALES
// ========================================

// Hacer funciones disponibles globalmente
window.DocentIA = DocentIA;
window.mostrarAlerta = mostrarAlerta;
window.mostrarLoading = mostrarLoading;
window.ocultarLoading = ocultarLoading;
window.mostrarFormulario = mostrarFormulario;
window.mostrarResultado = mostrarResultado;
window.limpiarFormulario = limpiarFormulario;
window.configurarDesplegablesRelacionados = configurarDesplegablesRelacionados;
window.configurarOtroEspecificar = configurarOtroEspecificar;
window.generarContenido = generarContenido;
window.descargarDocumento = descargarDocumento;
window.validarFormulario = validarFormulario;
window.validarOtro = validarOtro;
window.obtenerValorConOtro = obtenerValorConOtro;
