import { ref, onMounted, onUnmounted } from "vue";
import { api } from "@/components/services/Axios";
import { useCustomToast } from "@/components/utils/toast";

// Constantes para mejor mantenibilidad
const NETWORK_TEST_ENDPOINTS = [
  "https://www.gstatic.com/generate_204",
  "https://connectivitycheck.gstatic.com/generate_204",
  "https://api.ipify.org?format=json",
];

const DEFAULT_CHECK_INTERVALS = {
  online: 60000,    // 1 minuto cuando está online
  offline: 10000,   // 10 segundos cuando está offline
  retry: 1000,      // 1 segundo para reintentos
  network: 5000,    // 5 segundos para chequeo de red
  debounce: 2000,   // 2 segundos debounce
  apiTimeout: 3000, // 3 segundos timeout para API
};

export function useConnection() {
  const toast = useCustomToast(); // Correcta inicialización dentro del composable
  
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

  // Verificar estado real de la red
  const checkRealNetworkStatus = async () => {
    if (state.isCheckingNetwork.value) return;
    
    state.isCheckingNetwork.value = true;
    clearTimeout(timers.network);

    let isConnected = false;

    // Probar múltiples endpoints
    for (const endpoint of NETWORK_TEST_ENDPOINTS) {
      try {
        const url = new URL(endpoint);
        url.searchParams.append("ts", Date.now()); // Evitar caché

        const response = await fetch(url, {
          method: endpoint.includes("generate_204") ? "HEAD" : "GET",
          cache: "no-store",
          mode: "no-cors",
        });

        isConnected = endpoint.includes("generate_204") 
          ? response.status === 204 
          : true;

        if (isConnected) break;
      } catch {
        continue;
      }
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

  // Verificar conexión con la API
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
      const response = await api.options("", {
        signal: controller.signal,
        timeout: DEFAULT_CHECK_INTERVALS.apiTimeout,
      });

      const newStatus = response.status >= 200 && response.status < 300;

      if (state.isApiConnected.value !== newStatus) {
        showNotification(
          newStatus
            ? "Conexión con el servidor restablecida"
            : "Problemas de conexión con el servidor",
          newStatus ? "success" : "error"
        );
      }

      state.isApiConnected.value = newStatus;
      state.lastApiCheck.value = new Date();
      resetCheckInterval();
    } catch (error) {
      state.isApiConnected.value = false;

      if (error.message !== "Timeout" && state.lastApiCheck.value) {
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
    checkApiConnection();
    resetCheckInterval();
    checkRealNetworkStatus();
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