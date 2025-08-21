<template>
  <div class="container-fluid">
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
            
            <!-- Módulos destacados -->
            <div class="mb-4">
              <h5 class="mb-3 text-center"><i class="pi pi-th-large me-2"></i>Módulos Principales</h5>
              <div class="row justify-content-center g-3">
               
                <!-- Módulo de Personal -->
                <div class="col-8 col-sm-6 col-md-5 col-lg-3">
                  <div class="module-card p-3 border rounded bg-light text-center h-100" @click="redirectToModule('/user/create')">
                    <i class="pi pi-users fs-3 text-purple mb-2"></i>
                    <h6 class="fw-bold">Personal</h6>
                    <p class="small text-muted mb-0">Gestión del equipo</p>
                  </div>
                </div>
               
                <!-- Módulo de Arquitectura -->
                <div class="col-8 col-sm-6 col-md-5 col-lg-3">
                  <div class="module-card p-3 border rounded bg-light text-center h-100" @click="redirectToModule('/dashboard')">
                    <i class="pi pi-sitemap fs-3 text-primary mb-2"></i>
                    <h6 class="fw-bold">Arquitectura</h6>
                    <p class="small text-muted mb-0">Diseño del sistema completo</p>
                  </div>
                </div>

                 <!-- Módulo de Autenticación -->
                <div class="col-8 col-sm-6 col-md-5 col-lg-3">
                  <div class="module-card p-3 border rounded bg-light text-center h-100" @click="redirectToModule('/dashboard')">
                    <i class="pi pi-lock fs-3 text-warning mb-2"></i>
                    <h6 class="fw-bold">Autenticación</h6>
                    <p class="small text-muted mb-0">Gestión de usuarios y accesos</p>
                  </div>
                </div>

                <!-- Módulo de Informática -->
                <div class="col-8 col-sm-6 col-md-5 col-lg-3">
                  <div class="module-card p-3 border rounded bg-light text-center h-100" @click="redirectToModule('/dashboard')">
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
  if (!token) return false;
  
  // Verificar si el token es válido (puedes agregar más verificaciones aquí)
  // Por ejemplo, verificar la expiración si guardaste esa información
  return true;
});
const currentYear = ref(new Date().getFullYear());

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
</style>