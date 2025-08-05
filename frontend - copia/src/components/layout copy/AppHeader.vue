<template>
  <header id="header" class="header fixed-top">
    <div class="container-fluid d-flex align-items-center justify-content-between">
      <!-- Botones de toggle -->
      <button v-if="!isMobile" class="toggle-btn" @click="toggleSidebar">
        <i class="fas fa-bars"></i>
      </button>
      <button v-if="isMobile" class="mobile-toggle-btn" @click="toggleSidebar">
        <i class="fas fa-bars"></i>
      </button>

      <!-- Menú de usuario -->
      <nav class="header-nav ms-auto">
        <ul class="d-flex align-items-center gap-3">
          <li class="nav-item dropdown">
            <a class="nav-profile d-flex align-items-center" href="#" @click.prevent="toggleDropdown">
              <div class="avatar-container">
<img :src="userStore.effectiveUserImage" 
     :key="userStore.effectiveUserImage" 
     @error="userStore.setImageError(true)" 
     alt="Profile" 
     class="avatar-img">              </div>
              <span class="user-name">{{ userStore.fullName }}</span>
              <i class="fas fa-chevron-down ms-2 dropdown-arrow"></i>
            </a>

            <!-- Dropdown menu -->
            <div v-if="showDropdown" class="dropdown-menu" @click.stop>
              <div class="dropdown-header">
                <div class="avatar-container-lg">
                  <img :src="userStore.effectiveUserImage" alt="Profile" class="avatar-img" @error="userStore.setImageError(true)">
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
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { api } from '@/components/services/Axios'

const router = useRouter()
const userStore = useUserStore()
const showDropdown = ref(false)

// Props y emits
defineProps({
  isCollapsed: Boolean,
  isMobile: Boolean
})
const emit = defineEmits(['toggle-sidebar'])

// Métodos
const toggleSidebar = () => emit('toggle-sidebar')
const toggleDropdown = () => showDropdown.value = !showDropdown.value

const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.dropdown-menu')
  const profileBtn = document.querySelector('.nav-profile')

  if (dropdown && profileBtn && !dropdown.contains(event.target) && !profileBtn.contains(event.target)) {
    showDropdown.value = false
  }
}

const logout = async () => {
  try {
    const refreshToken = localStorage.getItem('refreshToken')
    if (refreshToken) {
      await api.post('user/logout/', { refresh: refreshToken })
    }
  } catch (error) {
    console.error('Error al cerrar sesión:', error)
  } finally {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('refreshToken')
    router.push('/login')
  }
}

// Lifecycle hooks
onMounted(() => {
  userStore.fetchUserProfile()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Estilos optimizados */
.header {
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  height: 70px;
  left: var(--sidebar-width, 250px);
  width: calc(100% - var(--sidebar-width, 250px));
  padding: 0 1rem;
  z-index: 1000;
  background: white;
  position: fixed;
  top: 0;
}

.toggle-btn, .mobile-toggle-btn {
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

.toggle-btn { margin-right: 10px; }
.toggle-btn:hover { background: rgba(255, 255, 255, 0.2); transform: scale(1.05); }

.nav-profile {
  text-decoration: none;
  color: #364257;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  transition: all 0.3s ease;
}
.nav-profile:hover { background: rgba(0, 0, 0, 0.05); }

.avatar-container {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(0, 0, 0, 0.1);
}
.avatar-img { width: 100%; height: 100%; object-fit: cover; }

.user-name {
  margin-left: 10px;
  font-weight: 500;
  color: #364257;
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

.user-info { flex: 1; }
.user-fullname { font-weight: 600; color: #333; margin-bottom: 3px; }
.user-email { font-size: 0.85rem; color: #6c757d; }

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  color: #495057;
  text-decoration: none;
  transition: all 0.2s;
}
.dropdown-item:hover { background: #f8f9fa; color: #3F4D67; }
.dropdown-item i { margin-right: 10px; width: 20px; text-align: center; color: #6c757d; }

.logout-item { color: #dc3545; }
.logout-item:hover { background: rgba(220, 53, 69, 0.1); }

.dropdown-arrow {
  transition: transform 0.3s;
  font-size: 0.8rem;
}
.nav-profile:hover .dropdown-arrow { transform: rotate(180deg); }

/* Responsive */
@media (max-width: 768px) {
  .header {
    left: 0;
    width: 100% !important;
    padding: 0 0.5rem;
  }
  .toggle-btn { display: none; }
  .mobile-toggle-btn { display: flex; }
  .user-name { 
    font-size: 0.8rem;
    max-width: 100px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .dropdown-menu { right: 10px; width: 260px; }
}
</style>