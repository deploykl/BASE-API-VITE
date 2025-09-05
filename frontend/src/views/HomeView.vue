<template>
  <div class="modern-container">
    <!-- Barra de navegación corregida -->
    <nav class="navbar navbar-expand-lg navbar-modern fixed-top">
      <div class="container">
      <!-- En la barra de navegación -->
<router-link to="/" class="navbar-brand navbar-brand-modern">
  <img src="/src/assets/img/logo2.png" alt="Logo HGA" class="navbar-logo me-2">
  DGOS
</router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent"
          aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <button class="nav-link" href="#" @click="scrollToSection('modules')">Módulos</button>
            </li>
            <li class="nav-item">
              <button class="nav-link" href="#" @click="scrollToSection('benefits')">Beneficios</button>
            </li>
            <li class="nav-item">
              <button class="nav-link" href="#" @click="scrollToSection('features')">Características</button>
            </li>
            <li class="nav-item">
              <button class="nav-link" href="#" @click="scrollToSection('about')">Nosotros</button>
            </li>
            <li class="nav-item">
              <button class="nav-link" href="#" @click="scrollToSection('contact')">Contacto</button>
            </li>
          </ul>

          <div class="d-flex">
            <button v-if="isAuthenticated" @click="goToDashboard" class="btn btn-outline-primary btn-sm me-2">
              Admin
            </button>
            <router-link v-else to="/login" class="btn btn-primary btn-sm">
              Iniciar Sesión
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Espacio para el navbar fijo -->
    <div class="navbar-spacer"></div>

    <!-- Contenido principal -->
    <div class="main-content">
      <!-- Header con logo y título -->
      <header class="header-section text-center">

        <h1 class="display-5 fw-bold text-primary">HERRAMIENTAS DE GESTIÓN ADMINISTRATIVA - DGOS</h1>
        <p class="text-muted mb-4">DGOS - DIMON - DIEM</p>
      </header>

      <!-- Alert de novedad -->
      <div class="alert-modern d-flex align-items-center mb-5" role="alert">
        <div class="alert-icon-container me-3">
          <i class="bi bi-megaphone-fill"></i>
        </div>
        <small>
          <strong>Novedad:</strong> Lanzamiento de la Versión (v2.0) nuevos modulos : (Personal, Tableros)
        </small>
      </div>

      <!-- Módulos principales -->
      <section id="modules" class="modules-section mb-5">
        <h2 class="section-title text-center mb-4">
          <span class="title-decoration"></span>
          <i class="pi pi-th-large me-2"></i>Módulos Principales
          <span class="title-decoration"></span>
        </h2>

        <div class="row justify-content-center g-4">
          <div v-for="module in modules" :key="module.id" class="col-10 col-sm-6 col-md-4 col-lg-3 mod-perso">
            <div class="module-card-modern p-4 rounded-4 text-center h-100 position-relative"
              :class="{ 'module-enabled': module.enabled, 'module-disabled': !module.enabled }"
              @click="module.enabled ? redirectToModule(module.path) : null">

              <!-- Badge para módulos deshabilitados -->
              <div v-if="!module.enabled"
                class="position-absolute top-0 start-50 translate-middle px-3 py-1 badge bg-warning coming-soon-badge">
                Próximamente
              </div>

              <div class="module-icon-container-modern mb-3" :style="{ '--icon-color': module.color }">
                <i :class="module.icon" class="module-icon-modern"></i>
              </div>
              <h6 class="fw-bold mb-2">{{ module.title }}</h6>
              <p class="small text-muted mb-0">{{ module.description }}</p>
            </div>
          </div>
        </div>
      </section>
      <!-- Sección de beneficios -->
      <section id="benefits" class="benefits-section mb-5">
        <h2 class="section-title text-center mb-4">
          <span class="title-decoration"></span>
          <i class="bi bi-award me-2"></i>Beneficios Principales
          <span class="title-decoration"></span>
        </h2>

        <div class="row justify-content-center g-4">
          <div class="col-md-6 col-lg-3">
            <div class="benefit-card text-center p-4 rounded-4 h-100">
              <div class="benefit-icon mb-3">
                <i class="bi bi-graph-up-arrow"></i>
              </div>
              <h5>Eficiencia Mejorada</h5>
              <p class="text-muted">Automatiza procesos administrativos y reduce tiempos de ejecución.</p>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="benefit-card text-center p-4 rounded-4 h-100">
              <div class="benefit-icon mb-3">
                <i class="bi bi-shield-check"></i>
              </div>
              <h5>Seguridad de Datos</h5>
              <p class="text-muted">Protección avanzada para toda la información institucional.</p>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="benefit-card text-center p-4 rounded-4 h-100">
              <div class="benefit-icon mb-3">
                <i class="bi bi-lightning-charge"></i>
              </div>
              <h5>Rapidez</h5>
              <p class="text-muted">Acceso rápido a la información y reportes en tiempo real.</p>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="benefit-card text-center p-4 rounded-4 h-100">
              <div class="benefit-icon mb-3">
                <i class="bi bi-bar-chart"></i>
              </div>
              <h5>Toma de Decisiones</h5>
              <p class="text-muted">Dashboards intuitivos para una mejor visualización de datos.</p>
            </div>
          </div>
        </div>
      </section>
      <!-- Sección de características -->
      <section id="features" class="features-section mb-5">
        <h2 class="section-title text-center mb-4">
          <span class="title-decoration"></span>
          <i class="bi bi-stars me-2"></i>Características Destacadas
          <span class="title-decoration"></span>
        </h2>

        <div class="row align-items-center">
          <div class="col-lg-6">
            <div class="feature-item d-flex mb-4">
              <div class="feature-icon me-4">
                <i class="bi bi-check2-circle"></i>
              </div>
              <div>
                <h5>Interfaz Intuitiva</h5>
                <p class="text-muted mb-0">Diseño moderno y fácil de usar que requiere mínima capacitación.</p>
              </div>
            </div>

            <div class="feature-item d-flex mb-4">
              <div class="feature-icon me-4">
                <i class="bi bi-check2-circle"></i>
              </div>
              <div>
                <h5>Integración Total</h5>
                <p class="text-muted mb-0">Todos los módulos conectados entre sí para un flujo de trabajo unificado.</p>
              </div>
            </div>

            <div class="feature-item d-flex mb-4">
              <div class="feature-icon me-4">
                <i class="bi bi-check2-circle"></i>
              </div>
              <div>
                <h5>Acceso Móvil</h5>
                <p class="text-muted mb-0">Disponible desde cualquier dispositivo con conexión a internet.</p>
              </div>
            </div>
          </div>

          <div class="col-lg-6 text-center">
            <div class="feature-visual p-4 rounded-4">
              <i class="bi bi-laptop"></i>
              <div class="mt-3">
                <h5>Plataforma Unificada</h5>
                <p class="text-muted">Todas las herramientas en un solo lugar</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Sección Nosotros -->
      <section id="about" class="about-section mb-4">
        <h2 class="section-title text-center mb-4">
          <span class="title-decoration"></span>
          <i class="bi bi-people me-2"></i>Nosotros
          <span class="title-decoration"></span>
        </h2>

        <div class="row justify-content-center">
          <div class="col-lg-8 text-center">
            <p class="lead">
              Somos el área de Tecnologías de la Información de la DGOS, dedicados a desarrollar
              soluciones innovadoras que mejoren la gestión administrativa y optimicen los procesos
              institucionales.
            </p>
          </div>
        </div>
      </section>

      <!-- Sección Contacto -->
      <section id="contact" class="contact-section mb-5">
        <h2 class="section-title text-center mb-4">
          <span class="title-decoration"></span>
          <i class="bi bi-envelope me-2"></i>Contacto
          <span class="title-decoration"></span>
        </h2>

        <div class="row justify-content-center mod-perso">
          <div class="col-lg-6">
            <div class="contact-card p-4 rounded-4 text-center">
              <i class="bi bi-headset contact-icon mb-3"></i>
              <h5>Soporte Técnico</h5>
              <p class="text-muted">Estamos aquí para ayudarte con cualquier consulta o problema técnico.</p>
              <p class="mb-0">
                <i class="bi bi-envelope me-2"></i>
                <a href="mailto:soporte@dgos.gob.pe">dgos.staff@minsa.gob.pe</a>
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="footer-modern py-4 bg-light mod-perso">
        <div class="container">
          <div class="row align-items-center">

            <!-- Texto centrado en móviles, alineado a la izquierda en pantallas grandes -->
            <div class="col-lg-5 text-center text-lg-start mb-lg-0">
              <p class="mb-0">
                <span class="text-muted">&copy; {{ currentYear }} - Desarrollado por</span>
                <span class="fw-medium text-primary ms-1">área de TI de la DGOS</span>
              </p>
            </div>

            <!-- Tecnologías: centrado en móviles, alineado a la derecha en pantallas grandes -->
            <div class="col-lg-7 text-center text-lg-end">
              <div
                class="d-inline-flex flex-wrap justify-content-center justify-content-lg-end align-items-center gap-2">
                <small class="text-muted">Tecnologías:</small>
                <span v-for="(tech, index) in technologies" :key="index"
                  class="tech-badge-modern d-flex align-items-center">
                  <img :src="tech.icon" :alt="tech.name" class="tech-icon me-1" />
                  {{ tech.name }}
                </span>
              </div>
            </div>

          </div>
        </div>
      </footer>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = computed(() => {
  const token = localStorage.getItem('auth_token');
  return !!token;
});

const currentYear = ref(new Date().getFullYear());

// Array de tecnologías para el footer (sin imports para evitar errores)
const technologies = ref([
  { name: 'Python', icon: '/src/assets/svg/python.svg' },
  { name: 'Vuejs3', icon: '/src/assets/svg/vuejs.svg' },
  { name: 'Sql Server', icon: '/src/assets/svg/sql_server.svg' },
  { name: 'Vite', icon: '/src/assets/svg/vite.svg' },
  { name: 'Pinia', icon: '/src/assets/svg/pinia.svg' },
  { name: 'WebSocket', icon: '/src/assets/svg/websocket.svg' }
]);

// Array de módulos para renderizar dinámicamente
const modules = ref([
  {
    id: 1,
    title: 'Personal',
    description: 'Gestión de usuarios',
    icon: 'pi pi-users',
    color: '#6f42c1',
    path: '/dgos/personal',
    enabled: true
  },
  {
    id: 2,
    title: 'Tableros',
    description: 'Gestión de Dashboards',
    icon: 'pi pi-chart-line',
    color: '#007bff',
    path: '/dimon/tablero',
    enabled: true
  },
  {
    id: 3,
    title: 'POI',
    description: 'Planeamiento Operativo',
    icon: 'pi pi-lock',
    color: '#ffc107',
    path: '/dashboard',
    enabled: false
  },
  {
    id: 4,
    title: 'Informática',
    description: 'Control de equipos',
    icon: 'pi pi-desktop',
    color: '#28a745',
    path: '/dashboard',
    enabled: false
  },
  {
    id: 5,
    title: 'Pool vehicular',
    description: 'Control de salida',
    icon: 'pi pi-car',
    color: '#0B5ED7',
    path: '/dashboard',
    enabled: false
  },
  {
    id: 6,
    title: 'Patrimonio',
    description: 'Control de bienes',
    icon: 'pi pi-box',
    color: '#fd7e14',
    path: '/dashboard',
    enabled: false
  },
  {
    id: 7,
    title: 'Gasto',
    description: 'Control de equipos',
    icon: 'pi pi-chart-line',
    color: '#ffb300',
    path: '/dashboard',
    enabled: false
  },
  {
    id: 8,
    title: 'Reuniones',
    description: 'Control de reuniones',
    icon: 'pi pi-desktop',
    color: '#28a745',
    path: '/dashboard',
    enabled: false
  }
]);

// Función para scroll suave a secciones
const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};

// Función para redirigir a un módulo específico
const redirectToModule = (path) => {
  if (isAuthenticated.value) {
    router.push(path);
  } else {
    localStorage.setItem('redirectAfterLogin', path);
    router.push('/login');
  }
};

const goToDashboard = () => {
  router.push('/dashboard');
};

// Efecto de aparición progresiva para las tarjetas
onMounted(() => {
  const cards = document.querySelectorAll('.module-card-modern');
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`;
  });
});
</script>

<style scoped>
.modern-container {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  padding: 0;
  backdrop-filter: blur(1px);
}

/* Espaciador para navbar fijo */
.navbar-spacer {
  height: 76px;
  /* Ajusta según la altura de tu navbar */
}

/* Navbar styles corregidos */
.navbar-modern {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  padding: 0.5rem 0;
}

.navbar-brand-modern {
  font-weight: 700;
  color: var(--bs-primary) !important;
  font-size: 1.5rem;
}

.navbar-brand-modern i {
  color: var(--bs-primary);
}

.navbar-modern .nav-link {
  font-weight: 500;
  color: #495057 !important;
  transition: all 0.3s ease;
  position: relative;
}

.navbar-modern .nav-link:hover {
  color: var(--bs-primary) !important;
}

.navbar-modern .nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: var(--bs-primary);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.navbar-modern .nav-link:hover::after {
  width: 80%;
}

.main-content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.logo-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: linear-gradient(135deg, var(--bs-primary) 0%, #0d6efd 100%);
  box-shadow: 0 10px 20px rgba(13, 110, 253, 0.2);
}

.logo-icon {
  font-size: 2.5rem;
  color: white;
}

/* Alert moderno */
.alert-modern {
  font-size: 0.9rem;
  border: none;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  padding: 1rem 1.5rem;
  align-items: center;
  display: flex;
  margin: 0 auto 30px auto;
  /* Centrado horizontal con margen automático */
  width: 60%;
  /* Ancho definido para que el margen automático funcione */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  opacity: 0.7;
  text-align: center;
}

.alert-modern:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 36px rgba(31, 38, 135, 0.15);
}

.mod-perso {
  transition: transform 0.3s ease,
    box-shadow 0.3s ease;

}

.mod-perso:hover {
  transform: translateY(-5px);
}

.alert-icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bs-primary);
  color: white;
}

/* Section title */
.section-title {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.title-decoration {
  width: 40px;
  height: 3px;
  background: linear-gradient(to right, transparent, var(--bs-primary), transparent);
  margin: 0 15px;
}

/* Benefit cards */
.benefit-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  transition: all 0.3s ease;
}

.benefit-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 36px rgba(31, 38, 135, 0.15);
}

.benefit-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: linear-gradient(135deg, var(--bs-primary) 0%, #0a58ca 100%);
  color: white;
  font-size: 1.5rem;
}

/* Feature section */
.feature-item {
  padding: 1rem;
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: rgba(13, 110, 253, 0.1);
  color: var(--bs-primary);
  font-size: 1.2rem;
  flex-shrink: 0;
}

.feature-visual {
  background: linear-gradient(135deg, rgba(13, 110, 253, 0.1) 0%, rgba(13, 110, 253, 0.05) 100%);
  border: 1px solid rgba(13, 110, 253, 0.1);
}

.feature-visual i {
  font-size: 4rem;
  color: var(--bs-primary);
}

/* About section */
.about-section {
  padding: 2rem 0;
}

.contact-section {
  padding: 2rem 0;
}

.contact-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
}

.contact-icon {
  font-size: 3rem;
  color: var(--bs-primary);
}

/* Tarjetas de módulos modernas */
.module-card-modern {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

}

.module-card-modern:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 36px rgba(31, 38, 135, 0.2);
}

.module-enabled:hover .module-icon-container-modern {
  transform: scale(1.1);
}

.module-disabled {
  opacity: 0.6 !important;
  cursor: not-allowed;
}

.module-disabled:hover {
  transform: none !important;
}

.coming-soon-badge {
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.module-icon-container-modern {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 70px;
  border-radius: 20px;
  background: linear-gradient(135deg, var(--icon-color) 0%, var(--icon-color) 100%);
  color: white;
  margin-bottom: 1.5rem;
  transition: transform 0.3s ease;
}

.module-icon-modern {
  font-size: 2rem;
}

/* Botón moderno */
.btn-modern {
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--bs-primary) 0%, #0a58ca 100%);
  box-shadow: 0 8px 20px rgba(13, 110, 253, 0.3);
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-modern:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 25px rgba(13, 110, 253, 0.4);
}

/* Footer moderno */
.footer-modern {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(1px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;

}


.tech-badge-modern {
  padding: 0.4rem 0.8rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  font-size: 0.75rem;
  color: #2c3e50;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  transition: all 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.tech-badge-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.tech-icon {
  width: 16px;
  height: 16px;
  object-fit: contain;
  margin-right: 6px;
}

/* Animaciones */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .modern-container {
    padding: 0;
  }

  .navbar-spacer {
    height: 66px;
  }

  .header-section h1 {
    font-size: 1.8rem;
  }

  .section-title {
    flex-direction: column;
  }

  .title-decoration {
    margin: 10px 0;
    width: 80px;
  }

  .tech-badge-modern {
    margin-bottom: 0.5rem;
  }

  .navbar-brand-modern {
    font-size: 1.2rem;
  }
}
.navbar-logo {
  height: 32px; /* Ajusta según el tamaño de tu logo */
  width: auto;
  object-fit: contain;
}
</style>