<template>
  <div class="maintenance-container p-d-flex p-jc-center p-ai-center p-min-vh-100">
    <Card class="maintenance-card text-center p-shadow-8">
      <template #header>
        <div class="p-d-flex p-jc-center p-p-3">
          <i class="pi pi-cog p-text-primary" style="font-size: 3rem"></i>
        </div>
      </template>
      
      <template #title>
        <div class="p-text-center p-text-bold">Estamos realizando mantenimiento</div>
      </template>
      
      <template #content>
        <div class="p-text-center p-mb-4">
          <p class="p-text-secondary">El servicio no está disponible en este momento.</p>
          <p class="p-text-secondary">Estamos trabajando para solucionarlo lo antes posible.</p>
        </div>
        
        <div class="p-d-flex p-flex-column p-ai-center p-gap-1">
          <Button 
            @click="checkStatus" 
            :label="buttonLabel" 
            icon="pi pi-refresh" 
            :loading="isChecking"
            :disabled="isChecking"
            class="p-button-rounded p-button-lg me-4"
            style="min-width: 200px;"
          />
          
          <Button 
            v-if="!isAuthenticated"
            @click="goHome" 
            label="Ir a la página principal" 
            icon="pi pi-home" 
            severity="secondary"
            class="p-button-rounded p-button-lg"
            style="min-width: 200px;"
          />
        </div>
        
        <Divider class="p-my-4" />
        
        <div class="p-d-flex p-flex-column p-ai-center p-gap-2">
          <div class="p-text-sm p-text-secondary">
            Última verificación: {{ lastCheck ? lastCheck.toLocaleTimeString() : 'Nunca' }}
          </div>
          <div v-if="retryCount > 0" class="p-text-sm mb-2">
            <Tag :value="`Intentos: ${retryCount}`" severity="info" />
          </div>
          <div v-if="nextRetryIn > 0" class="p-text-sm">
            <Tag :value="`Próximo intento en: ${nextRetryIn}s`" severity="warning" />
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'

import { api } from '@/components/services/Axios'

const router = useRouter()
const lastCheck = ref(null)
const isAuthenticated = ref(localStorage.getItem('auth_token'))
const isChecking = ref(false)
const retryCount = ref(0)
const nextRetryIn = ref(0)
let intervalId = null
let countdownInterval = null

const buttonLabel = computed(() => {
  if (isChecking.value) return 'Verificando...'
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
  padding: 2rem;
}

.maintenance-card {
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: none;
}

:deep(.p-card-title) {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-color);
}

:deep(.p-card-content) {
  padding-bottom: 0;
}
</style>