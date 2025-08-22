<template>
  <div class="container">
    <main class="flex-grow-1 py-4">
      <div class="container">
        <!-- Sección de presentación -->
        <div class="row align-items-center justify-content-center mb-5">

          <div class="col-md-12 text-center">
            <h1 class="mb-3 text-center text-primary fw-bold">Dirección General de Operaciones en Salud</h1>
            <p class="mb-3 lead">DGOS - DIMON - DIEM</p>

            <div class="alert alert-info d-flex align-items-center mb-4">
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
                  <div class="module-card p-3 p-lg-4 rounded text-center h-100 position-relative"
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
:root {
  --primary: #2c6fbb;
  --primary-dark: #1e5aa0;
  --secondary: #6c757d;
  --success: #198754;
  --info: #0dcaf0;
  --warning: #ffc107;
  --danger: #dc3545;
  --light: #f8f9fa;
  --dark: #212529;
  --gradient-primary: linear-gradient(135deg, #2c6fbb 0%, #3b86d6 100%);
  --gradient-card: linear-gradient(135deg, #ffffff 0%, #f5f9ff 100%);
  --shadow-sm: 0 4px 6px rgba(0, 0, 0, 0.03);
  --shadow-md: 0 6px 12px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.1);
  --border-radius: 12px;
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


.module-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  
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



.module-disabled {
  opacity: 0.7;
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

/* Footer */
.footer {
  z-index: 1;
  position: relative;
}

</style>