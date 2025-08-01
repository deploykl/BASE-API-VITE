import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import DashBoardView from "../views/DashBoardView.vue";
import NotFoundView from "../components/layout/NotFoundView.vue"; // Componente para 404
import AdminPoi from "./AdminPoi";
import AdminAuth from "./AdminAuth";
import AdminGore from "./AdminGore";

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
    path: "/:catchAll(.*)",
    name: "not-found",
    component: NotFoundView,
    meta: {
      title: "Página no encontrada",
      public: true,  // Marca como pública
      hideLayout: true  // Nueva propiedad para ocultar layout
    },
  },
  // INTEGRANDO POI ADMIN ROUTES
  ...AdminPoi,
  ...AdminAuth,
  ...AdminGore,
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// En router.js
// En tu router.js
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('auth_token');
  const userModulos = JSON.parse(localStorage.getItem('user_modulos') || '[]');
  const isSuperuser = localStorage.getItem('is_superuser') === 'true';
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login');
  }
  
  // Función helper para comparación case-insensitive
  const hasModuleAccess = (moduleName) => {
    return userModulos.some(m => m.toLowerCase() === moduleName.toLowerCase());
  };
  
  // Protección especial para rutas de usuarios
  if (to.path.startsWith('/user/') && !isSuperuser && !hasModuleAccess('usuarios')) {
    return next('/unauthorized');
  }
  
  if (to.name === 'login' && isAuthenticated) {
    return next('/dashboard');
  }
  
  next();
});
export default router;
