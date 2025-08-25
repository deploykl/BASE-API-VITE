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
          <!-- Mostrar intentos restantes si existen -->
          <div v-if="remainingAttempts !== null" class="attempts-warning">
            <div class="attempts-content">
              <i class="fas fa-exclamation-triangle"></i>
              <div class="attempts-text">
                <div class="d-flex justify-content-center align-items-center">
                  <small class="text-muted me-2">Intentos restantes:</small>
                  <span class="badge bg-warning text-dark">{{ remainingAttempts }}</span>
                </div>
              </div>
            </div>
          </div>
          <!-- Temporizador de cuenta bloqueada -->
          <div v-if="blockedTimeRemaining" class="blocked-timer">
            <div class="timer-content">
              <i class="fas fa-lock"></i>
              <div class="timer-text">
                <p>Cuenta bloqueada temporalmente</p>
                <div class="countdown">
                  Tiempo restante:
                  <span class="time">{{ formatTime(blockedTimeRemaining) }}</span>
                </div>
              </div>
            </div>
            <div class="timer-progress">
              <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
            </div>
            <!-- Botón para ingresar con otra cuenta -->
            <div class="use-another-account">
              <button @click="useAnotherAccount" class="another-account-btn">
                <i class="fas fa-user-plus"></i> Ingresar con otra cuenta
              </button>
            </div>
          </div>

          <!-- Formulario con diseño moderno -->
          <form @submit.prevent="handleSubmit" class="login-form">
            <!-- Campo Usuario con float label -->
            <div class="input-group">
              <div class="input-icon">
                <i class="fas fa-user"></i>
              </div>
              <input type="text" id="username" v-model="username" @input="handleLowerCASE" class="input-field"
                placeholder=" " :disabled="isBlocked" required />
              <label for="username" class="float-label">Nombre de usuario</label>
            </div>

            <!-- Campo Contraseña con float label -->
            <div class="input-group">
              <div class="input-icon">
                <i class="fas fa-lock"></i>
              </div>
              <input :type="showPassword ? 'text' : 'password'" id="password" v-model="password" class="input-field"
                placeholder=" " :disabled="isBlocked" required />
              <label for="password" class="float-label">Contraseña</label>
              <div class="password-toggle" @click="showPassword = !showPassword">
                <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
              </div>
            </div>

            <!-- Botón con diseño moderno -->
            <button type="submit" class="login-btn" :disabled="isLoading || isBlocked"
              :class="{ 'btn-blocked': isBlocked }">
              <span v-if="isLoading" class="btn-loader"></span>
              <span v-else>
                <i class="fas fa-sign-in-alt"></i>
                {{ isBlocked ? 'Cuenta Bloqueada' : 'Ingresar' }}
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
            <span class="version">{{ version }}</span>
            <span class="copyright">© {{ new Date().getFullYear() }} {{ projectName }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/components/services/Axios';
import { useErrorStore } from '@/stores/errorStore'

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const showPassword = ref(false)
const blockedTimeRemaining = ref(0)
const blockedTimeTotal = ref(0)
const countdownInterval = ref(null)
const remainingAttempts = ref(null) // ← Nueva variable para intentos restantes
const projectName = import.meta.env.VITE_PROJECT_NAME
const version = import.meta.env.VITE_VERSION
const router = useRouter()
const errorStore = useErrorStore()

// Computed propertiesisLoading.value = true;
const isBlocked = computed(() => blockedTimeRemaining.value > 0)
const progressPercentage = computed(() => {
  if (blockedTimeTotal.value <= 0) return 0
  return 100 - (blockedTimeRemaining.value / blockedTimeTotal.value * 100)
})

// Formatear tiempo en minutos y segundos
const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const handleLowerCASE = (event) => {
  const targetField = event.target.id;
  if (targetField === 'username') {
    username.value = event.target.value.toLowerCase();
  }
};
// Función para usar otra cuenta
const useAnotherAccount = () => {
  // Limpiar el bloqueo actual
  if (countdownInterval.value) {
    clearInterval(countdownInterval.value)
    countdownInterval.value = null
  }
  blockedTimeRemaining.value = 0
  blockedTimeTotal.value = 0

  // Limpiar el almacenamiento local relacionado con bloqueos
  localStorage.removeItem('accountBlockExpiry')
  localStorage.removeItem('lastAttemptUsername')

  // Limpiar campos y mensajes de error
  username.value = ''
  password.value = ''
  errorStore.clearMessage()

  console.log("Modo para ingresar con otra cuenta activado")
}
// Iniciar el contador regresivo
const startCountdown = (minutes) => {
  // Limpiar intervalo existente
  if (countdownInterval.value) {
    clearInterval(countdownInterval.value)
  }

  blockedTimeTotal.value = minutes * 60
  blockedTimeRemaining.value = minutes * 60

  countdownInterval.value = setInterval(() => {
    if (blockedTimeRemaining.value > 0) {
      blockedTimeRemaining.value--
    } else {
      clearInterval(countdownInterval.value)
      countdownInterval.value = null
    }
  }, 1000)
}

// Detectar si hay un bloqueo activo consultando al backend
const checkExistingBlock = async () => {
  try {
    // Verificar si hay un usuario en localStorage que podría estar bloqueado
    const lastUsername = localStorage.getItem('lastAttemptUsername');
    if (!lastUsername) return;

    // Consultar al backend el estado del usuario
    const response = await api.post('user/check-block-status/', {
      username: lastUsername
    });

    if (response.data.is_blocked) {
      const remainingMinutes = response.data.remaining_minutes;
      startCountdown(remainingMinutes);
      errorStore.showMessage(`Cuenta bloqueada. Espere ${formatTime(remainingMinutes * 60)}.`, 'warning');
    }
  } catch (error) {
    console.error("Error al verificar estado de bloqueo:", error);
    // Si hay error, mantener la lógica anterior de localStorage como fallback
    const blockExpiry = localStorage.getItem('accountBlockExpiry')
    if (blockExpiry) {
      const expiryTime = new Date(parseInt(blockExpiry))
      const now = new Date()
      const remainingSeconds = Math.max(0, Math.floor((expiryTime - now) / 1000))

      if (remainingSeconds > 0) {
        const minutes = Math.ceil(remainingSeconds / 60)
        startCountdown(minutes)
        errorStore.showMessage(`Cuenta bloqueada. Espere ${formatTime(remainingSeconds)}.`, 'warning')
      } else {
        localStorage.removeItem('accountBlockExpiry')
      }
    }
  }
}

const handleSubmit = async () => {
  // Si la cuenta está bloqueada, no hacer nada
  if (isBlocked.value) {
    return
  }

  errorStore.clearMessage()
  isLoading.value = true;
  remainingAttempts.value = null; // Resetear intentos restantes

  try {
    // Guardar el nombre de usuario para posibles verificaciones futuras
    localStorage.setItem('lastAttemptUsername', username.value);

    const response = await api.post('user/login/', {
      username: username.value,
      password: password.value,
    });

    const { access, refresh, user_id,is_superuser, is_staff, modulos, modulos_desactivados, warning } = response.data;

    if (!access) {
      console.error("Error: No se recibió token de acceso")
      errorStore.showMessage('No se recibió token de acceso.')
      return;
    }

    // Limpiar cualquier bloqueo previo
    localStorage.removeItem('accountBlockExpiry')
    localStorage.removeItem('lastAttemptUsername');
    if (countdownInterval.value) {
      clearInterval(countdownInterval.value)
      countdownInterval.value = null
    }
    blockedTimeRemaining.value = 0

    // Mostrar información de módulos en consola
    console.log("Módulos activos:", modulos);
    if (modulos_desactivados) {
      console.log("Módulos desactivados:", modulos_desactivados);
    }
    if (warning) {
      console.warn("Advertencia:", warning);
    }

    // Guardar datos
    localStorage.setItem('auth_token', access);
    if (refresh) localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('user_id', user_id); // ← GUARDAR USER_ID
    localStorage.setItem('is_superuser', is_superuser ? 'true' : 'false');
    localStorage.setItem('is_staff', is_staff ? 'true' : 'false');
    localStorage.setItem('user_modulos', JSON.stringify(modulos));

    // Verificar si hay una ruta de redirección guardada
    const redirectPath = localStorage.getItem('redirectAfterLogin');

    if (redirectPath) {
      localStorage.removeItem('redirectAfterLogin');
      router.push(redirectPath);
    } else {
      router.push('/dashboard');
    }

  } catch (error) {
    console.error("Error en login:", error)

    // Manejar bloqueo de cuenta
    if (error.response?.status === 403 && error.response.data.detail?.includes('bloqueada')) {
      const match = error.response.data.detail.match(/(\d+)\s*minutos/)
      if (match && match[1]) {
        const minutes = parseInt(match[1])

        // Calcular tiempo de expiración y guardar en localStorage
        const expiryTime = new Date()
        expiryTime.setMinutes(expiryTime.getMinutes() + minutes)
        localStorage.setItem('accountBlockExpiry', expiryTime.getTime().toString())

        // Iniciar contador
        startCountdown(minutes)
      }
    }

    // ✅ CORRECCIÓN: Manejar todos los tipos de errores correctamente
    if (error.response?.data) {
      // Mostrar el mensaje de error del backend directamente
      if (error.response.data.detail) {
        errorStore.showMessage(error.response.data.detail)

        // Mostrar información adicional si existe
        if (error.response.data.modulos_desactivados) {
          console.log("Módulos desactivados:", error.response.data.modulos_desactivados)
        }

        // ✅ CORRECCIÓN: Guardar intentos restantes para mostrarlos en la UI
        if (error.response.data.remaining_attempts !== undefined) {
          remainingAttempts.value = error.response.data.remaining_attempts;
          console.log("Intentos restantes:", remainingAttempts.value);
        }
      }
      // Manejar errores de validación de formulario
      else if (typeof error.response.data === 'object') {
        const firstError = Object.values(error.response.data)[0];
        if (Array.isArray(firstError)) {
          errorStore.showMessage(firstError[0])
        } else {
          errorStore.showMessage(firstError || 'Error de validación')
        }
      }
      // Manejar otros formatos de error
      else {
        errorStore.showMessage(error.response.data.toString() || 'Error desconocido')
      }
    }
    // Error de conexión
    else if (error.request) {
      errorStore.showMessage('Error de conexión. Verifique su internet e intente nuevamente.')
    }
    // Error inesperado
    else {
      errorStore.showMessage('Error inesperado. Por favor intente nuevamente.')
    }
  } finally {
    isLoading.value = false;
  }
};

// Verificar bloqueo existente al cargar el componente
onMounted(() => {
  checkExistingBlock()
})

// Limpiar intervalo al desmontar el componente
onUnmounted(() => {
  if (countdownInterval.value) {
    clearInterval(countdownInterval.value)
  }
})
</script>

<style scoped>
.background-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.background-container::before {
  content: "";
  position: absolute;
  top: -20px;
  left: -20px;
  right: -20px;
  bottom: -20px;
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
  position: relative;
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

/* Temporizador de cuenta bloqueada */
.blocked-timer {
  background: linear-gradient(135deg, #fff6e6 0%, #ffe6e6 100%);
  border: 1px solid #ffcccb;
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 20px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 100, 100, 0.4);
  }

  70% {
    box-shadow: 0 0 0 10px rgba(255, 100, 100, 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(255, 100, 100, 0);
  }
}

.timer-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.timer-content i {
  font-size: 24px;
  color: #ff4757;
}

.timer-text p {
  margin: 0;
  font-weight: 600;
  color: #ff4757;
  font-size: 14px;
}

.countdown {
  margin-top: 5px;
  font-size: 13px;
  color: #666;
}

.countdown .time {
  font-weight: bold;
  color: #ff4757;
  font-family: monospace;
  font-size: 15px;
}

.timer-progress {
  height: 6px;
  background: #ffe0e0;
  border-radius: 3px;
  margin-top: 10px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #ff7e7e 0%, #ff4757 100%);
  border-radius: 3px;
  transition: width 1s linear;
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
}

.input-field:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

.input-field:disabled~.float-label {
  color: #aaa;
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

.input-field:disabled~.password-toggle {
  opacity: 0.5;
  cursor: not-allowed;
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

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.login-btn:disabled {
  background: #bdbdbd;
  transform: none;
  box-shadow: none;
  cursor: not-allowed;
}

.btn-blocked {
  background: #ff4757 !important;
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

/* Estilos para el botón de otra cuenta */
.use-another-account {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 100, 100, 0.3);
}

.another-account-btn {
  width: 100%;
  padding: 10px 15px;
  background: transparent;
  color: #3498db;
  border: 1px solid #3498db;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.another-account-btn:hover {
  background: #3498db;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
}

.another-account-btn:active {
  transform: translateY(0);
}

/* Ajustes al temporizador para acomodar el nuevo botón */
.blocked-timer {
  background: linear-gradient(135deg, #fff6e6 0%, #ffe6e6 100%);
  border: 1px solid #ffcccb;
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 20px;
  animation: pulse 2s infinite;
  position: relative;
}

/* Estilos para el mensaje de intentos restantes */
.attempts-warning {
  background: linear-gradient(135deg, #fff9e6 0%, #fff3e6 100%);
  border: 1px solid #ffd699;
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 20px;
  animation: fadeIn 0.5s ease-in-out;
}

.attempts-content {
  align-items: center;
  text-align: center;
  gap: 12px;
}

.attempts-content i {
  font-size: 24px;
  color: #ff9800;
}

.attempts-text p {
  margin: 0;
  font-weight: 600;
  color: #ff9800;
  font-size: 14px;
  text-align: center;
}

.attempts-count {
  margin-top: 5px;
  font-size: 13px;
  color: #666;
}

.attempts-count .count {
  font-weight: bold;
  color: #ff6b00;
  font-size: 15px;
  padding: 2px 6px;
  background: rgba(255, 107, 0, 0.1);
  border-radius: 4px;
}

/* Animación para aparecer suavemente */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>