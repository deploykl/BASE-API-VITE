<template>
  <header id="header" class="header fixed-top">
    <div class="container-fluid d-flex align-items-center justify-content-between">
      <div class="d-flex align-items-center gap-3">
        <button v-if="!isMobile" class="toggle-btn" @click="toggleSidebar">
          <i :class="isCollapsed ? 'fas fa-bars' : 'fas fa-bars'"></i>
        </button>

        <button v-if="isMobile" class="mobile-toggle-btn" @click="toggleSidebar">
          <i class="fas fa-bars"></i>
        </button>

        <div class="connection-status me-2" :class="{ 'online': isOnline, 'offline': !isOnline }">
          <i :class="isOnline ? 'fas fa-wifi' : 'fas fa-wifi-slash'"></i>
          <span class="status-text">{{ isOnline ? 'Online' : 'Offline' }}</span>
        </div>
      </div>
      <!-- Indicador de conexión al API -->
      <div class="connection-status" :class="{
        'online': isApiConnected === true,
        'offline': isApiConnected === false,
        'checking': isApiConnected === null || isCheckingApi
      }">
        <i :class="{
          'fas fa-server': isApiConnected === true,
          'fas fa-server-slash': isApiConnected === false,
          'fas fa-circle-notch fa-spin': isApiConnected === null || isCheckingApi
        }"></i>
        <span class="status-text">
          <template v-if="isCheckingApi">Verificando API...</template>
          <template v-else-if="isApiConnected === true">API Conectado</template>
          <template v-else-if="isApiConnected === false">API Desconectado</template>
          <template v-else>Estado API</template>
        </span>
      </div>
      <nav class="header-nav ms-auto">
        <ul class="d-flex align-items-center gap-3">
          <li class="nav-item dropdown">
            <a class="nav-profile d-flex align-items-center" href="#" @click.prevent="toggleDropdown">
              <div class="avatar-container">
                <img :src="effectiveUserImage" @error="handleImageError" alt="Profile" class="avatar-img">
              </div>
              <span class="user-name">{{ userData.username }}</span>
              <i class="fas fa-chevron-down ms-2 dropdown-arrow"></i>
            </a>

            <div v-if="showDropdown" class="dropdown-menu">
              <div class="dropdown-header">
                <div class="avatar-container-lg">
                  <img :src="effectiveUserImage" alt="Profile" class="avatar-img" @error="handleImageError">
                </div>
                <div class="user-info">
                  <div class="user-fullname">{{ fullName }}</div>
                  <div class="user-email">{{ userData.email }}</div>
                </div>
              </div>
              <div class="dropdown-divider"></div>
              <router-link to="/settings" class="dropdown-item">
                <i class="fas fa-cog"></i> Configuración
              </router-link>
              <router-link to="/change-password" class="dropdown-item">
                <i class="fas fa-key"></i> Cambiar contraseña
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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '@/components/services/Axios';
import defaultAvatar from '@/assets/img/header/default-avatar.png';
import { useApiConnection } from '@/components/utils/ApiConnection'; // Importa el composable

const { isApiConnected, isLoading: isCheckingApi } = useApiConnection()
// Props
const props = defineProps({
  isCollapsed: Boolean,
  isMobile: Boolean
});

// Emits
const emit = defineEmits(['toggle-sidebar']);

// Router
const router = useRouter();

// Estado del usuario
const userData = ref({
  firstName: '',
  lastName: '',
  email: '',
  image: '',
  username: ''
});

// Estado de la UI
const isOnline = ref(navigator.onLine);
const imageError = ref(false);
const showDropdown = ref(false);
const imgServerURL = process.env.VUE_APP_IMG_SERVER;

// Computed properties
const effectiveUserImage = computed(() => {
  return imageError.value || !userData.value.image ? defaultAvatar : userData.value.image;
});

const fullName = computed(() => {
  return `${userData.value.firstName} ${userData.value.lastName}`.trim();
});

// Métodos
const toggleSidebar = () => {
  emit('toggle-sidebar');
};

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const handleImageError = () => {
  imageError.value = true;
};

const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.dropdown-menu');
  const profileBtn = document.querySelector('.nav-profile');

  if (dropdown && profileBtn &&
    !dropdown.contains(event.target) &&
    !profileBtn.contains(event.target)) {
    showDropdown.value = false;
  }
};

const updateOnlineStatus = async () => {
  try {
    // Verificación más robusta que solo navigator.onLine
    const response = await fetch('https://www.google.com', { 
      method: 'HEAD',
      cache: 'no-store',
      mode: 'no-cors'
    });
    isOnline.value = true;
  } catch (error) {
    isOnline.value = false;
  }
};

const checkConnection = async () => {
  try {
    await fetch('https://httpbin.org/get', { method: 'HEAD' });
    isOnline.value = true;
  } catch (error) {
    isOnline.value = false;
  }
};

const fetchUserProfile = async () => {
  const accessToken = localStorage.getItem('auth_token');
  if (!accessToken) return;

  try {
    const response = await api.get('user/profile/', {
      headers: { Authorization: `Bearer ${accessToken}` }
    });

    const { first_name, last_name, email, image, username } = response.data;

    userData.value = {
      firstName: first_name || '',
      lastName: last_name || '',
      email: email || '',
      username: username || '',
      image: image ? buildImageUrl(image) : defaultAvatar
    };

    imageError.value = false;
  } catch (error) {
    console.error('Error al obtener perfil:', error);
    userData.value.image = defaultAvatar;
  }
};

const buildImageUrl = (imagePath) => {
  if (!imagePath) return defaultAvatar;
  if (imagePath.startsWith('http')) return imagePath;
  return `${imgServerURL.replace(/\/+$/, '')}/${imagePath.replace(/^\/+/, '')}`;
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
    // Limpiar almacenamiento
    localStorage.removeItem('auth_token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('is_superuser');
    localStorage.removeItem('is_staff');
    router.push('/login');
  }
};

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  document.addEventListener('click', handleClickOutside);
  fetchUserProfile();
  checkConnection();
});

onUnmounted(() => {
  window.removeEventListener('online', updateOnlineStatus);
  window.removeEventListener('offline', updateOnlineStatus);
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
/* Base Styles */
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

.toggle-btn {
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
  margin-right: 10px;
}

.toggle-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

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

.container-fluid {
  height: 100%;
}

/* Reset list styles */
.header-nav ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: 0;
}

.header-nav li {
  list-style: none;
  display: inline-block;
}

/* User Profile */
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

.avatar-container {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(0, 0, 0, 0.1);
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
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

/* Estilos para el indicador de conexión */
.connection-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.connection-status.online {
  background-color: rgba(40, 167, 69, 0.15);
  color: #28a745;
}

.connection-status.offline {
  background-color: rgba(220, 53, 69, 0.15);
  color: #dc3545;
}

.status-text {
  font-weight: 500;
}

/* Dropdown styles */
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
}

.dropdown-header {
  display: flex;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
}

.avatar-container-lg {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(0, 0, 0, 0.1);
  margin-right: 12px;
}

.user-info {
  flex: 1;
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

/* Mobile adjustments */
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

  .status-text {
    display: none;
  }

  .connection-status {
    padding: 0.25rem;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    justify-content: center;
  }

  .user-name {
    font-size: 0.8rem;
    margin-left: 5px;
    max-width: 100px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .dropdown-menu {
    right: 10px;
    width: 260px;
  }

  .user-name {
    display: none;
  }

  .dropdown-arrow {
    display: none;
  }

  .avatar-container {
    width: 32px;
    height: 32px;
  }
}

.connection-status {
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

/* Internet status */
.connection-status.online:not(.checking) {
  background-color: rgba(40, 167, 69, 0.15);
  color: #28a745;
  border: 1px solid #28a745;
}

.connection-status.offline:not(.checking) {
  background-color: rgba(220, 53, 69, 0.15);
  color: #dc3545;
  border: 1px solid #dc3545;
}

/* API status */
.connection-status.checking {
  background-color: rgba(255, 193, 7, 0.15);
  color: #ffc107;
  border: 1px solid #ffc107;
}

/* Iconos */
.connection-status i {
  font-size: 0.9rem;
}

.fa-spin {
  animation: fa-spin 2s infinite linear;
}

@keyframes fa-spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(359deg);
  }
}

@media (max-width: 768px) {
  .connection-status {
    padding: 0.25rem;
    width: 30px;
    height: 30px;
    justify-content: center;
    border-radius: 50%;
  }

  .connection-status .status-text {
    display: none;
  }

  .connection-status i {
    margin: 0;
  }
}
</style>