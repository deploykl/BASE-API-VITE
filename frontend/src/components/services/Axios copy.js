import axios from 'axios';
import router from '@/router';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

let refreshPromise = null;

api.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

api.interceptors.response.use(response => response, async error => {
  const originalRequest = error.config;
  
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
  router.push('/login');
}

export { api };
