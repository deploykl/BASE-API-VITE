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
              <h5 class="mb-3 text-center"><i class="bi bi-grid-fill me-2"></i>Módulos Principales</h5>
              <div class="row justify-content-center g-3"> <!-- Centrado y mejor espaciado -->
                <!-- Módulo de Fichas -->
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="bi bi-clipboard-check fs-3 text-success mb-2"></i>
                    <h6 class="fw-bold">Fichas de Verificación</h6>
                    <p class="small text-muted mb-0">Gestión completa de fichas técnicas</p>
                  </div>
                </div>

                <!-- Módulo de Compromisos -->
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="bi bi-microsoft-teams fs-3 text-primary mb-2"></i>
                    <h6 class="fw-bold">Compromisos</h6>
                    <p class="small text-muted mb-0">Seguimiento de acuerdos</p>
                  </div>
                </div>

                <!-- Módulo de Alertas -->
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="bi bi-exclamation-triangle fs-3 text-warning mb-2"></i>
                    <h6 class="fw-bold">Alertas</h6>
                    <p class="small text-muted mb-0">Notificaciones importantes</p>
                  </div>
                </div>

                <!-- Módulo de Enlaces -->
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="bi bi-link-45deg fs-3 text-info mb-2"></i>
                    <h6 class="fw-bold">Enlaces Rápidos</h6>
                    <p class="small text-muted mb-0">Acceso directo a recursos</p>
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
              <span class="tech-tag"><i class="fas fa-database"></i> SQL Server</span>
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
                        style="width: 30%;" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100">30%</div>
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
                    <div class="btn-group btn-group-sm" role="group">
                      <button type="button" class="btn btn-tutline-primary filter-btn active"
                        data-filter="all">Todos</button>
                      <button type="button" class="btn btn-outline-success filter-btn"
                        data-filter="backend">Backend</button>
                      <button type="button" class="btn btn-outline-info filter-btn"
                        data-filter="frontend">Frontend</button>
                      <button type="button" class="btn btn-outline-warning filter-btn" data-filter="database">Base de
                        Datos</button>
                      <button type="button" class="btn btn-outline-danger filter-btn"
                        data-filter="security">Seguridad</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="timeline">
            <!-- Fase 1 -->
            <div class="phase left current-phase" data-phase="1">
              <div class="phase-content">
                <div class="phase-date"><i class="fa fa-calendar-alt"></i> Enero - Marzo 2023</div>
                <h3 class="phase-title">Fase 1: Inicio y Configuración</h3>
                <p>Configuración inicial del proyecto, infraestructura básica y módulos fundamentales.</p>
                <div>
                  <span class="badge bg-primary module-badge" data-type="backend">API Core</span>
                  <span class="badge bg-success module-badge" data-type="database">Modelo de Datos</span>
                  <span class="badge bg-info module-badge" data-type="frontend">Landing Page</span>
                  <span class="badge bg-warning module-badge" data-type="security">Auth Básico</span>
                </div>
                <div class="mt-2">
                  <span class="badge bg-secondary">En progreso</span>
                </div>
              </div>
            </div>

            <!-- Fase 2 -->
            <div class="phase right" data-phase="2">
              <div class="phase-content">
                <div class="phase-date"><i class="fa fa-calendar-alt"></i> Abril - Junio 2023</div>
                <h3 class="phase-title">Fase 2: Desarrollo Base</h3>
                <p>Implementación de funcionalidades centrales y primeros módulos de usuario.</p>
                <div>
                  <span class="badge bg-primary module-badge" data-type="backend">Servicios Core</span>
                  <span class="badge bg-success module-badge" data-type="database">Migraciones</span>
                  <span class="badge bg-info module-badge" data-type="frontend">Dashboard</span>
                  <span class="badge bg-danger module-badge" data-type="security">Roles y Permisos</span>
                </div>
                <div class="mt-2">
                  <span class="badge bg-light text-dark">Próximamente</span>
                </div>
              </div>
            </div>

            <!-- Fase 3 -->
            <div class="phase left" data-phase="3">
              <div class="phase-content">
                <div class="phase-date"><i class="fa fa-calendar-alt"></i> Julio - Septiembre 2023</div>
                <h3 class="phase-title">Fase 3: Funcionalidades Avanzadas</h3>
                <p>Desarrollo de módulos especializados y optimización del sistema.</p>
                <div>
                  <span class="badge bg-primary module-badge" data-type="backend">Microservicios</span>
                  <span class="badge bg-info module-badge" data-type="frontend">Componentes Avanzados</span>
                  <span class="badge bg-warning module-badge" data-type="database">Replicación</span>
                  <span class="badge bg-dark module-badge" data-type="security">Auditoría</span>
                </div>
                <div class="mt-2">
                  <span class="badge bg-light text-dark">Próximamente</span>
                </div>
              </div>
            </div>

            <!-- Fase 4 -->
            <div class="phase right" data-phase="4">
              <div class="phase-content">
                <div class="phase-date"><i class="fa fa-calendar-alt"></i> Octubre - Diciembre 2023</div>
                <h3 class="phase-title">Fase 4: Integración y Pruebas</h3>
                <p>Integración de todos los módulos, pruebas exhaustivas y preparación para lanzamiento.</p>
                <div>
                  <span class="badge bg-primary module-badge" data-type="backend">API Gateway</span>
                  <span class="badge bg-success module-badge" data-type="database">Optimización</span>
                  <span class="badge bg-info module-badge" data-type="frontend">UI/UX Final</span>
                  <span class="badge bg-danger module-badge" data-type="security">Pentesting</span>
                </div>
                <div class="mt-2">
                  <span class="badge bg-light text-dark">Próximamente</span>
                </div>
              </div>
            </div>

            <!-- Fase 5 -->
            <div class="phase left" data-phase="5">
              <div class="phase-content">
                <div class="phase-date"><i class="fa fa-calendar-alt"></i> Enero 2024</div>
                <h3 class="phase-title">Fase 5: Lanzamiento y Mantenimiento</h3>
                <p>Lanzamiento oficial y ciclo de mantenimiento inicial.</p>
                <div>
                  <span class="badge bg-primary module-badge" data-type="backend">Monitorización</span>
                  <span class="badge bg-info module-badge" data-type="frontend">Feedback UI</span>
                  <span class="badge bg-dark module-badge" data-type="security">Parches</span>
                </div>
                <div class="mt-2">
                  <span class="badge bg-light text-dark">Próximamente</span>
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
                    <table class="table table-hover">
                      <thead>
                        <tr>
                          <th>Módulo</th>
                          <th>Tipo</th>
                          <th>Fase</th>
                          <th>Estado</th>
                          <th>Descripción</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr data-type="backend">
                          <td>API Core</td>
                          <td><span class="badge bg-primary">Backend</span></td>
                          <td>1</td>
                          <td><span class="badge bg-success">Completado</span></td>
                          <td>API principal del sistema</td>
                        </tr>
                        <tr data-type="database">
                          <td>Modelo de Datos</td>
                          <td><span class="badge bg-success">Base de Datos</span></td>
                          <td>1</td>
                          <td><span class="badge bg-warning">En progreso</span></td>
                          <td>Diseño e implementación inicial de la base de datos</td>
                        </tr>
                        <tr data-type="frontend">
                          <td>Landing Page</td>
                          <td><span class="badge bg-info">Frontend</span></td>
                          <td>1</td>
                          <td><span class="badge bg-success">Completado</span></td>
                          <td>Página de presentación del producto</td>
                        </tr>
                        <tr data-type="security">
                          <td>Auth Básico</td>
                          <td><span class="badge bg-danger">Seguridad</span></td>
                          <td>1</td>
                          <td><span class="badge bg-success">Completado</span></td>
                          <td>Sistema básico de autenticación</td>
                        </tr>
                        <tr data-type="backend">
                          <td>Servicios Core</td>
                          <td><span class="badge bg-primary">Backend</span></td>
                          <td>2</td>
                          <td><span class="badge bg-secondary">Pendiente</span></td>
                          <td>Servicios principales de negocio</td>
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
          <span class="tech-tag"><i class="fas fa-database"></i> SQL Server</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted  } from 'vue';
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

window.addEventListener('scroll', function() {
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
  padding-bottom: 180px; /* Ajusta según la altura de tu footer */
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
    position: relative; /* Cambia de fixed a relative en móvil */
    transform: translateY(0) !important; /* Fuerza a que siempre sea visible */
    border-radius: 0; /* Opcional: quita el borde redondeado en móvil */
  }

  .main-content {
    padding-bottom: 0; /* Elimina el padding extra en móvil */
  }
}
</style>