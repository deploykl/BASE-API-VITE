<template>
  <div v-if="isMobile && !isCollapsed" class="sidebar-overlay" @click="toggleSidebar"></div>
  <aside :class="['sidebar', { 'collapsed': isCollapsed, 'mobile-hidden': isMobile && isCollapsed }]">
    <div class="sidebar-header">
      <img src="@/assets/logo.png" alt="Logo" class="logo-img">
      <span class="logo-text" v-if="!isCollapsed || isMobile">LOGO NAME</span>
    </div>

    <nav class="sidebar-menu">
      <ul>
        <li v-for="(item, index) in filteredMenuItems" :key="index" :class="{
          'active': activeMenu === index,
          'menu-header': item.isHeader,
          'menu-item-wrapper': !item.isHeader
        }">
          <!-- Renderizado de títulos/categorías -->
          <div v-if="item.isHeader" class="menu-header-title">
            <span v-if="!isCollapsed || isMobile">{{ item.title }}</span>
          </div>

          <!-- Renderizado de items normales -->
          <template v-else>
            <router-link v-if="!item.submenu" :to="item.path" class="menu-item" @click="() => toggleSubmenu(index)">
              <div class="menu-content">
                <i :class="['fas', item.icon]"></i>
                <span v-if="!isCollapsed || isMobile">{{ item.title }}</span>
              </div>
            </router-link>

            <div v-else class="menu-item" @click="toggleSubmenu(index)">
              <div class="menu-content">
                <i :class="['fas', item.icon]"></i>
                <span v-if="!isCollapsed || isMobile">{{ item.title }}</span>
              </div>
              <i v-if="item.submenu && (!isCollapsed || isMobile)"
                :class="['fas', 'submenu-arrow', isSubmenuOpen(index) ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
            </div>

            <transition name="slide">
              <ul v-if="item.submenu && isSubmenuOpen(index) && (!isCollapsed || isMobile)" class="submenu">
                <li v-for="(subItem, subIndex) in item.submenu" :key="subIndex"
                  :class="{ 'active': activeSubmenu === `${index}-${subIndex}` }">
                  <router-link :to="subItem.path" class="submenu-item" @click="handleSubmenuClick(index, subIndex)">
                    <i :class="['fas', subItem.icon]"></i>
                    <span>{{ subItem.title }}</span>
                  </router-link>
                </li>
              </ul>
            </transition>
          </template>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const emit = defineEmits(['toggle-collapse'])

// Estado del sidebar
const isCollapsed = ref(false)
const isMobile = ref(false)
const activeMenu = ref(null)
const activeSubmenu = ref(null)
const openSubmenus = ref([])

const props = defineProps({
  isCollapsed: {
    type: Boolean,
    default: false
  },
  isMobile: {
    type: Boolean,
    default: false
  }
})

// Función para alternar el sidebar
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
  emit('toggle-collapse', isCollapsed.value)
  emit('update:isCollapsed', isCollapsed.value)
}

// Obtener módulos del usuario desde localStorage
const userModulos = computed(() => {
  const modulos = localStorage.getItem('user_modulos')
  return modulos ? JSON.parse(modulos) : []
})

const isSuperuser = computed(() => {
  return localStorage.getItem('is_superuser') === 'true'
})

// Verificar si el usuario tiene acceso a un módulo específico
const hasModuleAccess = (moduleName) => {
  return isSuperuser.value || userModulos.value.includes(moduleName)
}

const filteredMenuItems = computed(() => {
  return menuItems.value.filter(item => {
    if (item.isHeader) return true;
    
    // Si no requiere módulo específico, mostrarlo
    if (!item.requiredModule) return true;
    
    // Verificar si el usuario tiene acceso
    return hasModuleAccess(item.requiredModule);
  });
});

// Datos del menú
const menuItems = ref([
  {
    title: "Principal",
    isHeader: true
  },
  {
    title: 'Dashboard',
    icon: 'fa-tachometer-alt',
    path: '/dashboard',
    submenu: null
  },
  {
    title: 'Usuarios',
    icon: 'fa-users',
    path: '/user/create',
    submenu: null,
    requiredModule: 'Usuarios' // Especificar módulo requerido
  },
  {
    title: "Pacientes",
    isHeader: true
  },
  {
    title: 'Emergencia',
    icon: 'fa-user-injured',
    path: '/patients',
    submenu: [
      { title: 'Fichas de Monitoreo', icon: 'fa-chart-bar', path: '/fichas' },
      { title: 'Matriz de compromiso', icon: 'fa-book', path: '/matriz-list' },
    ]
  },
  {
    title: "Reportes",
    isHeader: true
  },
  {
    title: 'Fichas de Monitoreo',
    icon: 'fa-chart-bar',
    path: '/fichas',
    submenu: null
  },
  {
    title: 'Matriz de compromiso',
    icon: 'fa-book',
    path: '/matriz-list',
    submenu: null
  },
  {
    title: 'Alertas',
    icon: 'fa-bell',
    path: '/alertas',
    submenu: null
  },
    {
    title: 'Presupuesto',
    icon: 'fa-bell',
    path: '/presupuesto',
    submenu: null
  }
])

const toggleSubmenu = (index) => {
  if (filteredMenuItems.value[index]?.submenu) {
    const submenuIndex = openSubmenus.value.indexOf(index)
    if (submenuIndex === -1) {
      openSubmenus.value.push(index)
    } else {
      openSubmenus.value.splice(submenuIndex, 1)
    }
  } else {
    activeMenu.value = index
    activeSubmenu.value = null
    if (isMobile.value) {
      isCollapsed.value = true
    }
  }
}

const isSubmenuOpen = (index) => {
  return openSubmenus.value.includes(index)
}

const setActiveSubmenu = (menuIndex, submenuIndex) => {
  activeMenu.value = menuIndex
  activeSubmenu.value = `${menuIndex}-${submenuIndex}`
}

const handleSubmenuClick = (menuIndex, submenuIndex) => {
  setActiveSubmenu(menuIndex, submenuIndex)
  if (isMobile.value) {
    isCollapsed.value = true
  }
}

// Configuración responsive
const checkScreenSize = () => {
  const width = window.innerWidth
  isMobile.value = width < 768
  if (isMobile.value) {
    isCollapsed.value = true
  } else {
    isCollapsed.value = false
  }
}

onMounted(() => {
  checkScreenSize()
  window.addEventListener('resize', checkScreenSize)

  // Marcar menú activo según la ruta actual
  const currentPath = route.path
  filteredMenuItems.value.forEach((item, index) => {
    if (item.path === currentPath) {
      activeMenu.value = index
    } else if (item.submenu) {
      item.submenu.forEach((subItem, subIndex) => {
        if (subItem.path === currentPath) {
          activeMenu.value = index
          activeSubmenu.value = `${index}-${subIndex}`
          if (!openSubmenus.value.includes(index)) {
            openSubmenus.value.push(index)
          }
        }
      })
    }
  })
})

// Sincronizamos con los cambios de props
watch(() => props.isCollapsed, (newVal) => {
  isCollapsed.value = newVal
})
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  background: #364257;
  color: white;
  transition: all 0.3s ease;
  z-index: 1001;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  border-bottom-right-radius: 15px;
  margin: 0;
  padding: 0;
  font-size: 0.9rem;
}

.sidebar.collapsed {
  transform: translateX(-100%);
}

.sidebar-overlay {
  position: fixed;
  top: 70px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  backdrop-filter: blur(2px);
}

/* Header del sidebar */
.sidebar-header {
  display: flex;
  align-items: center;
  padding: 20px;
  gap: 10px;
  height: 70px;
  min-height: 70px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
  cursor: pointer;
  position: relative;
}

.logo-img {
  width: 32px;
  height: 32px;
  object-fit: contain;
  transition: transform 0.3s ease;
}



/* Estilos para móvil */
@media (max-width: 768px) {
  .sidebar {
    width: 250px;
    transform: translateX(-100%);
  }

  .sidebar:not(.collapsed) {
    transform: translateX(0);
  }
}

.sidebar-header:hover .logo-img {
  transform: scale(1.1);
}

.logo-text {
  font-weight: 600;
  font-size: 1.2rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.3s ease;
}

.logo-tooltip {
  position: absolute;
  left: 100%;
  top: 50%;
  transform: translateY(-50%);
  background: #364257;
  padding: 8px 12px;
  border-radius: 0 4px 4px 0;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
  white-space: nowrap;
  margin-left: 10px;
  z-index: 1002;
}

/* Títulos de categoría */
.menu-header {
  padding: 15px 20px 5px;
  margin-top: 10px;
  position: relative;
  cursor: default;
}

.menu-header:not(:first-child) {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.menu-header-title {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.menu-header-title i {
  font-size: 0.9rem;
}

/* Ítems de menú */
.menu-item-wrapper {
  margin-bottom: 2px;
  position: relative;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  color: white;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.menu-content {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.menu-item i {
  min-width: 20px;
  text-align: center;
  transition: transform 0.3s ease;
}

.menu-item:hover i {
  transform: scale(1.1);
}

.menu-item span {
  white-space: nowrap;
  transition: all 0.3s ease;
}


/* Submenú */
.submenu-arrow {
  transition: transform 0.3s ease;
}

.submenu {
  background: rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.submenu-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px 20px 10px 50px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
}

.submenu-item::before {
  content: '';
  position: absolute;
  left: 30px;
  top: 0;
  height: 100%;
  width: 2px;
  background: rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.active .submenu-item::before {
  background: white;
}

.submenu-item:hover {
  background: #596170;
  color: white;
}

.submenu-item:hover::before {
  background: rgba(255, 255, 255, 0.6);
}

.submenu-item i {
  font-size: 0.8rem;
}

/* Estados activos */
.active>.menu-item {
  background: rgba(255, 255, 255, 0.15);
  border-left: 3px solid white;
}

.active .submenu-item {
  color: white;
}

/* Footer del sidebar */
.sidebar-footer {
  padding: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: auto;
}

.sidebar-menu ul {
  list-style: none;
  /* Esto elimina los puntos */
  padding: 0;
  /* Opcional: elimina el padding por defecto */
  margin: 0;
  /* Opcional: elimina el margen por defecto */
}


/* Transiciones */
.slide-enter-active,
.slide-leave-active {
  transition: max-height 0.3s ease, opacity 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  max-height: 0;
  opacity: 0;
}

.slide-enter-to,
.slide-leave-from {
  max-height: 300px;
  opacity: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Overlay para móvil */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  backdrop-filter: blur(2px);
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    width: 250px;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .sidebar:not(.collapsed) {
    transform: translateX(0);
  }

  .sidebar.collapsed {
    /* No necesitas width: 0 si usas transform */
    transform: translateX(-100%);
  }
}

@media (min-width: 769px) {
  .sidebar-overlay {
    display: none;
  }
}

@media (min-width: 769px) {

  .sidebar.collapsed .menu-item span,
  .sidebar.collapsed .submenu-arrow,
  .sidebar.collapsed .logo-text,
  .sidebar.collapsed .menu-header-title span,
  .sidebar.collapsed .menu-badge,
  .sidebar.collapsed .sidebar-footer {
    display: none;
  }

  .sidebar.collapsed .menu-item {
    justify-content: center;
    padding: 12px 0;
  }

  .sidebar.collapsed .menu-content {
    justify-content: center;
  }

  .sidebar.collapsed .sidebar-header {
    padding: 20px 0;
    justify-content: center;
  }

  .sidebar.collapsed .logo-img {
    margin: 0 auto;
  }

  .sidebar.collapsed .menu-header {
    padding: 10px 0;
    text-align: center;
    border: none;
  }

  .sidebar.collapsed .menu-header::after {
    content: "";
    display: block;
    width: 30%;
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
    margin: 5px auto 0;
  }
}
</style>