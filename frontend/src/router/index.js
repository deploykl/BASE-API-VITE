import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import DashBoardView from "../views/DashBoardView.vue";
import MaintenanceView from "../views/MaintenanceView.vue";
import NotFoundView from "../components/layout/NotFoundView.vue";
import UnauthorizedView from "../views/UnauthorizedView.vue"; // Necesitarás crear esta vista
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
    path: "/unauthorized",
    name: "unauthorized",
    component: UnauthorizedView, // Crear esta vista
    meta: {
      title: "Acceso no autorizado",
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

  // 🔹 Primero: si la ruta requiere login y NO está autenticado
  if (to.meta.requiresAuth && !isAuthenticated) {
    // guardamos la ruta a la que quiso ir
    localStorage.setItem('redirectAfterLogin', to.fullPath);
    return next({
      path: '/login',
      query: { error: 'no-access' } // opcional, para mostrar mensaje en el login
    });
  }

  // 🔹 Si está autenticado y quiere ir al login → lo mandamos al dashboard
  if (to.name === 'login' && isAuthenticated) {
    return next('/dashboard');
  }

  // 🔹 Rutas de admin → solo superusuario
  if (to.path.startsWith('/admin') && isAuthenticated && !isSuperuser) {
    return next('/unauthorized');
  }

  // 🔹 Rutas de módulos (ejemplo usuarios)
  if (to.path.startsWith('/user/') && isAuthenticated && !isSuperuser && !hasModuleAccess('usuarios', userModulos)) {
    return next('/unauthorized');
  }

  // Continuar
  next();
});

export default router;