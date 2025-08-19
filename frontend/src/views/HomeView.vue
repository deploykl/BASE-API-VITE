<template>
  <div class="d-flex flex-column min-vh-100">
    <main class="flex-grow-1 py-4">
      <div class="container">
        <!-- Sección de presentación -->
        <div class="row align-items-center justify-content-center mb-5">
          <div class="col-md-6 mb-4 mb-md-0 d-flex justify-content-center">
            <img src="@/assets/img/home/work.png" alt="Presentación"
              class="img-fluid rounded mx-auto d-block me-lg-5 image-style" style="max-width: 100%;">
          </div>
          <div class="col-md-6 text-center">
            <h1 class="mb-3 text-center text-primary fw-bold">Dirección de Monitoreo y Evaluación de la Gestión en Salud</h1>
            <p class="mb-3 lead">Dirección de Monitoreo y Evaluación de la Gestión en Salud.</p>

            <div class="alert alert-info d-flex align-items-center mb-4">
              <i class="bi bi-exclamation-circle-fill me-2 fs-4"></i>
              <div>
                <strong>Novedad:</strong> Lanzamiento de la Versión Demo (v1.0) con módulos esenciales
              </div>
            </div>
            
            <!-- Módulos destacados -->
            <div class="mb-4">
              <h5 class="mb-3 text-center"><i class="pi pi-th-large me-2"></i>Módulos Principales</h5>
              <div class="row justify-content-center g-3">
                <!-- Módulo de Arquitectura -->
                <div class="col-8 col-sm-6 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100">
                    <i class="pi pi-sitemap fs-3 text-primary mb-2"></i>
                    <h6 class="fw-bold">Arquitectura</h6>
                    <p class="small text-muted mb-0">Diseño del sistema completo</p>
                  </div>
                </div>

                <!-- Módulo de Autenticación -->
                <div class="col-8 col-sm-6 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100">
                    <i class="pi pi-lock fs-3 text-warning mb-2"></i>
                    <h6 class="fw-bold">Autenticación</h6>
                    <p class="small text-muted mb-0">Gestión de usuarios y accesos</p>
                  </div>
                </div>

                <!-- Módulo de Personal -->
                <div class="col-8 col-sm-6 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100">
                    <i class="pi pi-users fs-3 text-purple mb-2"></i>
                    <h6 class="fw-bold">Personal</h6>
                    <p class="small text-muted mb-0">Gestión del equipo</p>
                  </div>
                </div>

                <!-- Módulo de Informática -->
                <div class="col-8 col-sm-6 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100">
                    <i class="pi pi-desktop fs-3 text-success mb-2"></i>
                    <h6 class="fw-bold">Informática</h6>
                    <p class="small text-muted mb-0">Control de equipos</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="access-buttons d-flex flex-column align-items-center">
              <button v-if="isAuthenticated" @click="goToDashboard" class="btn btn-primary btn-lg mb-3 px-4">
                <i class="bi bi-box-arrow-in-right me-2"></i>Ingresar al Sistema
              </button>
              <router-link v-else to="/login" class="btn btn-primary btn-lg mb-3 px-4">
                <i class="bi bi-box-arrow-in-right me-2"></i>Ingresar al Sistema
              </router-link>

              <button @click="scrollToRoadmap" class="btn btn-outline-primary btn-sm">
                <i class="fas fa-arrow-down me-2"></i>Ver Roadmap del Proyecto
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Footer flotante -->
      <footer class="footer-float bg-dark text-white py-3 fixed-bottom">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-lg-8 mb-3 mb-lg-0">
              <div class="quote-slider position-relative" style="min-height: 80px;">
                <div class="quote position-absolute w-100" :class="{ 'opacity-100': currentQuoteIndex === 0, 'opacity-0': currentQuoteIndex !== 0 }" style="transition: opacity 0.5s ease;">
                  <div class="d-flex">
                    <span class="fs-1 me-2 text-primary opacity-25">“</span>
                    <div>
                      <p class="mb-1 fst-italic text-white">Si lo puedes imaginar, lo puedes programar</p>
                      <div class="d-flex align-items-center">
                        <div class="flex-grow-1 border-top border-primary opacity-25 me-2"></div>
                        <span class="text-muted small">Alan Kay</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="quote position-absolute w-100" :class="{ 'opacity-100': currentQuoteIndex === 1, 'opacity-0': currentQuoteIndex !== 1 }" style="transition: opacity 0.5s ease;">
                  <div class="d-flex">
                    <span class="fs-1 me-2 text-primary opacity-25">“</span>
                    <div>
                      <p class="mb-1 fst-italic text-white">Camina hacia el futuro, abriendo nuevas puertas y probando cosas nuevas...</p>
                      <div class="d-flex align-items-center">
                        <div class="flex-grow-1 border-top border-primary opacity-25 me-2"></div>
                        <span class="text-muted small">Walt Disney</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="d-flex flex-column flex-md-row justify-content-between align-items-center align-items-lg-end text-center text-lg-start">
                <div class="mb-2 mb-md-0">
                  <small class="text-muted">&copy; {{ currentYear }} - Desarrollado por el área de TI de la DGOS</small>
                </div>
                <div>
                  <small class="text-muted me-2">Tecnologías:</small>
                  <span class="badge bg-secondary bg-opacity-25 me-1 mb-1"><i class="fab fa-python me-1"></i>Python</span>
                  <span class="badge bg-secondary bg-opacity-25 me-1 mb-1"><i class="fab fa-js me-1"></i>Vue.js</span>
                  <span class="badge bg-secondary bg-opacity-25 mb-1"><i class="fas fa-database me-1"></i>SQL Server</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </footer>
      
    
    </main>

    <!-- Footer normal (para móviles) -->
    <footer class="footer bg-dark text-white py-3 d-lg-none">
      <div class="container">
        <div class="text-center mb-3">
          <small class="text-muted">&copy; {{ currentYear }} - Desarrollado por el área de TI de la DGOS</small>
        </div>
        <div class="d-flex flex-wrap justify-content-center gap-2">
          <small class="text-muted me-2">Tecnologías:</small>
          <span class="badge bg-secondary bg-opacity-25 me-1 mb-1"><i class="fab fa-python me-1"></i>Python</span>
          <span class="badge bg-secondary bg-opacity-25 me-1 mb-1"><i class="fab fa-js me-1"></i>Vue.js</span>
          <span class="badge bg-secondary bg-opacity-25 mb-1"><i class="fas fa-database me-1"></i>SQL Server</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = computed(() => localStorage.getItem('auth_token'));
const currentQuoteIndex = ref(0);
const currentYear = ref(new Date().getFullYear());
let quoteInterval = null;
let lastScrollPosition = 0;

const goToDashboard = () => {
  router.push('/dashboard');
};

const scrollToRoadmap = () => {
  const roadmapSection = document.getElementById('roadmap-section');
  if (roadmapSection) {
    roadmapSection.scrollIntoView({ behavior: 'smooth' });
  }
};

const startQuoteRotation = () => {
  quoteInterval = setInterval(() => {
    currentQuoteIndex.value = (currentQuoteIndex.value + 1) % 2;
  }, 5000);
};

const handleScroll = () => {
  const floatingFooter = document.querySelector('.footer-float');
  if (!floatingFooter || window.innerWidth < 992) return;

  const currentScrollPosition = window.scrollY;
  
  if (currentScrollPosition > lastScrollPosition && currentScrollPosition > 100) {
    floatingFooter.style.transform = 'translateY(100%)';
  } else {
    floatingFooter.style.transform = 'translateY(0)';
  }

  lastScrollPosition = currentScrollPosition;
};

onMounted(() => {
  startQuoteRotation();
  window.addEventListener('scroll', handleScroll);

  // Filtrado de módulos
  const filterButtons = document.querySelectorAll('.filter-btn');
  const moduleBadges = document.querySelectorAll('.module-badge');
  const moduleRows = document.querySelectorAll('tbody tr');

  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      filterButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      const filter = this.getAttribute('data-filter');

      moduleBadges.forEach(badge => {
        badge.style.display = (filter === 'all' || badge.getAttribute('data-type') === filter) ? 'inline-block' : 'none';
      });

      moduleRows.forEach(row => {
        row.style.display = (filter === 'all' || row.getAttribute('data-type') === filter) ? '' : 'none';
      });
    });
  });

  // Animación de progreso
  const progressBar = document.querySelector('.progress-bar');
  if (progressBar) {
    let width = 0;
    const targetWidth = parseInt(progressBar.getAttribute('aria-valuenow'));
    const interval = setInterval(() => {
      if (width >= targetWidth) {
        clearInterval(interval);
      } else {
        width++;
        progressBar.style.width = width + '%';
        progressBar.textContent = width + '%';
      }
    }, 30);
  }
});

onUnmounted(() => {
  clearInterval(quoteInterval);
  window.removeEventListener('scroll', handleScroll);
});

// Datos de las fases
const phases = ref([
  {
    id: 1,
    date: 'Agosto - Diciembre 2024',
    title: 'Fase 1: Diseño e Infraestructura',
    description: 'Definición de arquitectura, diseño de base de datos y configuración inicial.',
    modules: [
      { name: 'Arquitectura del Sistema', type: 'POI' },
      { name: 'Modelo de Datos', type: 'Informática' },
      { name: 'Entorno de Desarrollo', type: 'Infraestructura' },
      { name: 'API Core', type: 'Backend' },
    ],
    status: 'in-progress',
    isCurrent: true,
    deliverables: ['Documentación técnica', 'Prototipo de BD', 'Entorno configurado']
  },
  {
    id: 2,
    date: 'Enero - Marzo 2025',
    title: 'Fase 2: Desarrollo de Módulos Básicos',
    description: 'Implementación de funcionalidades centrales y autenticación.',
    modules: [
      { name: 'Sistema de Autenticación', type: 'security' },
      { name: 'Módulo de Usuarios', type: 'Administración' },
      { name: 'CRUD Básico', type: 'Backend' },
      { name: 'Interfaz Administrativa', type: 'Frontend' },
    ],
    status: 'upcoming',
    isCurrent: false,
    deliverables: ['Login funcional', 'Gestión de usuarios', 'Panel admin básico']
  },
  {
    id: 3,
    date: 'Abril - Junio 2025',
    title: 'Fase 3: Módulos Específicos',
    description: 'Desarrollo de módulos funcionales según áreas de negocio.',
    modules: [
      { name: 'Módulo de Personal', type: 'Administración' },
      { name: 'Módulo de Informática', type: 'Informática' },
      { name: 'Módulo de Patrimonio', type: 'Inventario' },
      { name: 'Reportes Básicos', type: 'Business Intelligence' },
    ],
    status: 'upcoming',
    isCurrent: false,
    deliverables: ['Gestión completa de personal', 'Control de equipos', 'Registro de activos']
  },
  {
    id: 4,
    date: 'Julio - Septiembre 2025',
    title: 'Fase 4: Integración y Pruebas',
    description: 'Integración de módulos, pruebas exhaustivas y preparación para producción.',
    modules: [
      { name: 'Integración de Módulos', type: 'POI' },
      { name: 'Pruebas de Carga', type: 'Calidad' },
      { name: 'Seguridad y Auditoría', type: 'security' },
      { name: 'Migración de Datos', type: 'Informática' },
    ],
    status: 'upcoming',
    isCurrent: false,
    deliverables: ['Sistema integrado', 'Reporte de pruebas', 'Plan de migración']
  },
  {
    id: 5,
    date: 'Octubre 2025',
    title: 'Fase 5: Implementación Inicial',
    description: 'Despliegue en ambiente productivo para usuarios clave.',
    modules: [
      { name: 'Despliegue en Producción', type: 'Infraestructura' },
      { name: 'Capacitación Inicial', type: 'Soporte' },
      { name: 'Monitoreo Post-Implementación', type: 'Calidad' },
    ],
    status: 'upcoming',
    isCurrent: false,
    deliverables: ['Sistema en producción', 'Manuales de usuario', 'Plan de soporte']
  },
  {
    id: 6,
    date: 'Noviembre - Diciembre 2025',
    title: 'Fase 6: Consolidación y Mejoras',
    description: 'Ajustes basados en feedback y plan de mejoras continuas.',
    modules: [
      { name: 'Recolección de Feedback', type: 'POI' },
      { name: 'Implementación de Mejoras', type: 'Desarrollo' },
      { name: 'Plan de Roadmap', type: 'Gestión' },
    ],
    status: 'upcoming',
    isCurrent: false,
    deliverables: ['Reporte de ajustes', 'Versión estable', 'Plan de evolución']
  }
]);

// Todos los módulos para la tabla
const allModules = computed(() => {
  return phases.value.flatMap(phase => {
    return phase.modules.map(module => ({
      ...module,
      phase: phase.id,
      phaseTitle: phase.title,
      status: phase.status,
      description: getModuleDescription(module.name, phase.id),
      deliverables: phase.deliverables || []
    }));
  });
});

// Funciones de ayuda
const getBadgeClass = (type) => {
  const classes = {
    POI: 'bg-primary',
    Informática: 'bg-success',
    Frontend: 'bg-info',
    Backend: 'bg-dark',
    security: 'bg-warning',
    Administración: 'bg-purple',
    'Business Intelligence': 'bg-indigo',
    Infraestructura: 'bg-teal',
    Calidad: 'bg-pink',
    Soporte: 'bg-orange',
    Gestión: 'bg-cyan',
    Inventario: 'bg-brown',
    Desarrollo: 'bg-blue'
  };
  return classes[type] || 'bg-secondary';
};

const getTypeText = (type) => {
  const texts = {
    POI: 'Planificación',
    Informática: 'Base de Datos',
    Frontend: 'Interfaz',
    Backend: 'Servidor',
    security: 'Seguridad',
    Administración: 'Admin',
    'Business Intelligence': 'BI',
    Infraestructura: 'Infra',
    Calidad: 'QA',
    Soporte: 'Soporte',
    Gestión: 'Gestión',
    Inventario: 'Inventario',
    Desarrollo: 'Dev'
  };
  return texts[type] || type;
};

const getStatusClass = (status) => {
  const classes = {
    completed: 'bg-success',
    'in-progress': 'bg-warning',
    upcoming: 'bg-light text-dark'
  };
  return classes[status] || 'bg-light text-dark';
};

const getStatusText = (status) => {
  const texts = {
    completed: 'Completado',
    'in-progress': 'En progreso',
    upcoming: 'Próximamente'
  };
  return texts[status] || status;
};

const getModuleDescription = (name, phase) => {
  const descriptions = {
    'Arquitectura del Sistema': 'Diseño de la arquitectura técnica del sistema completo',
    'Modelo de Datos': 'Diseño e implementación inicial de la base de datos',
    'Entorno de Desarrollo': 'Configuración de ambientes de desarrollo y testing',
    'API Core': 'API principal del sistema con endpoints básicos',
    'Sistema de Autenticación': 'Módulo de login, registro y manejo de sesiones',
    'Módulo de Usuarios': 'Gestión de perfiles, roles y permisos',
    'CRUD Básico': 'Operaciones básicas para todos los módulos',
    'Interfaz Administrativa': 'Panel de administración principal',
    'Módulo de Personal': 'Gestión completa del personal de la organización',
    'Módulo de Informática': 'Control de equipos y recursos tecnológicos',
    'Módulo de Patrimonio': 'Registro y seguimiento de activos de la organización',
    'Reportes Básicos': 'Generación de reportes estadísticos básicos',
    'Integración de Módulos': 'Conectar todos los módulos entre sí',
    'Pruebas de Carga': 'Evaluación de performance bajo carga',
    'Seguridad y Auditoría': 'Análisis de vulnerabilidades y registro de actividades',
    'Migración de Datos': 'Transferencia de datos antiguos al nuevo sistema',
    'Despliegue en Producción': 'Implementación en servidores productivos',
    'Capacitación Inicial': 'Entrenamiento a usuarios clave',
    'Monitoreo Post-Implementación': 'Seguimiento a problemas iniciales',
    'Recolección de Feedback': 'Obtención de comentarios de usuarios',
    'Implementación de Mejoras': 'Ajustes basados en feedback',
    'Plan de Roadmap': 'Planificación de futuras versiones'
  };
  
  return descriptions[name] || `Módulo ${name} correspondiente a la fase ${phase}`;
};
</script>

<style>
/* Solo estilos mínimos necesarios que no pueden ser reemplazados por Bootstrap */
.footer-float {
  transition: transform 0.3s ease-in-out;
}

.quote {
  transition: opacity 0.5s ease;
}

/* Asegurar espacio para el footer flotante */
.main-content {
  padding-bottom: 180px;
}

@media (max-width: 991.98px) {
  .footer-float {
    position: relative !important;
    transform: none !important;
  }
  .main-content {
    padding-bottom: 0;
  }
}
* Colores de fondo de Bootstrap equivalentes */
.bg-primary {
  background-color: #0d6efd !important;
}

.bg-success {
  background-color: #198754 !important;
}

.bg-info {
  background-color: #0dcaf0 !important;
}

.bg-dark {
  background-color: #212529 !important;
}

.bg-warning {
  background-color: #ffc107 !important;
}

.bg-purple {
  background-color: #6f42c1 !important;
}

.bg-indigo {
  background-color: #6610f2 !important;
}

.bg-teal {
  background-color: #20c997 !important;
}

.bg-pink {
  background-color: #d63384 !important;
}

.bg-orange {
  background-color: #fd7e14 !important;
}

.bg-cyan {
  background-color: #0dcaf0 !important;
}

.bg-brown {
  background-color: #795548 !important; /* Color café/marrón estándar */
}

.bg-blue {
  background-color: #0d6efd !important; /* Igual que primary en Bootstrap */
}
.image-style {
  border: none !important;
  box-shadow: none !important;
  filter: drop-shadow(0 12px 20px rgba(0, 0, 0, 0.25));
  /* Efecto hover más notable */
  transition: all 0.3s ease;
  max-width: 90%;
  /* Asegura que la imagen no sea demasiado grande */
  margin: 0 auto;
  /* Centrado adicional */
  transform: translateY(-3px);
  /* Efecto de elevación sutil */

}

.image-style:hover {
  filter: drop-shadow(0 12px 20px rgba(0, 0, 0, 0.25));
  /* Efecto hover más notable */
  transform: translateY(-3px);
  /* Efecto de elevación sutil */
}

/* Elimina cualquier sombra preexistente en el contenedor */
.img-fluid.rounded.shadow {
  box-shadow: none !important;
}

</style>