import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/components/services/Axios";
import { useCustomToast } from "@/components/utils/toast";
import { webSocketTableroInstance } from "@/components/services/WebSocketTablero"; // Nombre corregido

export const useTableroStore = defineStore("tableroStore", () => {
  const toast = useCustomToast();
  const tableros = ref([]);
  const error = ref(null);
  const loading = ref(false);

  // Inicializar WebSocket
  // Inicializar WebSocket
  const initWebSocket = () => {
    console.log("Inicializando WebSocket...");

    // Conectar WebSocket si no está conectado
    if (!webSocketTableroInstance.connected) {
      console.log("WebSocket no conectado, conectando...");
      webSocketTableroInstance.connect();
    } else {
      console.log("WebSocket ya está conectado");
    }

    // Registrar handlers para los diferentes tipos de mensajes
    webSocketTableroInstance.on("TABLERO_CREATED", (data) => {
      handleTableroCreated(data);
    });

    webSocketTableroInstance.on("TABLERO_UPDATED", (data) => {
      handleTableroUpdated(data);
    });

    webSocketTableroInstance.on("TABLERO_DELETED", (data) => {
      handleTableroDeleted(data);
    });

    webSocketTableroInstance.on("TABLERO_STATUS_CHANGED", (data) => {
      handleTableroStatusChanged(data);
    });

    console.log("Handlers de WebSocket registrados");
  };

  // Handlers para eventos WebSocket
  const handleTableroCreated = (data) => {
    // Verificar si el tablero ya existe para evitar duplicados
    const exists = tableros.value.some((t) => t.id === data.tablero.id);
    if (!exists) {
      tableros.value.unshift(data.tablero);
      toast.showSuccess("Nuevo tablero creado (en tiempo real)");
    }
  };

  const handleTableroUpdated = (data) => {
    const index = tableros.value.findIndex((t) => t.id === data.tablero.id);
    if (index !== -1) {
      tableros.value[index] = data.tablero;
      toast.showSuccess("Tablero actualizado (en tiempo real)");
    }
  };

  const handleTableroDeleted = (data) => {
    tableros.value = tableros.value.filter((t) => t.id !== data.id);
    toast.showDelete("Tablero eliminado (en tiempo real)");
  };

  const handleTableroStatusChanged = (data) => {
    const index = tableros.value.findIndex((t) => t.id === data.tablero.id);
    if (index !== -1) {
      tableros.value[index] = data.tablero;
      toast.showSuccess(
        `Tablero ${
          data.tablero.is_active ? "activado" : "desactivado"
        } (en tiempo real)`
      );
    }
  };

  // Limpiar handlers al destruir el store
  const cleanupWebSocket = () => {
    webSocketTableroInstance.off("TABLERO_CREATED", handleTableroCreated);
    webSocketTableroInstance.off("TABLERO_UPDATED", handleTableroUpdated);
    webSocketTableroInstance.off("TABLERO_DELETED", handleTableroDeleted);
    webSocketTableroInstance.off(
      "TABLERO_STATUS_CHANGED",
      handleTableroStatusChanged
    );
  };

  // Métodos
const ListTablero = async () => {
  error.value = null;
  loading.value = true;

  try {
    const response = await api.get("dimon/tablero/");
    
    // Procesar los datos para incluir información de fuentes
    tableros.value = response.data.map(tablero => ({
      ...tablero,
      // Asegurarse de que fuentes_info esté disponible
      fuentes_detalles: tablero.fuentes_info || [],
      // Crear un array de IDs de fuentes para fácil manipulación
      fuentes_ids: tablero.fuentes_info ? tablero.fuentes_info.map(f => f.id) : []
    }));

    // Inicializar WebSocket después de cargar los datos
    initWebSocket();

    return tableros.value;
  } catch (err) {
    error.value = err;
    const message =
      err.response?.data?.detail ||
      err.response?.data?.message ||
      "Error al obtener tableros";
    toast.showError(message);
    throw err;
  } finally {
    loading.value = false;
  }
};


  // Crear un nuevo tablero
  const CreateTablero = async (tableroData) => {
  loading.value = true;

  try {
    // Asegúrate de que fuentes sea un array de IDs
    const dataToSend = {
      ...tableroData,
      fuentes: tableroData.fuentes ? tableroData.fuentes.map(f => f.id || f) : []
    };

    const response = await api.post("dimon/tablero/", dataToSend);
    return response.data;
  } catch (err) {
      error.value = err;

      if (err.response?.data) {
        for (const [field, messages] of Object.entries(err.response.data)) {
          const errorMsg = Array.isArray(messages) ? messages[0] : messages;
          toast.showError(`${field}: ${errorMsg}`);
        }
      } else {
        toast.showError(err.message || "Error al registrar tablero");
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Actualizar un tablero existente
const UpdateTablero = async (id, tableroData) => {
  loading.value = true;

  try {
    const dataToSend = {
      ...tableroData,
      fuentes: tableroData.fuentes ? tableroData.fuentes.map(f => f.id || f) : []
    };

    const response = await api.patch(`dimon/tablero/${id}/`, dataToSend);
    return response.data;
  } catch (err) {
      error.value = err;
      {
        toast.showError(err.message || "Error al actualizar tablero");
      }

      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Eliminar un tablero
  const DeleteTablero = async (id) => {
    loading.value = true;

    try {
      await api.delete(`dimon/tablero/${id}/`);
      tableros.value = tableros.value.filter((t) => t.id !== id);
      return true;
    } catch (err) {
      error.value = err;
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Error al eliminar tablero";
      toast.showError(message);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // Cambiar estado activo/inactivo del tablero
  const toggleTableroStatus = async (id, newStatus) => {
    try {
      const endpoint = newStatus ? "activate" : "deactivate";
      const response = await api.post(`dimon/tablero/${id}/${endpoint}/`);

      const tablero = tableros.value.find((t) => t.id === id);
      if (tablero) {
        tablero.is_active = newStatus;
      }
      return true;
    } catch (err) {
      error.value = err;
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        `Error al ${newStatus ? "activar" : "desactivar"} tablero`;
      toast.showError(message);

      // Revertir el cambio en la UI si falla
      const tablero = tableros.value.find((t) => t.id === id);
      if (tablero) {
        tablero.is_active = !newStatus;
      }

      return false;
    }
  };

  return {
    // Estado
    loading,
    tableros,
    error,

    // Métodos
    ListTablero,
    CreateTablero,
    UpdateTablero,
    DeleteTablero,
    toggleTableroStatus,
    cleanupWebSocket,
  };
});
