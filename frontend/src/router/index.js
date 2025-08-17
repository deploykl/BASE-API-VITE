import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import DashBoardView from "../views/DashBoardView.vue";
import MaintenanceView from "../views/MaintenanceView.vue";
import NotFoundView from "../components/layout/NotFoundView.vue";
import AdminPoi from "./AdminPoi";
import AdminAuth from "./AdminAuth";
import AdminGore from "./AdminGore";
import AdminDimon from "./AdminDimon";
import AdminDgos from "./AdminDgos";
import { checkBackendHealth } from '@/components/services/Axios'; // Ajusta la ruta según tu estructura

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: {
      title: "HOME",
      public: true,
    },
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashBoardView,
    meta: {
      title: "DASHBOARD",
      requiresAuth: true,
    },
  },
  {
    path: "/maintenance",
    name: "maintenance",
    component: MaintenanceView,
    meta: {
      title: "Mantenimiento",
      public: true,
      hideLayout: true
    },
  },
  {
    path: "/:catchAll(.*)",
    name: "not-found",
    component: NotFoundView,
    meta: {
      title: "Página no encontrada",
      public: true,
      hideLayout: true
    },
  },
  ...AdminPoi,
  ...AdminAuth,
  ...AdminGore,
  ...AdminDimon,
  ...AdminDgos,
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Función para verificar módulos de usuario (case-insensitive)
const hasModuleAccess = (moduleName, userModulos) => {
  return userModulos.some(m => m.toLowerCase() === moduleName.toLowerCase());
};

// Guardia global de navegación
router.beforeEach(async (to, from, next) => {
  const isAuthenticated = localStorage.getItem('auth_token');
  const userModulos = JSON.parse(localStorage.getItem('user_modulos') || '[]');
  const isSuperuser = localStorage.getItem('is_superuser') === 'true';
  
  // Verificar salud del backend solo para rutas no públicas
  if (!to.meta.public && to.name !== 'maintenance') {
    try {
      const isHealthy = await checkBackendHealth();
      if (!isHealthy) {
        return next({ name: 'maintenance' });
      }
    } catch (error) {
      return next({ name: 'maintenance' });
    }
  }
  
  // Redirigir al login si la ruta requiere autenticación
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login');
  }
  
  // Redirigir al dashboard si ya está autenticado y va al login
  if (to.name === 'login' && isAuthenticated) {
    return next('/dashboard');
  }
  
  // Protección para rutas de administración
  if (to.path.startsWith('/admin') && !isSuperuser) {
    return next('/unauthorized');
  }
  
  // Protección especial para rutas de usuarios
  if (to.path.startsWith('/user/') && !isSuperuser && !hasModuleAccess('usuarios', userModulos)) {
    return next('/unauthorized');
  }
  
  // Continuar con la navegación
  next();
});

export default router;