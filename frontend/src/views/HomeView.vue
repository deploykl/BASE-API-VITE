<template>
  <div class="container">
    <!-- Fondo con efecto de cristal -->
    <div class="glass-background"></div>

    <div class="container p-2 glass-content">
      <!-- Sección de presentación -->
      <div class="row align-items-center justify-content-center mb-5">
        <div class="col-md-12 text-center">
          <h1 class="my-3 text-center text-primary fw-bold">DIRECCIÓN GENERAL DE OPERACIONES EN SALUD</h1>
          <p class="mb lead">DGOS - DIMON - DIEM</p>

          <div class="alert alert-info d-flex align-items-center mb-4 glass-alert">
            <i class="bi bi-megaphone-fill me-2 fs-4"></i>
            <div class="ms-3">
              <strong>Novedad:</strong> Lanzamiento de la Versión Demo (v1.0) con módulos esenciales
            </div>
          </div>

          <!-- Módulos destacados -->
          <div class="mb-5">
            <h5 class="section-title mb-4 text-center">
              <i class="pi pi-th-large me-2"></i>Módulos Principales
            </h5>
            <div class="row justify-content-center g-3 g-lg-4">
              <div v-for="module in modules" :key="module.id" class="col-10 col-sm-8 col-md-6 col-lg-4 col-xl-3">
                <div class="module-card p-3 p-lg-4 rounded text-center h-100 position-relative glass-card"
                  :class="{ 'module-enabled': module.enabled, 'module-disabled': !module.enabled }"
                  @click="module.enabled ? redirectToModule(module.path) : null">
                  <!-- Badge para módulos deshabilitados -->
                  <div v-if="!module.enabled"
                    class="position-absolute top-0 start-50 translate-middle px-2 py-1 badge bg-warning">
                    Próximamente
                  </div>

                  <div class="module-icon-container mb-3">
                    <i :class="module.icon" class="module-icon"></i>
                  </div>
                  <h6 class="fw-bold mb-2">{{ module.title }}</h6>
                  <p class="small text-muted mb-0">{{ module.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="access-buttons d-flex flex-column align-items-center">
            <button v-if="isAuthenticated" @click="goToDashboard" class="btn btn-primary btn-lg mb-3 px-4 glass-button">
              <i class="bi bi-box-arrow-in-right me-2"></i>Ingresar al Sistema
            </button>
            <router-link v-else to="/login" class="btn btn-primary btn-lg mb-3 px-4 glass-button">
              <i class="bi bi-box-arrow-in-right me-2"></i>Ingresar al Sistema
            </router-link>
          </div>
        </div>

        <footer class="footer pt-4 pb-3 mt-1 glass-footer">
          <div class="row align-items-center">
            <div class="col-md-6 mb-3 mb-md-0">
              <div class="d-flex flex-wrap align-items-center">
                <span class="text-muted me-2">&copy; {{ currentYear }} - Desarrollado por</span>
                <span class="fw-medium text-primary">área de TI de la DGOS</span>
              </div>
            </div>

            <div class="col-md-6">
              <div class="d-flex flex-wrap justify-content-md-end gap-2">
                <small class="text-muted me-2">Tecnologías:</small>
                <span class="tech-badge glass-badge">
                  <img src="@/assets/svg/python.svg" alt="Python" class="w-4 h-4 me-1" />
                  Python
                </span>
                <span class="tech-badge glass-badge">
                  <img src="@/assets/svg/vuejs.svg" alt="Vuejs" class="w-4 h-4 me-1" />
                  Vuejs3
                </span>
                <span class="tech-badge glass-badge">
                  <img src="@/assets/svg/sql_server.svg" alt="Sql Server" class="w-4 h-4 me-1" />
                  Sql Server
                </span>
                <span class="tech-badge glass-badge">
                  <img src="@/assets/svg/vite.svg" alt="Vite" class="w-4 h-4 me-1" />
                  Vite
                </span>
                <span class="tech-badge glass-badge">
                  <img src="@/assets/svg/pinia.svg" alt="Pinia" class="w-4 h-4 me-1" />
                  Pinia
                </span>
                <span class="tech-badge glass-badge">
                  <img src="@/assets/svg/websocket.svg" alt="Websocket" class="w-4 h-4 me-1" />
                  WebSocket
                </span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
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
</script>

<style scoped>
.container {
  background: rgb(255, 255, 255);
  backdrop-filter: blur(1px);
  border-radius: 10px;
}

.section-title:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 25%;
  width: 50%;
  height: 3px;
  background: var(--gradient-primary);
  border-radius: 3px;
}

/* Tarjetas de módulos */
.module-card {
  transition: all 0.3s ease;
  background: var(--gradient-card);
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  border-radius: 50%;
  transition: transform 0.2s, box-shadow 0.2s;

}

.module-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);

}

.module-disabled {
  opacity: 0.4;
  cursor: not-allowed !important;
}

.module-disabled:hover {
  transform: none !important;
  box-shadow: var(--shadow-sm) !important;
}

.module-icon-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: rgba(44, 111, 187, 0.1);
  color: var(--primary);
  margin-bottom: 1rem;
}

.module-icon {
  font-size: 1.8rem;
}

/* Botón de acceso */
.access-btn {
  background: var(--gradient-primary);
  border: none;
  border-radius: 50px;
  font-weight: 600;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
}

.access-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(44, 111, 187, 0.3);
}

/* Nuevo footer styles */
.footer {
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(to right, #f8f9fa, #ffffff, #f8f9fa) !important;
  border-radius: 10px;
}

.tech-badge {
  padding: 0.35rem 0.65rem;
  background-color: rgba(44, 111, 187, 0.1);
  border-radius: 50px;
  font-size: 0.75rem;
  color: #2c6fbb;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  transition: all 0.2s ease;
  margin-bottom: 0.4rem;
}

.tech-badge img {
  width: 18px;
  /* ancho fijo */
  height: 18px;
  /* alto fijo */
  object-fit: contain;
  /* para que el SVG no se deforme */
  margin-right: 4px;
  /* separa del texto */
  vertical-align: middle;
  /* alinea con el texto */
}

.tech-badge:hover {
  background-color: rgba(44, 111, 187, 0.2);
  transform: translateY(-1px);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .custom-footer .row {
    flex-direction: column;
    text-align: center;
  }

  .custom-footer .justify-content-md-end {
    justify-content: center !important;
  }
}
</style>