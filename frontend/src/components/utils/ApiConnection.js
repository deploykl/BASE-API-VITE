import { ref, onMounted, onUnmounted } from 'vue'
import { api } from '@/components/services/Axios'

export function useApiConnection() {
  const isApiConnected = ref(null)
  const isLoading = ref(false)
  const retryCount = ref(0)
  const maxRetries = 3
  let connectionInterval = null
  let retryTimeout = null
let timeoutId = null;

  const checkApiConnection = async () => {
    if (isLoading.value) return
    
    isLoading.value = true
    try {
      // Usamos un timeout más corto para mayor reactividad
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 3000) // 3 segundos de timeout
      
      const response = await api.options('', {
        signal: controller.signal
      })
      
      clearTimeout(timeoutId)
      
      // Verificamos que la respuesta sea válida
      if (response.status >= 200 && response.status < 500) {
        isApiConnected.value = true
        retryCount.value = 0
        adjustCheckFrequency(true)
      } else {
        throw new Error('Invalid response status')
      }
    } catch (error) {
      clearTimeout(timeoutId)
      retryCount.value++
      isApiConnected.value = false
      adjustCheckFrequency(false)
      
      // Reintento más agresivo si falla
      if (retryCount.value <= maxRetries) {
        retryTimeout = setTimeout(checkApiConnection, 1000) // Reintento en 1 segundo
      }
    } finally {
      isLoading.value = false
    }
  }

  const adjustCheckFrequency = (isConnected) => {
    clearInterval(connectionInterval)
    clearTimeout(retryTimeout)
    
    if (isConnected) {
      // Si está conectado, verificamos cada 30 segundos
      connectionInterval = setInterval(checkApiConnection, 30000)
    } else {
      // Si falla, verificamos cada 5 segundos
      connectionInterval = setInterval(checkApiConnection, 5000)
    }
  }

  // Verificación inmediata al montar
  onMounted(() => {
    checkApiConnection()
    connectionInterval = setInterval(checkApiConnection, 30000)
  })

  // Limpieza al desmontar
  onUnmounted(() => {
    clearInterval(connectionInterval)
    clearTimeout(retryTimeout)
  })

  return { 
    isApiConnected, 
    isLoading,
    checkApiConnection 
  }
}