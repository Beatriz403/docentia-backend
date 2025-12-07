/**
 * ========================================
 * BOTÓN DE EMERGENCIA - JAVASCRIPT
 * ========================================
 */

// Datos educativos (Niveles, Cursos, Asignaturas)
const datosEducativos = {
    "Primaria": {
        cursos: [
            "1º de Primaria",
            "2º de Primaria",
            "3º de Primaria",
            "4º de Primaria",
            "5º de Primaria",
            "6º de Primaria"
        ],
        asignaturas: {
            "1º de Primaria": [
                "Lengua Castellana y Literatura",
                "Matemáticas",
                "Conocimiento del Medio Natural, Social y Cultural",
                "Educación Artística",
                "Educación Física",
                "Lengua Extranjera (Inglés)"
            ],
            "2º de Primaria": [
                "Lengua Castellana y Literatura",
                "Matemáticas",
                "Conocimiento del Medio Natural, Social y Cultural",
                "Educación Artística",
                "Educación Física",
                "Lengua Extranjera (Inglés)"
            ],
            "3º de Primaria": [
                "Lengua Castellana y Literatura",
                "Matemáticas",
                "Conocimiento del Medio Natural, Social y Cultural",
                "Educación Artística",
                "Educación Física",
                "Lengua Extranjera (Inglés)"
            ],
            "4º de Primaria": [
                "Lengua Castellana y Literatura",
                "Matemáticas",
                "Conocimiento del Medio Natural, Social y Cultural",
                "Educación Artística",
                "Educación Física",
                "Lengua Extranjera (Inglés)"
            ],
            "5º de Primaria": [
                "Lengua Castellana y Literatura",
                "Matemáticas",
                "Conocimiento del Medio Natural, Social y Cultural",
                "Educación Artística",
                "Educación Física",
                "Lengua Extranjera (Inglés)",
                "Educación en Valores Cívicos y Éticos"
            ],
            "6º de Primaria": [
                "Lengua Castellana y Literatura",
                "Matemáticas",
                "Conocimiento del Medio Natural, Social y Cultural",
                "Educación Artística",
                "Educación Física",
                "Lengua Extranjera (Inglés)",
                "Educación en Valores Cívicos y Éticos"
            ]
        }
    },
    "ESO": {
        cursos: [
            "1º de ESO",
            "2º de ESO",
            "3º de ESO",
            "4º de ESO"
        ],
        asignaturas: {
            "1º de ESO": [
                "Lengua Castellana y Literatura",
                "Matemáticas",
                "Biología y Geología",
                "Geografía e Historia",
                "Lengua Extranjera (Inglés)",
                "Educación Física",
                "Educación Plástica, Visual y Audiovisual",
                "Música",
                "Tecnología y Digitalización"
            ],
            "2º de ESO": [
                "Lengua Castellana y Literatura",
                "Matemáticas",
                "Física y Química",
                "Geografía e Historia",
                "Lengua Extranjera (Inglés)",
                "Educación Física",
                "Educación Plástica, Visual y Audiovisual",
                "Música",
                "Tecnología y Digitalización",
                "Educación en Valores Cívicos y Éticos"
            ],
            "3º de ESO": [
                "Lengua Castellana y Literatura",
                "Matemáticas",
                "Biología y Geología",
                "Física y Química",
                "Geografía e Historia",
                "Lengua Extranjera (Inglés)",
                "Educación Física",
                "Tecnología y Digitalización"
            ],
            "4º de ESO": [
                "Lengua Castellana y Literatura",
                "Matemáticas A",
                "Matemáticas B",
                "Geografía e Historia",
                "Lengua Extranjera (Inglés)",
                "Educación Física",
                "Biología y Geología",
                "Física y Química",
                "Economía y Emprendimiento",
                "Latín",
                "Tecnología"
            ]
        }
    }
};

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Configurar desplegables relacionados
    configurarDesplegablesRelacionados(datosEducativos);
    
    // Configurar formulario
    const form = document.getElementById('emergenciaForm');
    const btnDescargar = document.getElementById('btnDescargar');
    
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }
    
    if (btnDescargar) {
        btnDescargar.addEventListener('click', handleDescargar);
    }
});

// ========================================
// HANDLERS
// ========================================

async function handleSubmit(e) {
    e.preventDefault();
    
    const datos = {
        nivel: document.getElementById('nivel').value,
        curso: document.getElementById('curso').value,
        asignatura: document.getElementById('asignatura').value,
        situacion: document.getElementById('situacion').value,
        duracion: document.getElementById('duracion').value
    };
    
    try {
        const response = await generarContenido('/api/emergencia', datos);
        mostrarResultado(response.data.contenido);
    } catch (error) {
        mostrarAlerta('❌ Error al generar la actividad. Por favor, inténtalo de nuevo.', 'error');
    }
}

function handleDescargar() {
    const asignatura = document.getElementById('asignatura').value;
    const titulo = `Actividad_Emergencia_${asignatura}_${new Date().toLocaleDateString()}`;
    descargarDocumento(titulo);
}
