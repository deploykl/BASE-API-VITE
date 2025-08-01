<template>
  <div class="background-container">
    <div class="login-container">
      <!-- Fondo con imagen y blur -->
      <div class="background-blur"></div>
      <div class="login-wrapper">
        <div class="login-card">
          <!-- Logo con diseño moderno -->
          <div class="logo-container">
            <div class="logo-circle">
              <img src="@/assets/img/account/user-account.png" alt="Logo" class="logo-img" />
            </div>
            <h1 class="app-title">Panel de Control</h1>
            <h2 class="welcome-text">Autenticación requerida</h2>
          </div>

          <!-- Mensaje de error mejorado -->
          <ErrorMessage />
          <!-- Formulario con diseño moderno -->
          <form @submit.prevent="handleSubmit" class="login-form">
            <!-- Campo Usuario con float label -->
            <div class="input-group">
              <div class="input-icon">
                <i class="fas fa-user"></i>
              </div>
              <input type="text" id="username" v-model="username" @input="handleLowerCASE" class="input-field"
                placeholder=" " required />
              <label for="username" class="float-label">Nombre de usuario</label>
            </div>

            <!-- Campo Contraseña con float label -->
            <div class="input-group">
              <div class="input-icon">
                <i class="fas fa-lock"></i>
              </div>
              <input :type="showPassword ? 'text' : 'password'" id="password" v-model="password" class="input-field"
                placeholder=" " required />
              <label for="password" class="float-label">Contraseña</label>
              <div class="password-toggle" @click="showPassword = !showPassword">
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </div>
            </div>

            <!-- Botón con diseño moderno -->
            <button type="submit" class="login-btn" :disabled="isLoading">
              <span v-if="isLoading" class="btn-loader"></span>
              <span v-else>
                <i class="fas fa-sign-in-alt"></i> Ingresar
              </span>
            </button>
          </form>

          <!-- Enlace olvidé contraseña con diseño minimalista -->
          <div class="forgot-password">
            <router-link to="/password-reset" class="forgot-link">
              ¿Olvidaste tu contraseña?
            </router-link>
          </div>

          <!-- Footer minimalista -->
          <div class="login-footer">
            <span class="version">v1.0.0</span>
            <span class="copyright">© 2023 OBS Salud</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/components/services/Axios';
import { useUserStore } from '@/store/gore/userStore'

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const showPassword = ref(false)
const router = useRouter()
const userStore = useUserStore()

const handleLowerCASE = (event) => {
  const targetField = event.target.id;
  if (targetField === 'username') {
    username.value = event.target.value.toLowerCase();
  }
};

const handleSubmit = async () => {
  isLoading.value = true;

  try {
    const response = await api.post('gore/login/', {  // Asegúrate que coincida con tu backend
      username: username.value,
      password: password.value,
    });

    const { access, refresh, user } = response.data;

    if (!access || !user) {
      throw new Error('Respuesta de login inválida');
    }

    localStorage.setItem('auth_token', access);
    if (refresh) localStorage.setItem('refreshToken', refresh);
    
    router.push('/dashboard');
  } catch (error) {
    let errorMessage = 'Error al conectar con el servidor';
    
    if (error.response) {
      errorMessage = error.response.data?.detail || errorMessage;
    } else if (error.code === 'ECONNABORTED') {
      errorMessage = 'Tiempo de espera agotado';
    } else if (error.code === 'ERR_NETWORK') {
      errorMessage = 'No se pudo conectar al servidor. Verifica tu conexión.';
    }
    
    console.error('Error en login:', error);
    alert(errorMessage);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.background-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  /* Esto recorta el exceso de blur */
}

.background-container::before {
  content: "";
  position: absolute;
  top: -20px;
  /* Expansión hacia arriba */
  left: -20px;
  /* Expansión hacia la izquierda */
  right: -20px;
  /* Expansión hacia la derecha */
  bottom: -20px;
  /* Expansión hacia abajo */
  background-image: url('@/assets/img/account/background3.jpg');
  background-size: cover;
  background-position: center;
  filter: blur(8px);
  z-index: -1;
}

/* Estilos base */
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-size: cover;
}

.forgot-password {
  text-align: center;
  margin: 15px 0;
}

.welcome-text {
  font-size: 14px;
  color: #6b7280;
  font-weight: 400;
  margin: 8px 0 4px;
  letter-spacing: 1px;
}

.forgot-link {
  color: #3498db;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.forgot-link:hover {
  color: #2980b9;
  text-decoration: underline;
}

.forgot-link i {
  font-size: 16px;
}

.login-wrapper {
  width: 100%;
  max-width: 420px;
  padding: 0 20px;
}

.login-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  padding: 40px;
  animation: fadeIn 0.6s ease-in-out;
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

/* Logo */
.logo-container {
  text-align: center;
  margin-bottom: 20px;
}

.logo-img {
  max-width: 250px;
  height: 100px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

/* Campos de entrada */
.input-group {
  position: relative;
  margin-bottom: 25px;
}

.input-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #364257;
  font-size: 18px;
  opacity: 0.7;
  z-index: 1;
}

.input-field {
  width: 100%;
  padding: 22px 14px 8px 42px;
  border: none;
  border-bottom: 1px solid #d1d5db;
  font-size: 15px;
  background-color: transparent;
  color: #333;
  transition: border-bottom 0.3s ease;
}

.input-field:focus {
  outline: none;
  border-bottom: 2px solid #364257;
  box-shadow: 0 0 0 2px white;
  /* Opcional: añade un glow blanco si lo prefieres */
}

/* Float label */
.float-label {
  position: absolute;
  left: 42px;
  top: 18px;
  color: #6b7280;
  font-size: 15px;
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  transform-origin: left top;
  background-color: transparent;
  padding: 0 4px;
  z-index: 1;
}

.input-field:focus~.float-label,
.input-field:not(:placeholder-shown)~.float-label {
  transform: translateY(-24px) scale(0.85);
  color: #364257;
  background-color: white;
  padding: 0 4px;
  left: 38px;
}

/* Toggle de contraseña */
.password-toggle {
  position: absolute;
  right: 12px;
  top: 18px;
  color: #6b7280;
  cursor: pointer;
  font-size: 18px;
  transition: color 0.3s ease;
  z-index: 2;
}

.password-toggle:hover {
  color: #364257;
}

.login-btn span {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

/* Botón de login */
.login-btn {
  width: 100%;
  padding: 15px;
  background: #364257;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s, transform 0.2s;
  margin-top: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.login-btn:disabled {
  background: #bdbdbd;
  transform: none;
  box-shadow: none;
  cursor: not-allowed;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Footer minimalista */
.login-footer {
  margin-top: 32px;
  text-align: center;
  color: #6b7280;
  font-size: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.btn-loader {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.version {
  font-weight: 500;
}

.copyright {
  opacity: 0.8;
}
</style>