<template>
  <div class="maintenance-container">
    <div class="maintenance-card">
      <div class="card-header">
        <div class="icon-container">
          <span class="icon">🔧</span>
        </div>
        <h1>Estamos realizando mantenimiento</h1>
      </div>
      
      <div class="card-content">
        <p class="message">El servicio no está disponible en este momento.</p>
        <p class="message">Estamos trabajando para solucionarlo lo antes posible.</p>
        
        <div class="actions">
          <button 
            @click="checkStatus" 
            :disabled="isChecking"
            class="retry-button"
          >
            <span v-if="isChecking" class="button-loading">
              <span class="spinner"></span> Verificando...
            </span>
            <span v-else>
              <span class="button-icon">🔄</span> {{ buttonLabel }}
            </span>
          </button>
          
          <button 
            v-if="!isAuthenticated"
            @click="goHome" 
            class="home-button"
          >
            <span class="button-icon">🏠</span> Ir a la página principal
          </button>
        </div>
        
        <div class="divider"></div>
        
        <div class="status-info">
          <div class="status-item">
            <span class="status-label">Última verificación:</span>
            <span class="status-value">{{ lastCheck ? lastCheck.toLocaleTimeString() : 'Nunca' }}</span>
          </div>
          <div v-if="retryCount > 0" class="status-item">
            <span class="status-label">Intentos:</span>
            <span class="status-badge">{{ retryCount }}</span>
          </div>
          <div v-if="nextRetryIn > 0" class="status-item">
            <span class="status-label">Próximo intento:</span>
            <span class="status-countdown">{{ nextRetryIn }}s</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { api, checkBackendHealth } from '@/components/services/Axios'

const router = useRouter()
const lastCheck = ref(null)
const isAuthenticated = ref(localStorage.getItem('auth_token'))
const isChecking = ref(false)
const retryCount = ref(0)
const nextRetryIn = ref(0)
let intervalId = null
let countdownInterval = null

const buttonLabel = computed(() => {
  return retryCount.value > 0 ? 'Reintentar ahora' : 'Verificar conexión'
})

const checkStatus = async () => {
  if (isChecking.value) return
  
  isChecking.value = true
  try {
    lastCheck.value = new Date()
    const response = await api.get('user/health-check/', { timeout: 3000 })
    
    if (response.data.status === 'OK' || response.data.status === 'DEGRADED') {
      stopAutoRetry()
      if (isAuthenticated.value) {
        router.push('/dashboard')
      } else {
        router.push('/')
      }
    }
  } catch (error) {
    lastCheck.value = new Date()
    startCountdown()
  } finally {
    isChecking.value = false
    retryCount.value++
  }
}

const startCountdown = () => {
  nextRetryIn.value = 5
  clearInterval(countdownInterval)
  countdownInterval = setInterval(() => {
    nextRetryIn.value--
    if (nextRetryIn.value <= 0) {
      clearInterval(countdownInterval)
      checkStatus()
    }
  }, 1000)
}

const startAutoRetry = () => {
  checkStatus()
  intervalId = setInterval(checkStatus, 5000)
}

const stopAutoRetry = () => {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
  clearInterval(countdownInterval)
  nextRetryIn.value = 0
}

const goHome = () => {
  stopAutoRetry()
  router.push('/')
}

onMounted(startAutoRetry)
onUnmounted(stopAutoRetry)
</script>

<style scoped>
.maintenance-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f6f7f9 0%, #e7e9ee 100%);
  padding: 1rem;
}

.maintenance-card {
  width: 100%;
  max-width: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  padding: 2rem 2rem 1rem;
  text-align: center;
}

.icon-container {
  margin-bottom: 1rem;
}

.icon {
  font-size: 3rem;
}

h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.card-content {
  padding: 0 2rem 2rem;
}

.message {
  color: #7f8c8d;
  text-align: center;
  margin: 0.5rem 0;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin: 1.5rem 0;
}

button {
  padding: 0.75rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.retry-button {
  background-color: #3498db;
  color: white;
}

.retry-button:not(:disabled):hover {
  background-color: #2980b9;
}

.retry-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.home-button {
  background-color: #2ecc71;
  color: white;
}

.home-button:hover {
  background-color: #27ae60;
}

.button-icon {
  font-size: 1.1em;
}

.button-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.divider {
  height: 1px;
  background-color: #ecf0f1;
  margin: 1.5rem 0;
}

.status-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.status-value, .status-badge, .status-countdown {
  font-weight: 600;
  font-size: 0.9rem;
}

.status-badge {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.status-countdown {
  background-color: #fff8e1;
  color: #ff8f00;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>