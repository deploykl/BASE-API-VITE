import { ref, onMounted, onUnmounted } from "vue";
import { api } from "@/components/services/Axios";
import { useToast } from "vue-toastification";

// Constantes para mejor mantenibilidad
const NETWORK_TEST_ENDPOINTS = [
  "https://www.gstatic.com/generate_204",
  "https://connectivitycheck.gstatic.com/generate_204",
  "https://api.ipify.org?format=json",
];

const DEFAULT_CHECK_INTERVALS = {
  online: 60000,
  offline: 10000,
  retry: 1000,
  network: 5000,
  debounce: 2000,
  apiTimeout: 3000,
};

export function useConnection() {
  const toast = useToast();

  // Estados agrupados
  const state = {
    isOnline: ref(navigator.onLine),
    isApiConnected: ref(null),
    isCheckingApi: ref(false),
    isCheckingNetwork: ref(false), // Nuevo estado
    lastApiCheck: ref(null),
    lastNetworkChange: ref(null),
  };

  // Timers como referencia para mejor limpieza
  const timers = {
    apiCheck: null,
    retry: null,
    network: null,
  };

  // Mostrar notificación (memoizada)
  const showNotification = (message, type = "info") => {
    toast[type](message, {
      timeout: 3000,
      closeOnClick: true,
      pauseOnFocusLoss: true,
      pauseOnHover: true,
    });
  };

  // En useConnection.js
  // Modifica checkRealNetworkStatus
  const checkRealNetworkStatus = async () => {
    state.isCheckingNetwork.value = true;
    clearTimeout(timers.network);

    let isConnected = false;

    for (const endpoint of NETWORK_TEST_ENDPOINTS) {
      try {
        const url = new URL(endpoint);
        url.searchParams.append("ts", Date.now());

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

  const updateNetworkStatus = () => {
    const now = Date.now();
    if (
      state.lastNetworkChange.value &&
      now - state.lastNetworkChange.value < DEFAULT_CHECK_INTERVALS.debounce
    ) {
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

  const checkApiConnection = async () => {
    if (state.isCheckingApi.value || !state.isOnline.value) {
      // Si no hay internet, forzar estado offline
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
      const response = await api
        .options("", {
          signal: controller.signal,
          timeout: DEFAULT_CHECK_INTERVALS.apiTimeout,
        })
        .catch((error) => {
          // Manejar errores de axios específicamente
          if (
            error.code === "ECONNABORTED" ||
            error.message.includes("timeout")
          ) {
            throw new Error("Timeout");
          }
          throw error;
        });

      // Solo considerar éxito respuestas 2xx
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
      // Cualquier error debe marcar la API como desconectada
      state.isApiConnected.value = false;

      if (error.message !== "Timeout" && state.lastApiCheck.value) {
        // Solo mostrar notificación si previamente estaba conectado
        showNotification("Error al conectar con el servidor", "error");
      }

      scheduleRetry();
    } finally {
      clearTimeout(timeoutId);
      state.isCheckingApi.value = false;
    }
  };

  // Modificar los intervalos para ser más reactivos
  const DEFAULT_CHECK_INTERVALS = {
    online: 30000, // 30 segundos cuando está online
    offline: 5000, // 5 segundos cuando está offline
    retry: 2000, // 2 segundos para reintentos
    network: 5000, // 5 segundos para chequeo de red
    debounce: 1000, // 1 segundo debounce
    apiTimeout: 1500, // 1.5 segundos timeout para API
  };

  const scheduleRetry = () => {
    clearTimeout(timers.retry);
    timers.retry = setTimeout(
      checkApiConnection,
      DEFAULT_CHECK_INTERVALS.retry
    );
  };

  const resetCheckInterval = () => {
    clearInterval(timers.apiCheck);
    const interval = state.isApiConnected.value
      ? DEFAULT_CHECK_INTERVALS.online
      : DEFAULT_CHECK_INTERVALS.offline;
    timers.apiCheck = setInterval(checkApiConnection, interval);
  };

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
    Object.values(timers).forEach((timer) => {
      if (timer) clearTimeout(timer);
    });
  });

  return {
    ...state,
  checkApiConnection,
  checkRealNetworkStatus
  };
}
