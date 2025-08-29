<template>
  <div class="modern-container">
    <!-- Fondo con gradiente y efecto de partículas -->
    <div class="background-gradient"></div>
    
    <!-- Contenido principal -->
    <div class="main-content">
      <!-- Header con logo y título -->
      <header class="header-section text-center mb-5">
        <div class="logo-container mb-3">
          <i class="bi bi-heart-pulse-fill logo-icon"></i>
        </div>
        <h1 class="display-5 fw-bold text-primary mb-2">DIRECCIÓN GENERAL DE OPERACIONES EN SALUD</h1>
        <p class="text-muted mb-4">DGOS - DIMON - DIEM</p>
      </header>

      <!-- Alert de novedad -->
      <div class="alert alert-primary alert-modern d-flex align-items-center mb-5" role="alert">
        <div class="alert-icon-container me-3">
          <i class="bi bi-megaphone-fill"></i>
        </div>
        <div>
          <strong>Novedad:</strong> Lanzamiento de la Versión Demo (v1.0) con módulos esenciales
        </div>
      </div>

      <!-- Módulos principales -->
      <section class="modules-section mb-5">
        <h2 class="section-title text-center mb-4">
          <span class="title-decoration"></span>
          <i class="pi pi-th-large me-2"></i>Módulos Principales
          <span class="title-decoration"></span>
        </h2>
        
        <div class="row justify-content-center g-4">
          <div v-for="module in modules" :key="module.id" 
               class="col-10 col-sm-6 col-md-4 col-lg-3">
            <div class="module-card-modern p-4 rounded-4 text-center h-100 position-relative"
                 :class="{ 'module-enabled': module.enabled, 'module-disabled': !module.enabled }"
                 @click="module.enabled ? redirectToModule(module.path) : null">
              
              <!-- Badge para módulos deshabilitados -->
              <div v-if="!module.enabled" class="position-absolute top-0 start-50 translate-middle px-3 py-1 badge bg-warning coming-soon-badge">
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

      <!-- Botón de acceso -->
      <div class="access-section text-center mb-5">
        <button v-if="isAuthenticated" @click="goToDashboard" class="btn btn-primary btn-modern px-5 py-3">
          <i class="bi bi-box-arrow-in-right me-2"></i>Ingresar al Sistema
        </button>
        <router-link v-else to="/login" class="btn btn-primary btn-modern px-5 py-3">
          <i class="bi bi-box-arrow-in-right me-2"></i>Ingresar al Sistema
        </router-link>
      </div>

      <!-- Footer -->
      <footer class="footer-modern text-center py-4 mt-5">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-lg-6 mb-3 mb-lg-0">
              <p class="mb-0">
                <span class="text-muted">&copy; {{ currentYear }} - Desarrollado por</span>
                <span class="fw-medium text-primary ms-1">área de TI de la DGOS</span>
              </p>
            </div>
            <div class="col-lg-6">
              <div class="d-flex flex-wrap justify-content-center justify-content-lg-end align-items-center gap-2">
                <small class="text-muted me-2">Tecnologías:</small>
                <span v-for="(tech, index) in technologies" :key="index" class="tech-badge-modern">
                  <img :src="tech.icon" :alt="tech.name" class="tech-icon" />
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

// Array de tecnologías para el footer
const technologies = ref([
  { name: 'Python', icon: '@/assets/svg/python.svg' },
  { name: 'Vuejs3', icon: '@/assets/svg/vuejs.svg' },
  { name: 'Sql Server', icon: '@/assets/svg/sql_server.svg' },
  { name: 'Vite', icon: '@/assets/svg/vite.svg' },
  { name: 'Pinia', icon: '@/assets/svg/pinia.svg' },
  { name: 'WebSocket', icon: '@/assets/svg/websocket.svg' }
]);

// Array de módulos para renderizar dinámicamente
const modules = ref([
  {
    id: 1,
    title: 'Personal',
    description: 'Gestión de usuarios',
    icon: 'pi pi-users',
    color: '#6f42c1',
    path: '/user/create',
    enabled: true
  },
  {
    id: 2,
    title: 'Tableros',
    description: 'Gestión de Dashboards',
    icon: 'pi pi-chart-line',
    color: '#007bff',
    path: '/dashboard',
    enabled: false
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

// Función para redirigir a un módulo específico
const redirectToModule = (path) => {
  console.log('Intentando redirigir a:', path);
  console.log('Usuario autenticado:', isAuthenticated.value);
  console.log('Token en localStorage:', localStorage.getItem('auth_token'));

  if (isAuthenticated.value) {
    console.log('Redirigiendo directamente a:', path);
    router.push(path);
  } else {
    console.log('Guardando ruta para después del login:', path);
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
  padding: 2rem 1rem;
}

.background-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  z-index: -2;
}

.background-gradient::after {
  content: '';
  position: absolute;
  width: 300px;
  height: 300px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  filter: blur(50px);
  top: -150px;
  right: -150px;
  z-index: -1;
}

.background-gradient::before {
  content: '';
  position: absolute;
  width: 300px;
  height: 300px;
  background: rgba(13, 110, 253, 0.1);
  border-radius: 50%;
  filter: blur(50px);
  bottom: -150px;
  left: -150px;
  z-index: -1;
}

.main-content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
}

/* Header styles */
.header-section {
  padding-top: 2rem;
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
  border: none;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  padding: 1rem 1.5rem;
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
}

.module-card-modern:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 36px rgba(31, 38, 135, 0.2);
}

.module-enabled:hover .module-icon-container-modern {
  transform: scale(1.1);
}

.module-disabled {
  opacity: 0.6;
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
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 24px 24px 0 0;
  box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.05);
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
    padding: 1rem 0.5rem;
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
}
</style>