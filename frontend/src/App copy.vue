<template>
  <div>
    <template v-if="shouldShowLayout">
      <AppHeader 
        :is-collapsed="isCollapsed" 
        :is-mobile="isMobile" 
        @toggle-sidebar="toggleSidebar" 
      />
      <div class="main-container">
        <AppSidebar 
          :is-collapsed="isCollapsed" 
          :is-mobile="isMobile" 
          @toggle-sidebar="toggleSidebar" 
        />
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
    
    <Toast 
      position="top-right" 
      :closeButton="false"
      infoIcon="pi pi-info-circle"
      warnIcon="pi pi-exclamation-triangle"
      errorIcon="pi pi-times-circle"
      successIcon="pi pi-check-circle"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import AppHeader from './components/layout/AppHeader.vue';
import AppFooter from './components/layout/AppFooter.vue';
import AppSidebar from './components/layout/AppSidebar.vue';
import OnlineStatus from '@/components/ui/OnlineStatus.vue';

const route = useRoute();
const isMobile = ref(false);
const isCollapsed = ref(false);

const shouldShowLayout = computed(() => {
  const isAuthenticated = localStorage.getItem('auth_token');
  if (route.meta.hideLayout) return false;
  return (route.meta.requiresAuth && isAuthenticated) || (!route.meta.public && isAuthenticated);
});

const updateCssVariables = () => {
  document.documentElement.style.setProperty('--sidebar-width', isCollapsed.value ? '0px' : '250px');
};

const checkScreenSize = () => {
  isMobile.value = window.innerWidth < 768;
  isCollapsed.value = isMobile.value;
};

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
};

onMounted(() => {
  checkScreenSize();
  updateCssVariables();
  window.addEventListener('resize', checkScreenSize);
});

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize);
});

watch(isCollapsed, updateCssVariables);
</script>

<style>
:root {
  --sidebar-width: 250px;
  --transition-speed: 0.3s;
}

html, body, #app{
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: #F4F7FA;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: var(--sidebar-width);
  transition: margin-left var(--transition-speed);
}

.content-area {
  flex: 1;
  padding: 20px;
}

@media (max-width: 768px) {
  .content-wrapper {
    margin-left: 0;
  }
}
</style>