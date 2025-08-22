<template>
  <div class="container-fluid position-relative">
    <!-- Marca de agua "En Proyecto" -->
    <div class="watermark position-fixed top-50 start-50 translate-middle">
      <div class="text-center">
        <span class="watermark-text">EN PROYECTO</span>
        <div class="watermark-subtext">Versión Demo v1.0</div>
      </div>
    </div>
    
    <main class="flex-grow-1 py-4">
      <div class="container">
        <!-- Sección de presentación -->
        <div class="row align-items-center justify-content-center mb-5">
          
          <div class="col-md-12 text-center">
            <h1 class="mb-3 text-center text-primary fw-bold">Dirección General de Operaciones en Salud</h1>
            <p class="mb-3 lead">DGOS - DIMON - DIEM</p>

            <div class="alert alert-info d-flex align-items-center mb-4">
              <i class="bi bi-exclamation-circle-fill me-2 fs-4"></i>
              <div>
                <strong>Novedad:</strong> Lanzamiento de la Versión Demo (v1.0) con módulos esenciales
              </div>
            </div>
            
            <!-- Módulos destacados (simplificado) -->
            <div class="mb-4">
              <h5 class="mb-3 text-center"><i class="pi pi-th-large me-2"></i>Módulos Principales</h5>
              <div class="row justify-content-center g-3">
                <div v-for="module in modules" :key="module.id" class="col-8 col-sm-6 col-md-5 col-lg-3">
                  <div 
                    class="module-card p-3 border rounded text-center h-100 position-relative" 
                    :class="{'bg-light': module.enabled, 'bg-light disabled-module': !module.enabled}"
                    @click="module.enabled ? redirectToModule(module.path) : null"
                  >
                    <!-- Badge para módulos deshabilitados -->
                    <div v-if="!module.enabled" class="position-absolute top-0 start-50 translate-middle px-2 badge bg-warning text-dark">
                      Próximamente
                    </div>
                    
                    <i :class="module.icon" class="fs-3 mb-2" :style="{color: module.color}"></i>
                    <h6 class="fw-bold">{{ module.title }}</h6>
                    <p class="small text-muted mb-0">{{ module.description }}</p>
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
            </div>
          </div>
        </div>
      </div>
      
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
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = computed(() => {
  const token = localStorage.getItem('auth_token');
  return !!token;
});

const currentYear = ref(new Date().getFullYear());

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
    description: 'Control de equipos',
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
    title: 'Informática',
    description: 'Control de equipos',
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
</script>

<style scoped>
.module-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.module-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

/* Estilos para módulos deshabilitados */
.disabled-module {
  opacity: 0.7;
  cursor: not-allowed !important;
}

.disabled-module:hover {
  transform: none !important;
  box-shadow: none !important;
}

/* Estilos para la marca de agua */
.watermark {
  z-index: -1; /* Para que esté detrás del contenido */
  pointer-events: none; /* Para que no interfiera con los clics */
}

.watermark-text {
  font-size: 5rem;
  font-weight: 900;
  color: rgba(0, 123, 255, 0.08); /* Azul muy transparente */
  text-transform: uppercase;
  letter-spacing: 5px;
  transform: rotate(-30deg);
}

.watermark-subtext {
  font-size: 1.5rem;
  font-weight: 700;
  color: rgba(108, 117, 125, 0.1);
  transform: rotate(-30deg);
  margin-top: -20px;
}

/* Responsividad para la marca de agua */
@media (max-width: 768px) {
  .watermark-text {
    font-size: 3rem;
  }
  
  .watermark-subtext {
    font-size: 1rem;
    margin-top: -10px;
  }
}
</style>