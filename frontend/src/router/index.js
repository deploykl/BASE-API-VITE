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
      requiredModule: null, // ← Añade esta propiedad
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

// Función mejorada para verificar módulos (case-insensitive y con soporte para múltiples)
const hasModuleAccess = (moduleNames, userModulos) => {
  if (!moduleNames) return true;
  
  // Si es string, convertirlo a array
  const modulesToCheck = typeof moduleNames === 'string' 
    ? moduleNames.split(',').map(m => m.trim().toLowerCase())
    : Array.isArray(moduleNames) 
      ? moduleNames.map(m => m.toLowerCase())
      : [];
  
  if (modulesToCheck.length === 0) return true;
  
  const userModules = userModulos.map(m => m.toLowerCase());
  
  // Verifica si al menos uno de los módulos existe en los módulos del usuario
  return modulesToCheck.some(module => userModules.includes(module));
};

// Guardia global de navegación mejorada
router.beforeEach(async (to, from, next) => {
  const isAuthenticated = localStorage.getItem('auth_token');
  const userModulos = JSON.parse(localStorage.getItem('user_modulos') || '[]');
  const isSuperuser = localStorage.getItem('is_superuser') === 'true';

  // 🔹 PRIMERO: Si la ruta es pública, NO verificar backend
  if (to.meta.public) {
    return next();
  }

  // 🔹 SEGUNDO: Verificar salud del backend solo para rutas NO públicas
  if (to.name !== 'maintenance') {
    try {
      const isHealthy = await checkBackendHealth();
      if (!isHealthy) {
        return next({ name: 'maintenance' });
      }
    } catch (error) {
      return next({ name: 'maintenance' });
    }
  }

  // 🔹 TERCERO: Lógica de autenticación
  if (to.meta.requiresAuth && !isAuthenticated) {
    localStorage.setItem('redirectAfterLogin', to.fullPath);
    return next({
      path: '/login',
      query: { error: 'no-access' }
    });
  }

  if (to.name === 'login' && isAuthenticated) {
    return next('/dashboard');
  }

  // 🔹 CUARTO: Verificación de permisos por módulos (solo para rutas que requieren auth)
  if (to.meta.requiresAuth && isAuthenticated) {
    // 1. Si es superusuario, permite acceso a todo
    if (isSuperuser) {
      console.log('Acceso concedido: usuario superuser');
      return next();
    }
    
    // 2. Verificar si la ruta requiere módulos específicos
    if (to.meta.requiredModule !== undefined) { // Cambiado de to.meta.requiredModule a esta verificación
      const hasAccess = hasModuleAccess(to.meta.requiredModule, userModulos);
      
      if (!hasAccess) {
        console.warn(`Acceso denegado a ${to.path}. Módulos requeridos: ${to.meta.requiredModule}. Usuario tiene: ${userModulos.join(', ') || 'ninguno'}`);
        return next('/unauthorized');
      }
      
      console.log('Acceso concedido: usuario tiene los módulos requeridos');
    } else {
      console.log('Acceso concedido: ruta no requiere módulos específicos');
    }
    
    // 3. Verificación adicional para rutas administrativas (opcional)
    if (to.path.startsWith('/admin') && !isSuperuser) {
      console.warn('Acceso denegado: ruta admin requiere superuser');
      return next('/unauthorized');
    }
  }

  next();
});

export default router;