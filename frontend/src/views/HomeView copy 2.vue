<template>
  <div class="page-wrapper">
    <main class="main-content py-4">
      <div class="container">
        <!-- Sección de presentación existente -->
        <div class="row align-items-center justify-content-center mb-5">
          <div class="col-md-6 mb-4 mb-md-0 d-flex justify-content-center">
            <img src="@/assets/img/home/work.png" alt="Presentación"
              class="img-fluid rounded mx-auto d-block image-style me-5">
          </div>
          <div class="col-md-6 text-center">
            <h1 class="mb-3 text-center text-primary fw-bold">Dirección de Monitoreo y Evaluación de la Gestión en Salud
            </h1>
            <p class="mb-3 lead">
              Dirección de Monitoreo y Evaluación de la Gestión en Salud.
            </p>

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
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="pi pi-sitemap fs-3 text-primary mb-2"></i>
                    <h6 class="fw-bold">Arquitectura</h6>
                    <p class="small text-muted mb-0">Diseño del sistema completo</p>
                  </div>
                </div>

                <!-- Módulo de Autenticación -->
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="pi pi-lock fs-3 text-warning mb-2"></i>
                    <h6 class="fw-bold">Autenticación</h6>
                    <p class="small text-muted mb-0">Gestión de usuarios y accesos</p>
                  </div>
                </div>

                <!-- Módulo de Personal -->
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="pi pi-users fs-3 text-purple mb-2"></i>
                    <h6 class="fw-bold">Personal</h6>
                    <p class="small text-muted mb-0">Gestión del equipo</p>
                  </div>
                </div>

                <!-- Módulo de Informática -->
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="pi pi-desktop fs-3 text-success mb-2"></i>
                    <h6 class="fw-bold">Informática</h6>
                    <p class="small text-muted mb-0">Control de equipos</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="access-buttons d-flex flex-column align-items-center">
              <button v-if="isAuthenticated" @click="goToDashboard" class="btn btn-primary btn-lg mb-3">
                <i class="bi bi-box-arrow-in-right me-2"></i>Ingresar al Sistema
              </button>
              <router-link v-else to="/login" class="btn btn-primary btn-lg mb-3">
                <i class="bi bi-box-arrow-in-right me-2"></i>Ingresar al Sistema
              </router-link>

              <!-- Botón para ver el roadmap -->
              <button @click="scrollToRoadmap" class="btn btn-outline-primary btn-sm">
                <i class="fas fa-arrow-down me-2"></i>Ver Roadmap del Proyecto
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="container-fluid">
        <footer class="footer-float">
          <div class="quotes-container">
            <div class="quotes-slider">
              <div class="quote" :class="{ active: currentQuoteIndex === 0 }">
                <div class="quote-content">
                  <div class="quote-icon">“</div>
                  <p class="quote-text">Si lo puedes imaginar, lo puedes programar</p>
                  <div class="quote-author">
                    <div class="author-line"></div>
                    <span>Alan Kay</span>
                  </div>
                </div>
              </div>
              <div class="quote" :class="{ active: currentQuoteIndex === 1 }">
                <div class="quote-content">
                  <div class="quote-icon">“</div>
                  <p class="quote-text">Camina hacia el futuro, abriendo nuevas puertas y probando cosas nuevas...</p>
                  <div class="quote-author">
                    <div class="author-line"></div>
                    <span>Walt Disney</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="footer-info">
            <div class="copyright">
              &copy; {{ currentYear }} - Desarrollado por el área de TI de la DGOS
            </div>
            <div class="technologies">
              Tecnologías:
              <span class="tech-tag"><i class="fab fa-python"></i> Python</span>
              <span class="tech-tag"><i class="fab fa-python"></i> Django</span>
              <span class="tech-tag"><i class="fas fa-layer-group"></i> REST API</span>
              <span class="tech-tag"><i class="fab fa-js"></i> Vue.js</span>
              <span class="tech-tag"><i class="fas fa-Informática"></i> SQL Server</span>
            </div>
          </div>
        </footer>
      </div>
      <div class="container py-4">
        <!-- Nueva sección del Roadmap (con ID para el scroll) -->
        <div id="roadmap-section" class="roadmap-section mt-5">
          <div class="roadmap-header p-4 text-center mb-4">
            <h1><i class="fas fa-map-marked-alt me-2"></i>Roadmap del Proyecto</h1>
            <p class="lead mb-0">Planificación y módulos a implementar</p>
          </div>

          <div class="row mb-4">
            <div class="col-md-6">
              <div class="card h-100">
                <div class="card-body">
                  <h5 class="card-title"><i class="fa fa-info-circle me-2"></i>Resumen del Proyecto</h5>
                  <p class="card-text">Este proyecto tiene como objetivo desarrollar una plataforma integral para el
                    Monitoreo y Evaluación de la Gestión en Salud con múltiples módulos que se implementarán en fases
                    sucesivas.</p>
                  <div class="progress-container">
                    <label>Progreso general del proyecto:</label>
                    <div class="progress">
                      <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
                        style="width: 75%;" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100">75%</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card h-100">
                <div class="card-body">
                  <h5 class="card-title"><i class="fa fa-filter me-2"></i>Filtrar Módulos</h5>
                  <div class="filter-container">
                    <!-- Reemplaza esta sección -->
                    <div class="btn-group btn-group-sm" role="group">
                      <button type="button" class="btn btn-outline-primary filter-btn active"
                        data-filter="all">Todos</button>
                      <button type="button" class="btn btn-outline-primary filter-btn"
                        data-filter="POI">Planificación</button>
                      <button type="button" class="btn btn-outline-success filter-btn" data-filter="Informática">Base de
                        Datos</button>
                      <button type="button" class="btn btn-outline-info filter-btn"
                        data-filter="Frontend">Interfaz</button>
                      <button type="button" class="btn btn-outline-dark filter-btn"
                        data-filter="Backend">Servidor</button>
                      <button type="button" class="btn btn-outline-warning filter-btn"
                        data-filter="security">Seguridad</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="timeline">
            <!-- Fases -->
            <div v-for="(phase, index) in phases" :key="phase.id"
              :class="['phase', index % 2 === 0 ? 'left' : 'right', phase.isCurrent ? 'current-phase' : '']"
              :data-phase="phase.id">
              <div class="phase-content">
                <div class="phase-date"><i class="fa fa-calendar-alt"></i> {{ phase.date }}</div>
                <h3 class="phase-title">{{ phase.title }}</h3>
                <p>{{ phase.description }}</p>
                <div>
                  <span v-for="module in phase.modules" :key="module.name"
                    :class="['badge', 'module-badge', getBadgeClass(module.type)]" :data-type="module.type">
                    {{ module.name }}
                  </span>
                </div>
                <div class="mt-2">
                  <span :class="['badge', getStatusClass(phase.status)]">
                    {{ getStatusText(phase.status) }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="row mt-4">
            <div class="col-md-12">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title"><i class="fa fa-tasks me-2"></i>Detalle de Módulos</h5>
                  <div class="table-responsive">
                    <!-- Modifica la tabla para incluir entregables -->
                    <table class="table table-hover">
                      <thead>
                        <tr>
                          <th>Módulo</th>
                          <th>Tipo</th>
                          <th>Fase</th>
                          <th>Estado</th>
                          <th>Descripción</th>
                          <th>Entregables</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="module in allModules" :key="module.name" :data-type="module.type">
                          <td>{{ module.name }}</td>
                          <td><span :class="['badge', getBadgeClass(module.type)]">{{ getTypeText(module.type) }}</span>
                          </td>
                          <td>{{ module.phase }}</td>
                          <td><span :class="['badge', getStatusClass(module.status)]">{{ getStatusText(module.status)
                              }}</span></td>
                          <td>{{ module.description }}</td>
                          <td>
                            <ul class="list-unstyled mb-0">
                              <li v-for="(deliverable, index) in module.deliverables" :key="index" class="small">
                                <i class="bi bi-check-circle-fill text-success me-1"></i> {{ deliverable }}
                              </li>
                            </ul>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <footer class="footer">
      <div class="quotes-container">
        <div id="quoteCarousel" class="quotes-slider">
          <div class="quote active">
            <div class="quote-content">
              <div class="quote-icon">“</div>
              <p class="quote-text">Si lo puedes imaginar, lo puedes programar</p>
              <div class="quote-author">
                <div class="author-line"></div>
                <span>Alan Kay</span>
              </div>
            </div>
          </div>
          <div class="quote">
            <div class="quote-content">
              <div class="quote-icon">“</div>
              <p class="quote-text">Camina hacia el futuro, abriendo nuevas puertas y probando cosas nuevas...</p>
              <div class="quote-author">
                <div class="author-line"></div>
                <span>Walt Disney</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-info">
        <div class="copyright">
          &copy; {{ currentYear }} - Desarrollado por el área de TI de la DGOS
        </div>
        <div class="technologies">
          Tecnologías:
          <span class="tech-tag"><i class="fab fa-python"></i> Python</span>
          <span class="tech-tag"><i class="fab fa-python"></i> Django</span>
          <span class="tech-tag"><i class="fas fa-layer-group"></i> REST API</span>
          <span class="tech-tag"><i class="fab fa-js"></i> Vue.js</span>
          <span class="tech-tag"><i class="fas fa-Informática"></i> SQL Server</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = computed(() => localStorage.getItem('auth_token'));
const currentQuoteIndex = ref(0);
let quoteInterval = null;
let lastScrollPosition = 0;

const goToDashboard = () => {
  router.push('/dashboard');
};

const currentYear = ref(new Date().getFullYear());

// Función para hacer scroll al roadmap
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
  if (!floatingFooter) return;

  // No ocultar en móvil (ancho menor a 768px)
  if (window.innerWidth < 768) return;

  const currentScrollPosition = window.scrollY;

  if (currentScrollPosition > lastScrollPosition) {
    // Scroll hacia abajo - ocultar
    floatingFooter.style.transform = 'translateY(100%)';
  } else {
    // Scroll hacia arriba - mostrar
    floatingFooter.style.transform = 'translateY(0)';
  }

  lastScrollPosition = currentScrollPosition;
};
onMounted(() => {
  startQuoteRotation();
  window.addEventListener('scroll', handleScroll);

  const quotes = document.querySelectorAll('.quote');
  let currentIndex = 0;
  setInterval(() => {
    quotes[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % quotes.length;
    quotes[currentIndex].classList.add('active');
  }, 5000);

  // Filtrado de módulos
  const filterButtons = document.querySelectorAll('.filter-btn');
  const moduleBadges = document.querySelectorAll('.module-badge');
  const moduleRows = document.querySelectorAll('tbody tr');

  filterButtons.forEach(button => {
    button.addEventListener('click', function () {
      filterButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');

      const filter = this.getAttribute('data-filter');

      moduleBadges.forEach(badge => {
        if (filter === 'all' || badge.getAttribute('data-type') === filter) {
          badge.style.display = 'inline-block';
        } else {
          badge.style.display = 'none';
        }
      });

      moduleRows.forEach(row => {
        if (filter === 'all' || row.getAttribute('data-type') === filter) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    });
  });
  // Control del footer flotante
  let lastScrollPosition = 0;
  const floatingFooter = document.querySelector('.footer-float');

  window.addEventListener('scroll', function () {
    const currentScrollPosition = window.scrollY;

    if (currentScrollPosition > lastScrollPosition) {
      // Scroll hacia abajo
      floatingFooter.style.transform = 'translateY(100%)';
    } else {
      // Scroll hacia arriba
      floatingFooter.style.transform = 'translateY(0)';
    }

    lastScrollPosition = currentScrollPosition;
  });
  // Mostrar detalles al hacer clic en una fase
  const phases = document.querySelectorAll('.phase');
  phases.forEach(phase => {
    phase.addEventListener('click', function () {
      const phaseNumber = this.getAttribute('data-phase');
      alert(`Mostrar detalles de la Fase ${phaseNumber}`);
    });
  });

  // Animación de progreso
  const progressBar = document.querySelector('.progress-bar');
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
});
onUnmounted(() => {
  clearInterval(quoteInterval);
  window.removeEventListener('scroll', handleScroll);
});

// Datos de las fases mejoradas
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

// Funciones de ayuda mejoradas
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
/* Reset básico */
:root {
  --primary-color: #0b4a7a;
  --secondary-color: #f8f9fc;
  --success-color: #1cc88a;
  --info-color: #36b9cc;
  --warning-color: #f6c23e;
  --danger-color: #e74a3b;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', 'Roboto', sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8f9fa;
}

/* Estructura principal */
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header */
.header {
  background: linear-gradient(to right, var(--primary-color), #083758);
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  height: 50px;
  width: auto;
}

/* Contenido principal */
.main-content {
  flex: 1;
  /* Hace que el contenido principal ocupe todo el espacio disponible */
  padding-bottom: 2rem;
  /* Espacio antes del footer */
}

.container {
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
}

/* Estilos para la imagen */
.image-style {
  border: none !important;
  box-shadow: none !important;
  filter: drop-shadow(0 12px 20px rgba(0, 0, 0, 0.25));
  transition: all 0.3s ease;
  max-width: 90%;
  margin: 0 auto;
  transform: translateY(-3px);
}

.image-style:hover {
  filter: drop-shadow(0 12px 20px rgba(0, 0, 0, 0.25));
  transform: translateY(-3px);
}

/* Botones */
.access-buttons {
  margin-top: 2rem;
}

.btn-primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  padding: 0.75rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-primary:hover {
  background-color: #083758;
  border-color: #083758;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-outline-primary {
  border-color: var(--primary-color);
  color: var(--primary-color);
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background-color: var(--primary-color);
  color: white;
}

.access-buttons .btn {
  width: 100%;
  max-width: 250px;
}

/* Roadmap styles */
.roadmap-section {
  margin-top: 3rem;
  padding: 2rem;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.1);
}

.roadmap-header {
  background: linear-gradient(135deg, var(--primary-color), #083758);
  color: white;
  border-radius: 10px;
  margin-bottom: 30px;
}

.timeline {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
}

.timeline::after {
  content: '';
  position: absolute;
  width: 6px;
  background-color: var(--primary-color);
  top: 0;
  bottom: 0;
  left: 50%;
  margin-left: -3px;
  border-radius: 10px;
}

.phase {
  padding: 10px 40px;
  position: relative;
  background-color: inherit;
  width: 50%;
  animation: fadeIn 0.5s ease forwards;
  opacity: 0;
}

.phase:nth-child(1) {
  animation-delay: 0.1s;
}

.phase:nth-child(2) {
  animation-delay: 0.3s;
}

.phase:nth-child(3) {
  animation-delay: 0.5s;
}

.phase:nth-child(4) {
  animation-delay: 0.7s;
}

.phase:nth-child(5) {
  animation-delay: 0.9s;
}

.phase::after {
  content: '';
  position: absolute;
  width: 25px;
  height: 25px;
  right: -17px;
  background-color: white;
  border: 4px solid var(--primary-color);
  top: 15px;
  border-radius: 50%;
  z-index: 1;
}

.left {
  left: 0;
}

.right {
  left: 50%;
}

.left::before {
  content: " ";
  height: 0;
  position: absolute;
  top: 22px;
  width: 0;
  z-index: 1;
  right: 30px;
  border: medium solid white;
  border-width: 10px 0 10px 10px;
  border-color: transparent transparent transparent white;
}

.right::before {
  content: " ";
  height: 0;
  position: absolute;
  top: 22px;
  width: 0;
  z-index: 1;
  left: 30px;
  border: medium solid white;
  border-width: 10px 10px 10px 0;
  border-color: transparent white transparent transparent;
}

.right::after {
  left: -16px;
}

.phase-content {
  padding: 20px 30px;
  background-color: white;
  position: relative;
  border-radius: 10px;
  box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
  transition: all 0.3s ease;
}

.phase-content:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 2rem 0 rgba(58, 59, 69, 0.2);
}

.phase-title {
  font-weight: 600;
  margin-bottom: 15px;
  color: var(--primary-color);
}

.phase-date {
  font-weight: 600;
  color: #6c757d;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.phase-date i {
  margin-right: 8px;
}

.module-badge {
  margin-right: 5px;
  margin-bottom: 5px;
  font-size: 0.8rem;
}

.current-phase .phase-content {
  border-left: 5px solid var(--success-color);
}

.current-phase .phase-title {
  color: var(--success-color);
}

.progress-container {
  margin-top: 20px;
}

.filter-container {
  margin-bottom: 30px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Footer */
.footer {
  background-color: #0f172a;
  color: white;
  padding: 1rem 0;
  width: 100%;
  margin-top: auto;
  /* Esto lo empuja hacia abajo */
  position: relative;
  /* Cambiamos de fixed a relative */
}

/* Footer */
.footer-float {
  background-color: #0f172a;
  color: white;
  padding: 1rem 0;
  width: 100%;
  position: fixed;
  bottom: 0;
  left: 0;
  z-index: 1000;
  transition: transform 0.3s ease-in-out;
  border-radius: 20px 20px 0 0;
  box-shadow: 0 -5px 15px rgba(0, 0, 0, 0.1);
  transform: translateY(0);
}

.quotes-slider {
  position: relative;
  min-height: 100px;
}

.quote {
  position: absolute;
  width: 100%;
  opacity: 0;
  transition: opacity 0.5s ease;
  top: 0;
  left: 0;
}

.quote.active {
  opacity: 1;
}

/* Asegurar que el contenido principal no quede oculto detrás del footer */
.main-content {
  padding-bottom: 180px;
  /* Ajusta según la altura de tu footer */
}

.quotes-container {
  width: 90%;
  max-width: 700px;
  margin: 0 auto 1rem;
  padding: 1rem;
  background: linear-gradient(145deg, #1e293b, #0f172a);
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.quotes-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, #3b82f6, #8b5cf6);
}

.quotes-slider {
  position: relative;
  min-height: 80px;
}

.quote {
  position: absolute;
  width: 100%;
  opacity: 0;
  transition: all 0.5s ease;
}

.quote.active {
  opacity: 1;
}

.quote-content {
  padding: 0 1rem;
}

.quote-icon {
  font-size: 3rem;
  color: #3b82f6;
  opacity: 0.2;
  position: absolute;
  top: -1rem;
  left: 0;
  line-height: 1;
  font-family: Georgia, serif;
}

.quote-text {
  font-size: 1.1rem;
  line-height: 1.5;
  color: #f8fafc;
  margin-bottom: 1rem;
  position: relative;
  font-style: italic;
  padding-left: 1rem;
}

.quote-author {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.author-line {
  flex-grow: 1;
  height: 1px;
  background: linear-gradient(to right, rgba(59, 130, 246, 0.5), transparent);
}

.quote-author span {
  color: #94a3b8;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.footer-info {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.copyright {
  color: #94a3b8;
  font-size: 0.9rem;
}

.technologies {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.tech-tag {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

/* Responsive */
@media screen and (max-width: 768px) {
  .timeline::after {
    left: 31px;
  }

  .phase {
    width: 100%;
    padding-left: 70px;
    padding-right: 25px;
  }

  .phase::before {
    left: 60px;
    border: medium solid white;
    border-width: 10px 10px 10px 0;
    border-color: transparent white transparent transparent;
  }

  .left::after,
  .right::after {
    left: 15px;
  }

  .right {
    left: 0%;
  }

  .main-content {
    flex: 1;
    padding: 3rem 0 6rem;
    /* Añade más espacio en la parte inferior */
  }

  .quotes-container {
    padding: 1.2rem;
    min-height: 100px;
  }

  .quote-text {
    font-size: 1rem;
  }

  .quote-icon {
    font-size: 2.5rem;
    top: -0.8rem;
  }

  .footer-info {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .technologies {
    justify-content: center;
  }

  .col-md-6 {
    text-align: center !important;
  }

  .footer-float {
    position: relative;
    /* Cambia de fixed a relative en móvil */
    transform: translateY(0) !important;
    /* Fuerza a que siempre sea visible */
    border-radius: 0;
    /* Opcional: quita el borde redondeado en móvil */
  }

  .main-content {
    padding-bottom: 0;
    /* Elimina el padding extra en móvil */
  }
}
</style>