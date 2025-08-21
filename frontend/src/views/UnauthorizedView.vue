<template>
  <div class="unauthorized-container">
    <div class="error-card">
      <div class="error-icon">
        <i class="fas fa-ban"></i>
      </div>
      <h1>Acceso no autorizado</h1>
      <p v-if="isAuthenticated">
        No tienes permisos para acceder a este módulo.
      </p>
      <p v-else>
        Debes iniciar sesión para acceder a esta página.
      </p>
      <div class="action-buttons">
        <button v-if="isAuthenticated" @click="goToDashboard" class="btn-primary">
          Volver al Dashboard
        </button>
        <button v-else @click="goToLogin" class="btn-primary">
          Ir al Login
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = computed(() => localStorage.getItem('auth_token'));

const goToDashboard = () => {
  router.push('/dashboard');
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.unauthorized-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  padding: 20px;
}

.error-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.error-icon {
  font-size: 64px;
  color: #dc3545;
  margin-bottom: 20px;
}

h1 {
  color: #343a40;
  margin-bottom: 16px;
  font-size: 28px;
}

p {
  color: #6c757d;
  margin-bottom: 24px;
  font-size: 16px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.btn-primary {
  background: #364257;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.btn-primary:hover {
  background: #2a3447;
}
</style>