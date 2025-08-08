<template>
  <div class="app-layout">
    <template v-if="shouldShowLayout">
      <AppHeader :is-collapsed="isCollapsed" :is-mobile="isMobile" @toggle-sidebar="toggleSidebar" />
      <div class="main-container">
        <AppSidebar :is-collapsed="isCollapsed" :is-mobile="isMobile" @toggle-collapse="toggleSidebar" />
        <div class="content-wrapper">
          <main class="content-area">
            <router-view />
          </main>
              <OnlineStatus v-if="shouldShowLayout" />

          <AppFooter />
        </div>
      </div>
    </template>
    <template v-else>
      <router-view />
    </template>
  </div>
      <!-- Componente de usuarios en línea -->
<Toast 
    position="top-right" 
    :closeButton="false"
    infoIcon="pi pi-info-circle"
    warnIcon="pi pi-exclamation-triangle"
    errorIcon="pi pi-times-circle"
    successIcon="pi pi-check-circle"
  />
  </template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'
import AppSidebar from './components/layout/AppSidebar.vue'
import OnlineStatus from '@/components/ui/OnlineStatus.vue'

const route = useRoute()
const isCollapsed = ref(false)
const isMobile = ref(false)

const shouldShowLayout = computed(() => {
  const isAuthenticated = localStorage.getItem('auth_token');

  // Si la ruta especifica hideLayout, no mostrar el layout completo
  if (route.meta.hideLayout) {
    return false;
  }

  // Mostrar layout completo si:
  // 1. La ruta requiere autenticación Y el usuario está autenticado
  // 2. O si es una ruta que no es pública (por defecto mostramos layout)
  return (route.meta.requiresAuth && isAuthenticated) ||
    (!route.meta.public && isAuthenticated);
});

const updateCssVariables = () => {
  const width = isCollapsed.value ? '0px' : '250px'
  document.documentElement.style.setProperty('--sidebar-width', width)
}

const checkScreenSize = () => {
  isMobile.value = window.innerWidth < 768
  // Solo establecer el estado inicial si no ha sido modificado por el usuario
  if (isMobile.value && !localStorage.getItem('sidebar-state-changed')) {
    isCollapsed.value = true
  }
  updateCssVariables()
}

// Función mejorada para alternar el sidebar
const toggleSidebar = (forceState = null) => {
  if (forceState !== null) {
    isCollapsed.value = forceState
  } else {
    isCollapsed.value = !isCollapsed.value
  }
  localStorage.setItem('sidebar-state-changed', 'true')
  updateCssVariables()
}

watch(isCollapsed, updateCssVariables)

onMounted(() => {
  checkScreenSize()
  window.addEventListener('resize', checkScreenSize)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize)
})

</script>

<style>
:root {
  --sidebar-width: 250px;
  --transition-speed: 0.3s;
}

html,
body,
#app,
.app-layout {
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: #F4F7FA;

}

.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  /* Usar viewport height */
}

.main-container {
  display: flex;
  flex: 1;
  padding: 15px;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-left: var(--sidebar-width);
}

.content-area {
  flex: 1;
  padding: 15px;
  transition: margin-left var(--transition-speed) ease;
}

@media (max-width: 768px) {
  .content-wrapper {
    margin-left: 0;
  }
}

.home {
  background-color: #ffffff;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}
</style>