<template>
  <div 
    class="api-status-indicator"
    :class="statusClass"
    :title="tooltipText"
    @click="checkApiConnection"
  >
    <i :class="iconClass"></i>
    <span v-if="!isMobile" class="status-text">{{ statusText }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  isApiConnected: Boolean,
  isCheckingApi: Boolean,
  isMobile: Boolean,
  checkApiConnection: Function
})

const statusClass = computed(() => ({
  'online': props.isApiConnected === true,
  'offline': props.isApiConnected === false,
  'checking': props.isCheckingApi
}))

const iconClass = computed(() => ({
  'fas': true,
  'fa-server': props.isApiConnected === true && !props.isCheckingApi,
  'fa-server-slash': props.isApiConnected === false && !props.isCheckingApi,
  'fa-circle-notch fa-spin': props.isCheckingApi
}))

const statusText = computed(() => {
  if (props.isCheckingApi) return 'Verificando API...'
  return props.isApiConnected ? 'API Conectado' : 'API Desconectado'
})

const tooltipText = computed(() => {
  if (props.isCheckingApi) return 'Verificando conexión con el servidor...'
  return props.isApiConnected ? 
    'Conexión estable con el servidor' : 
    'Problemas de conexión con el servidor'
})
</script>

<style scoped>
.api-status-indicator {
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.api-status-indicator.online {
  background-color: rgba(40, 167, 69, 0.15);
  color: #28a745;
  border: 1px solid #28a745;
}

.api-status-indicator.offline {
  background-color: rgba(220, 53, 69, 0.15);
  color: #dc3545;
  border: 1px solid #dc3545;
}

.api-status-indicator.checking {
  background-color: rgba(255, 193, 7, 0.15);
  color: #ffc107;
  border: 1px solid #ffc107;
}

.status-text {
  font-weight: 500;
}

@media (max-width: 768px) {
  .api-status-indicator {
    padding: 0.25rem;
    width: 30px;
    height: 30px;
    justify-content: center;
    border-radius: 50%;
  }

  .status-text {
    display: none;
  }
}
</style>