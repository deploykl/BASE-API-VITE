<template>
  <header id="header" class="header fixed-top">
    <div class="container-fluid d-flex align-items-center justify-content-between">
      <!-- Botones de toggle -->
      <div class="d-flex align-items-center gap-3">
        <button v-if="!isMobile" class="toggle-btn" @click="toggleSidebar">
          <i class="fas fa-bars"></i>
        </button>
        <button v-if="isMobile" class="mobile-toggle-btn" @click="toggleSidebar">
          <i class="fas fa-bars"></i>
        </button>
      </div>

      <!-- Indicadores de conexión -->
      <ConnectionManager
        v-slot="{ isOnline, isApiConnected, isCheckingApi, isCheckingNetwork, lastApiCheck, lastNetworkChange, checkApiConnection, checkNetworkConnection }">
        <div class="connection-indicators">
          <NetworkStatusIndicator 
            :isOnline="isOnline" 
            :isMobile="isMobile" 
            :lastNetworkCheck="lastNetworkChange"
            :isCheckingNetwork="isCheckingNetwork" 
            @force-check="checkNetworkConnection" 
          />
          <ApiStatusIndicator 
            :isApiConnected="isApiConnected" 
            :isCheckingApi="isCheckingApi" 
            :isMobile="isMobile"
            @check-api="checkApiConnection" 
          />
        </div>
      </ConnectionManager>

      <!-- Menú de usuario -->
      <nav class="header-nav ms-auto">
        <ul class="d-flex align-items-center gap-3">
          <li class="nav-item dropdown">
            <a class="nav-profile d-flex align-items-center" href="#" @click.prevent="toggleDropdown">
              <div class="avatar-container">
                <img 
                  :src="userStore.effectiveUserImage" 
                  alt="Foto de perfil" 
                  class="avatar-img" 
                  @error="userStore.setImageError(true)"
                >
              </div>
              <span class="user-name">{{ userStore.userData.username }}</span>
              <i class="fas fa-chevron-down ms-2 dropdown-arrow"></i>
            </a>

            <!-- Dropdown Menu -->
            <div 
              v-if="showDropdown" 
              class="dropdown-menu"
              ref="dropdownMenu"
              @mouseleave="handleMouseLeave"
              @focusout="handleFocusOut"
              tabindex="-1"
            >
              <div class="dropdown-header">
                <div class="avatar-container-lg">
                  <img 
                    :src="userStore.effectiveUserImage" 
                    alt="Foto de perfil" 
                    class="avatar-img" 
                    @error="userStore.setImageError(true)"
                  >
                </div>
                <div class="user-info">
                  <div class="user-fullname">{{ userStore.fullName }}</div>
                  <div class="user-email">{{ userStore.userData.email }}</div>
                </div>
              </div>

              <div class="dropdown-divider"></div>

              <router-link to="/perfil" class="dropdown-item">
                <i class="fas fa-cog"></i> Perfil
              </router-link>

              <router-link to="/change-password" class="dropdown-item">
                <i class="fas fa-key"></i> Cambiar contraseña
              </router-link>

              <router-link to="/settings" class="dropdown-item">
                <i class="fas fa-cog"></i> Configuración
              </router-link>

              <div class="dropdown-divider"></div>

              <a href="#" class="dropdown-item logout-item" @click.prevent="logout">
                <i class="fas fa-sign-out-alt"></i> Cerrar sesión
              </a>
            </div>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '@/components/services/Axios';
import { useUserStore } from '@/store/user';
import ConnectionManager from '@/components/connection/ConnectionManager';
import NetworkStatusIndicator from '@/components/connection/NetworkStatusIndicator';
import ApiStatusIndicator from '@/components/connection/ApiStatusIndicator';

// Props
const props = defineProps({
  isCollapsed: Boolean,
  isMobile: Boolean
});

// Emits
const emit = defineEmits(['toggle-sidebar']);

// Refs
const dropdownMenu = ref(null);
const isOnline = ref(navigator.onLine);
const showDropdown = ref(false);

// Stores y router
const router = useRouter();
const userStore = useUserStore();

// Methods
const toggleSidebar = () => emit('toggle-sidebar');

const toggleDropdown = () => showDropdown.value = !showDropdown.value;

const handleMouseLeave = () => {
  setTimeout(() => {
    if (showDropdown.value && !dropdownMenu.value.contains(document.activeElement)) {
      showDropdown.value = false;
    }
  }, 100);
};

const handleFocusOut = (event) => {
  if (dropdownMenu.value && !dropdownMenu.value.contains(event.relatedTarget)) {
    showDropdown.value = false;
  }
};

const handleClickOutside = (event) => {
  const profileBtn = document.querySelector('.nav-profile');
  
  if (dropdownMenu.value && profileBtn &&
    !dropdownMenu.value.contains(event.target) &&
    !profileBtn.contains(event.target)) {
    showDropdown.value = false;
  }
};

const updateOnlineStatus = async () => {
  try {
    await fetch('https://www.google.com', { method: 'HEAD', cache: 'no-store', mode: 'no-cors' });
    isOnline.value = true;
  } catch {
    isOnline.value = false;
  }
};

const checkConnection = async () => {
  try {
    await fetch('https://httpbin.org/get', { method: 'HEAD' });
    isOnline.value = true;
  } catch {
    isOnline.value = false;
  }
};

const logout = async () => {
  try {
    const refreshToken = localStorage.getItem('refreshToken');
    if (refreshToken) {
      await api.post('user/logout/', { refresh: refreshToken });
    }
  } catch (error) {
    console.error('Error al cerrar sesión:', error);
  } finally {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('is_superuser');
    localStorage.removeItem('is_staff');
    router.push('/');
  }
};

// Lifecycle hooks
onMounted(() => {
  userStore.fetchUserProfile();
  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  document.addEventListener('click', handleClickOutside);
  checkConnection();
});

onUnmounted(() => {
  window.removeEventListener('online', updateOnlineStatus);
  window.removeEventListener('offline', updateOnlineStatus);
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
/* Estilos se mantienen igual que en tu versión anterior */
.header {
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  height: 70px;
  left: var(--sidebar-width, 250px);
  width: calc(100% - var(--sidebar-width, 250px));
  right: 0;
  padding: 0 1rem;
  transition: all 0.3s ease;
  z-index: 1000;
  border-bottom-right-radius: 15px;
  position: relative;
  background: white;
}

.container-fluid {
  height: 100%;
}

.toggle-btn,
.mobile-toggle-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #364257;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-btn {
  margin-right: 10px;
}

.toggle-btn:hover,
.mobile-toggle-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.header-nav ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: 0;
}

.header-nav li {
  list-style: none;
  display: inline-block;
}

.nav-profile {
  text-decoration: none;
  color: #364257;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 50px;
}

.nav-profile:hover {
  background: rgba(0, 0, 0, 0.05);
}

.avatar-container,
.avatar-container-lg {
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(0, 0, 0, 0.1);
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-container {
  width: 40px;
  height: 40px;
}

.avatar-container-lg {
  width: 50px;
  height: 50px;
  margin-right: 12px;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  margin-left: 10px;
  font-weight: 500;
  color: #364257;
}

.user-fullname {
  font-weight: 600;
  color: #333;
  margin-bottom: 3px;
}

.user-email {
  font-size: 0.85rem;
  color: #6c757d;
}

.dropdown-menu {
  position: absolute;
  right: 15px;
  top: 60px;
  width: 280px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
  z-index: 1001;
  padding: 0;
  overflow: hidden;
  display: block;
  outline: none;
  pointer-events: auto;
}

.dropdown-header {
  display: flex;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
}

.dropdown-divider {
  height: 1px;
  background: #e9ecef;
  margin: 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  color: #495057;
  text-decoration: none;
  transition: all 0.2s;
  pointer-events: auto;
}

.dropdown-item i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
  color: #6c757d;
}

.dropdown-item:hover {
  background: #f8f9fa;
  color: #3F4D67;
}

.dropdown-item:hover i {
  color: #3F4D67;
}

.logout-item {
  color: #dc3545;
}

.logout-item:hover {
  background: rgba(220, 53, 69, 0.1);
}

.dropdown-arrow {
  transition: transform 0.3s;
  font-size: 0.8rem;
}

.nav-profile:hover .dropdown-arrow {
  transform: rotate(180deg);
}

.connection-indicators {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.fa-spin {
  animation: fa-spin 2s infinite linear;
}

@keyframes fa-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(359deg); }
}

@media (max-width: 768px) {
  .header {
    left: 0;
    padding: 0 0.5rem;
    width: 100% !important;
  }

  .mobile-toggle-btn {
    display: flex;
  }

  .toggle-btn {
    display: none;
  }

  .status-text,
  .user-name,
  .dropdown-arrow {
    display: none;
  }

  .connection-status {
    padding: 0.25rem;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    justify-content: center;
  }

  .connection-status i {
    margin: 0;
  }

  .dropdown-menu {
    right: 10px;
    width: 260px;
  }

  .avatar-container {
    width: 32px;
    height: 32px;
  }
}
</style>