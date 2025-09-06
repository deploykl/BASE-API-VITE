import { ref, onMounted, onUnmounted } from "vue";
import { useCustomToast } from "@/components/utils/toast";

// Ruta de tu API Django
const API_BASE_URL = import.meta.env.VITE_API_URL;

const DEFAULT_CHECK_INTERVALS = {
  online: 60000,    // 1 minuto cuando está online
  offline: 10000,   // 10 segundos cuando está offline
  retry: 5000,      // 5 segundos para reintentos (aumentado)
  network: 10000,   // 10 segundos para chequeo de red
  debounce: 2000,   // 2 segundos debounce
  apiTimeout: 8000, // 8 segundos timeout para API (aumentado)
};

export function useConnection() {
  const toast = useCustomToast();
  
  // Estados reactivos
  const state = {
    isOnline: ref(navigator.onLine),
    isApiConnected: ref(null),
    isCheckingApi: ref(false),
    isCheckingNetwork: ref(false),
    lastApiCheck: ref(null),
    lastNetworkChange: ref(null),
  };

  // Timers para manejo de intervalos
  const timers = {
    apiCheck: null,
    retry: null,
    network: null,
  };

  // Mostrar notificación usando PrimeVue Toast
  const showNotification = (message, type = "info") => {
    switch (type) {
      case "success":
        toast.showSuccess(message);
        break;
      case "error":
        toast.showError(message);
        break;
      case "warning":
        toast.showWarning(message);
        break;
      default:
        toast.showInfo(message);
    }
  };

  // Verificar estado real de la red usando una imagen como método alternativo
  const checkRealNetworkStatus = async () => {
    if (state.isCheckingNetwork.value) return;
    
    state.isCheckingNetwork.value = true;
    clearTimeout(timers.network);

    let isConnected = false;

    // Método alternativo para verificar conexión sin problemas CORS
    try {
      isConnected = await checkConnectionWithImage();
    } catch (error) {
      console.error("Error checking network connection:", error);
      isConnected = false;
    }

    // Solo actualizar si hay cambio de estado
    if (isConnected !== state.isOnline.value) {
      state.isOnline.value = isConnected;
      showNotification(
        isConnected 
          ? "Conexión a Internet restablecida" 
          : "Se perdió la conexión a Internet",
        isConnected ? "success" : "error"
      );
      
      if (isConnected) checkApiConnection();
    }

    state.isCheckingNetwork.value = false;
    timers.network = setTimeout(
      checkRealNetworkStatus, 
      DEFAULT_CHECK_INTERVALS.network
    );
  };

  // Método alternativo para verificar conexión usando una imagen
  const checkConnectionWithImage = () => {
    return new Promise((resolve) => {
      const img = new Image();
      let timedOut = false;
      
      // Timeout para la verificación
      const timeout = setTimeout(() => {
        timedOut = true;
        resolve(false);
      }, 2000);
      
      img.onload = () => {
        if (!timedOut) {
          clearTimeout(timeout);
          resolve(true);
        }
      };
      
      img.onerror = () => {
        if (!timedOut) {
          clearTimeout(timeout);
          resolve(false);
        }
      };
      
      // Usar una imagen de Google con timestamp para evitar caché
      img.src = "https://www.google.com/favicon.ico?t=" + Date.now();
    });
  };

  // Actualizar estado de red con debounce
  const updateNetworkStatus = () => {
    const now = Date.now();
    if (state.lastNetworkChange.value && 
        now - state.lastNetworkChange.value < DEFAULT_CHECK_INTERVALS.debounce) {
      return;
    }

    state.lastNetworkChange.value = now;
    const newStatus = navigator.onLine;

    if (newStatus !== state.isOnline.value) {
      state.isOnline.value = newStatus;
      showNotification(
        newStatus 
          ? "Conexión a Internet restablecida" 
          : "Se perdió la conexión a Internet",
        newStatus ? "success" : "error"
      );
      
      if (newStatus) checkApiConnection();
      else state.isApiConnected.value = false;
    }

    checkRealNetworkStatus();
  };

  // Verificar conexión con la API de Django - CORREGIDO
  const checkApiConnection = async () => {
    if (state.isCheckingApi.value || !state.isOnline.value) {
      if (!state.isOnline.value) {
        state.isApiConnected.value = false;
      }
      return;
    }

    state.isCheckingApi.value = true;
    const controller = new AbortController();
    const timeoutId = setTimeout(
      () => controller.abort(),
      DEFAULT_CHECK_INTERVALS.apiTimeout
    );

    try {
      // Verificar API Django directamente
const response = await fetch(`${API_BASE_URL}user/health-check/`, {
        method: 'GET',
        signal: controller.signal,
        headers: {
          'Accept': 'application/json',
        },
      });

      // Verificar si la respuesta es exitosa
      const responseOk = response.status >= 200 && response.status < 300;
      
      if (responseOk) {
        // Intentar parsear la respuesta JSON
        try {
          const data = await response.json();
          
          // Verificar el contenido específico de la respuesta
          // Dependiendo de la estructura de tu health check
          const isApiHealthy = data.status === "OK" || 
                              data.status === "success" || 
                              (data.services && data.services.database === true);
          
          if (state.isApiConnected.value !== isApiHealthy) {
            showNotification(
              isApiHealthy
                ? "Conexión con el servidor Django restablecida"
                : "Problemas de conexión con el servidor",
              isApiHealthy ? "success" : "error"
            );
          }
          
          state.isApiConnected.value = isApiHealthy;
        } catch (jsonError) {
          console.error("Error parsing JSON response:", jsonError);
          // Si no podemos parsear JSON, al menos la respuesta HTTP fue exitosa
          state.isApiConnected.value = responseOk;
          if (state.isApiConnected.value !== responseOk) {
            showNotification(
              "Conexión con el servidor restablecida",
              "success"
            );
          }
        }
      } else {
        state.isApiConnected.value = false;
        if (state.isApiConnected.value !== false) {
          showNotification("Problemas de conexión con el servidor ", "error");
        }
      }

      state.lastApiCheck.value = new Date();
      resetCheckInterval();
    } catch (error) {
      console.error("API connection check failed:", error);
      state.isApiConnected.value = false;

      if (error.name !== "AbortError" && state.lastApiCheck.value) {
        showNotification("Error al conectar con el servidor", "error");
      }

      scheduleRetry();
    } finally {
      clearTimeout(timeoutId);
      state.isCheckingApi.value = false;
    }
  };

  // Programar reintento
  const scheduleRetry = () => {
    clearTimeout(timers.retry);
    timers.retry = setTimeout(
      checkApiConnection, 
      DEFAULT_CHECK_INTERVALS.retry
    );
  };

  // Reiniciar intervalo de chequeo
  const resetCheckInterval = () => {
    clearInterval(timers.apiCheck);
    const interval = state.isApiConnected.value
      ? DEFAULT_CHECK_INTERVALS.online
      : DEFAULT_CHECK_INTERVALS.offline;
    timers.apiCheck = setInterval(checkApiConnection, interval);
  };

  // Setup y limpieza
  onMounted(() => {
    window.addEventListener("online", updateNetworkStatus);
    window.addEventListener("offline", updateNetworkStatus);
    
    // Iniciar verificaciones después de un breve delay
    setTimeout(() => {
      checkApiConnection();
      resetCheckInterval();
      checkRealNetworkStatus();
    }, 1000);
  });

  onUnmounted(() => {
    window.removeEventListener("online", updateNetworkStatus);
    window.removeEventListener("offline", updateNetworkStatus);
    Object.values(timers).forEach(clearTimeout);
  });

  return {
    ...state,
    checkApiConnection,
    checkRealNetworkStatus,
  };
}