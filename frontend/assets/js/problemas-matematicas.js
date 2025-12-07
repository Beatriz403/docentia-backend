/**
 * ========================================
 * PROBLEMAS DE MATEMÁTICAS - JAVASCRIPT
 * ========================================
 */

// Temáticas por curso
const tematicasPorCurso = {
    "1º de Primaria": [
        "Números hasta el 99 (sumar y restar)",
        "Decenas y unidades",
        "Problemas de sumas sencillas",
        "Problemas de restas sencillas",
        "Comparar cantidades (mayor, menor, igual)",
        "Iniciación a la multiplicación (sumas repetidas)",
        "Medidas: longitud y peso (largo/corto, pesado/ligero)",
        "Dinero: monedas de euro",
        "Tiempo: horas en punto",
        "Figuras geométricas básicas",
        "Otro (especificar)"
    ],
    "2º de Primaria": [
        "Números hasta el 999",
        "Sumas y restas con llevadas",
        "Iniciación a la multiplicación (tablas 2, 5, 10)",
        "Problemas de dos operaciones",
        "Medidas de longitud: metro, centímetro",
        "Medidas de peso: kilo y medio kilo",
        "Medidas de capacidad: litro y medio litro",
        "Dinero: euros y céntimos",
        "Tiempo: horas y medias horas",
        "Formas geométricas y sus elementos",
        "Otro (especificar)"
    ],
    "3º de Primaria": [
        "Números hasta el 9.999",
        "Las cuatro operaciones básicas",
        "Multiplicaciones por una cifra (tablas del 1 al 10)",
        "Divisiones exactas sencillas",
        "Fracciones sencillas (mitad, tercio, cuarto)",
        "Medidas de longitud: km, m, cm",
        "Medidas de peso: tonelada, kg, gramo",
        "Medidas de capacidad: litro, medio litro, cuarto",
        "Tiempo: horas, minutos, días, meses",
        "Perímetros de figuras",
        "Problemas de dos y tres operaciones",
        "Otro (especificar)"
    ],
    "4º de Primaria": [
        "Números hasta el millón",
        "Multiplicaciones por dos y tres cifras",
        "Divisiones por una y dos cifras",
        "Fracciones: equivalentes, comparación",
        "Números decimales: décimas y centésimas",
        "Sumas y restas con decimales",
        "Medidas: conversiones simples",
        "Área de cuadrados y rectángulos",
        "Problemas con varias operaciones",
        "Proporcionalidad directa sencilla",
        "Gráficos de barras",
        "Otro (especificar)"
    ],
    "5º de Primaria": [
        "Números hasta los millones",
        "Operaciones combinadas (jerarquía)",
        "Fracciones: operaciones básicas",
        "Números decimales: operaciones",
        "Porcentajes sencillos (10%, 25%, 50%)",
        "Proporcionalidad y regla de tres",
        "Medidas: todas las conversiones",
        "Área y perímetro de polígonos",
        "Volumen: unidades cúbicas",
        "Problemas de múltiples pasos",
        "Media aritmética",
        "Probabilidad básica",
        "Otro (especificar)"
    ],
    "6º de Primaria": [
        "Operaciones con números naturales y decimales",
        "Fracciones: todas las operaciones",
        "Porcentajes: cálculo y problemas",
        "Proporcionalidad directa e inversa",
        "Escalas y planos",
        "Área de polígonos y círculo",
        "Volumen de cuerpos geométricos",
        "Coordenadas cartesianas",
        "Estadística: media, moda, mediana",
        "Probabilidad",
        "Problemas complejos de razonamiento",
        "Otro (especificar)"
    ]
};

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    const cursoSelect = document.getElementById('curso');
    const tematicaSelect = document.getElementById('tematica');
    const form = document.getElementById('problemasForm');
    const btnDescargar = document.getElementById('btnDescargar');
    
    // Configurar cambio de curso
    if (cursoSelect && tematicaSelect) {
        cursoSelect.addEventListener('change', handleCursoChange);
    }
    
    // Configurar opción "Otro"
    configurarOtroEspecificar('tematica', 'otroContainer', 'otraTematica');
    
    // Configurar formulario
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }
    
    // Configurar botón descargar
    if (btnDescargar) {
        btnDescargar.addEventListener('click', handleDescargar);
    }
});

// ========================================
// HANDLERS
// ========================================

function handleCursoChange() {
    const curso = document.getElementById('curso').value;
    const tematicaSelect = document.getElementById('tematica');
    const otroContainer = document.getElementById('otroContainer');
    const otraTematica = document.getElementById('otraTematica');
    
    // Resetear
    tematicaSelect.innerHTML = '<option value="">Selecciona una temática</option>';
    if (otroContainer) otroContainer.classList.remove('visible');
    if (otraTematica) {
        otraTematica.value = '';
        otraTematica.required = false;
    }
    
    // Llenar temáticas del curso seleccionado
    if (curso && tematicasPorCurso[curso]) {
        tematicasPorCurso[curso].forEach(tematica => {
            const option = document.createElement('option');
            option.value = tematica;
            option.textContent = tematica;
            tematicaSelect.appendChild(option);
        });
    }
}

async function handleSubmit(e) {
    e.preventDefault();
    
    // Validar campo "Otro" si está seleccionado
    if (!validarOtro('tematica', 'otraTematica')) {
        return;
    }
    
    // Obtener temática final
    const tematicaFinal = obtenerValorConOtro('tematica', 'otraTematica');
    
    const datos = {
        nivel: "Primaria",
        curso: document.getElementById('curso').value,
        tematica: tematicaFinal,
        dificultad: document.getElementById('dificultad').value,
        numero_problemas: parseInt(document.getElementById('numeroProblemas').value),
        incluir_soluciones: document.getElementById('incluirSoluciones').checked,
        contexto: document.getElementById('contexto').value.trim() || null
    };
    
    try {
        const response = await generarContenido('/api/generar/problemas-matematicas', datos);
        mostrarResultado(response.data.contenido);
    } catch (error) {
        mostrarAlerta('❌ Error al generar los problemas. Por favor, inténtalo de nuevo.', 'error');
    }
}

function handleDescargar() {
    const tematica = obtenerValorConOtro('tematica', 'otraTematica');
    const curso = document.getElementById('curso').value;
    const titulo = `Problemas_Matematicas_${curso}_${tematica}_${new Date().toLocaleDateString()}`;
    descargarDocumento(titulo);
}
