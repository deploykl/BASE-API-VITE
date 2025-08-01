<template>
  <div 
    class="network-status-indicator"
    :class="statusClass"
    :title="tooltipText"
    @click="forceNetworkCheck"
  >
    <i :class="iconClass"></i>
    <span v-if="!isMobile" class="status-text">{{ statusText }}</span>
    <span v-if="showLastCheck && lastNetworkCheck" class="last-check">
      {{ formattedLastCheck }}
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  isOnline: Boolean,
  isMobile: Boolean,
  showLastCheck: {
    type: Boolean,
    default: false
  },
  lastNetworkCheck: {  // This must match what's passed from parent
    type: Date,
    default: null
  },
  isCheckingNetwork: {
    type: Boolean,
    default: false
  },
  isCheckingNetwork: {  // Ahora usa esta propiedad específica
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['force-check'])

const forceNetworkCheck = () => {
  emit('force-check')
}

const statusClass = computed(() => ({
  'online': props.isOnline,
  'offline': !props.isOnline,
  'checking': props.isCheckingNetwork,  // Clase para estado de verificación
  'clickable': true
}))

const iconClass = computed(() => ({
  'fas': true,
  'fa-wifi': props.isOnline && !props.isCheckingNetwork,
  'fa-wifi-slash': !props.isOnline && !props.isCheckingNetwork,
  'fa-circle-notch fa-spin': props.isCheckingNetwork  // Icono de carga cuando está verificando
}))

const statusText = computed(() => {
  if (props.isCheckingNetwork) return 'Verificando...'
  return props.isOnline ? 'Online' : 'Offline'
})

const tooltipText = computed(() => {
  if (props.isCheckingNetwork) return 'Verificando conexión a Internet...'
  return props.isOnline ? 
    'Conexión a Internet estable. Click para verificar' : 
    'Sin conexión a Internet. Click para verificar'
})

const formattedLastCheck = computed(() => {
  if (!props.lastNetworkCheck) return ''
  const now = new Date()
  const diff = Math.floor((now - props.lastNetworkCheck) / 1000)
  
  if (diff < 60) return `Hace ${diff}s`
  if (diff < 3600) return `Hace ${Math.floor(diff/60)}m`
  return `Hace ${Math.floor(diff/3600)}h`
})
</script>

<style scoped>
.network-status-indicator {
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.network-status-indicator.online {
  background-color: rgba(40, 167, 69, 0.15);
  color: #28a745;
  border: 1px solid #28a745;
}

.network-status-indicator.offline {
  background-color: rgba(220, 53, 69, 0.15);
  color: #dc3545;
  border: 1px solid #dc3545;
}

.network-status-indicator.checking {
  background-color: rgba(255, 193, 7, 0.15);
  color: #ffc107;
  border: 1px solid #ffc107;
}

.status-text {
  font-weight: 500;
}

.last-check {
  font-size: 0.7rem;
  opacity: 0.8;
  margin-left: 0.3rem;
}

@media (max-width: 768px) {
  .network-status-indicator {
    padding: 0.25rem;
    width: 30px;
    height: 30px;
    justify-content: center;
    border-radius: 50%;
  }

  .status-text, .last-check {
    display: none;
  }
}
</style>