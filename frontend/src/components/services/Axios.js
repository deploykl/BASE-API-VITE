import axios from 'axios';
import router from '@/router';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000, // Timeout global de 10 segundos
});

let refreshPromise = null;
let isCheckingHealth = false;

// Interceptor de solicitud
api.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// Función para verificar salud del backend
const checkBackendHealth = async () => {
  if (isCheckingHealth) return false;
  
  isCheckingHealth = true;
  try {
    const response = await api.get('user/health-check/', { timeout: 3000 });
    return response.data.status === 'OK' || response.data.status === 'DEGRADED';
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  } finally {
    isCheckingHealth = false;
  }
};

// Interceptor de respuesta
api.interceptors.response.use(response => response, async error => {
  const originalRequest = error.config;
  
  // Manejar errores de conexión (backend no disponible)
  if (!error.response) {
    // Evitar redirección múltiple
    if (router.currentRoute.value.name !== 'maintenance') {
      const isHealthy = await checkBackendHealth();
      if (!isHealthy) {
        router.push({ name: 'maintenance' });
      }
    }
    return Promise.reject({
      ...error,
      message: 'El servicio no está disponible en este momento. Por favor, inténtelo más tarde.'
    });
  }
  
  // Manejar token expirado (401)
  if (error.response?.status === 401 && !originalRequest._isRetry && 
      !originalRequest.url.includes('token/refresh')) {
    
    originalRequest._isRetry = true;
    
    if (!refreshPromise) {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) {
        logout();
        return Promise.reject(error);
      }
      
      refreshPromise = api.post('token/refresh/', { refresh: refreshToken })
        .then(response => {
          const newAccessToken = response.data.access;
          localStorage.setItem('auth_token', newAccessToken);
          api.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
          return newAccessToken;
        })
        .catch(err => {
          logout();
          return Promise.reject(err);
        })
        .finally(() => {
          refreshPromise = null;
        });
    }
    
    return refreshPromise.then(token => {
      originalRequest.headers.Authorization = `Bearer ${token}`;
      return api(originalRequest);
    });
  }
  
  return Promise.reject(error);
});

function logout() {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('refreshToken');
  localStorage.removeItem('is_superuser');
  localStorage.removeItem('is_staff');
  localStorage.removeItem('user_modulos');
  router.push('/login');
}

// Exportar función de health check para uso global
export { api, checkBackendHealth };