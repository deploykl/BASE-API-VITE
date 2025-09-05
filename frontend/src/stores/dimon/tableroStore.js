import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/components/services/Axios";
import { useCustomToast } from "@/components/utils/toast";
import { webSocketTableroInstance } from "@/components/services/WebSocketTablero";

export const useTableroStore = defineStore("tableroStore", () => {
  const toast = useCustomToast();
  const tableros = ref([]);
  const fuentesOptions = ref([]);
  const categoriasOptions = ref([]);

  const error = ref(null);
  const loading = ref(false);

  // WebSocket methods
  const initWebSocket = () => {
    if (!webSocketTableroInstance.connected) {
      webSocketTableroInstance.connect();
    }

    webSocketTableroInstance.on("TABLERO_CREATED", handleTableroCreated);
    webSocketTableroInstance.on("TABLERO_UPDATED", handleTableroUpdated);
    webSocketTableroInstance.on("TABLERO_DELETED", handleTableroDeleted);
    webSocketTableroInstance.on("TABLERO_STATUS_CHANGED", handleTableroStatusChanged);
  };

  const handleTableroCreated = (data) => {
    const exists = tableros.value.some((t) => t.id === data.tablero.id);
    if (!exists) {
      const tableroWithFuentes = {
        ...data.tablero,
        fuentes_detalles: data.tablero.fuentes_info || [],
        fuentes_ids: data.tablero.fuentes_info ? data.tablero.fuentes_info.map(f => f.id) : []
      };
      tableros.value.unshift(tableroWithFuentes);
      toast.showSuccess("Nuevo tablero creado (en tiempo real)");
    }
  };

  const handleTableroUpdated = (data) => {
    const index = tableros.value.findIndex((t) => t.id === data.tablero.id);
    if (index !== -1) {
      const tableroWithFuentes = {
        ...data.tablero,
        fuentes_detalles: data.tablero.fuentes_info || [],
        fuentes_ids: data.tablero.fuentes_info ? data.tablero.fuentes_info.map(f => f.id) : []
      };
      tableros.value[index] = tableroWithFuentes;
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
      toast.showSuccess(`Tablero ${data.tablero.is_active ? "activado" : "desactivado"} (en tiempo real)`);
    }
  };

  const cleanupWebSocket = () => {
    webSocketTableroInstance.off("TABLERO_CREATED", handleTableroCreated);
    webSocketTableroInstance.off("TABLERO_UPDATED", handleTableroUpdated);
    webSocketTableroInstance.off("TABLERO_DELETED", handleTableroDeleted);
    webSocketTableroInstance.off("TABLERO_STATUS_CHANGED", handleTableroStatusChanged);
  };

  // API methods
  const ListTablero = async () => {
    error.value = null;
    loading.value = true;

    try {
      const response = await api.get("dimon/tablero/");
      tableros.value = response.data.map(tablero => ({
        ...tablero,
        fuentes_detalles: tablero.fuentes_info || [],
        fuentes_ids: tablero.fuentes_info ? tablero.fuentes_info.map(f => f.id) : []
      }));

      initWebSocket();
      return tableros.value;
    } catch (err) {
      error.value = err;
      const message = err.response?.data?.detail || err.response?.data?.message || "Error al obtener tableros";
      toast.showError(message);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const CreateTablero = async (tableroData) => {
    loading.value = true;
    try {
      const dataToSend = {
        ...tableroData,
        fuentes: tableroData.fuentes ? tableroData.fuentes.map(f => f.id || f) : []
      };

      const response = await api.post("dimon/tablero/", dataToSend);
      
      // Agregar el nuevo tablero a la lista
      const newTablero = {
        ...response.data,
        fuentes_detalles: response.data.fuentes_info || [],
        fuentes_ids: response.data.fuentes_info ? response.data.fuentes_info.map(f => f.id) : []
      };
      tableros.value.unshift(newTablero);
      
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

  const UpdateTablero = async (id, tableroData) => {
    loading.value = true;
    try {
      const dataToSend = {
        ...tableroData,
        fuentes: tableroData.fuentes ? tableroData.fuentes.map(f => f.id || f) : []
      };

      const response = await api.patch(`dimon/tablero/${id}/`, dataToSend);
      
      // Actualizar en la lista
      const index = tableros.value.findIndex((t) => t.id === id);
      if (index !== -1) {
        const updatedTablero = {
          ...response.data,
          fuentes_detalles: response.data.fuentes_info || [],
          fuentes_ids: response.data.fuentes_info ? response.data.fuentes_info.map(f => f.id) : []
        };
        tableros.value[index] = updatedTablero;
      }
      
      return response.data;
    } catch (err) {
      error.value = err;
      toast.showError(err.message || "Error al actualizar tablero");
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const DeleteTablero = async (id) => {
    loading.value = true;
    try {
      await api.delete(`dimon/tablero/${id}/`);
      tableros.value = tableros.value.filter((t) => t.id !== id);
      return true;
    } catch (err) {
      error.value = err;
      const message = err.response?.data?.detail || err.response?.data?.message || "Error al eliminar tablero";
      toast.showError(message);
      return false;
    } finally {
      loading.value = false;
    }
  };

  const toggleTableroStatus = async (id, newStatus) => {
    try {
      const endpoint = newStatus ? "activate" : "deactivate";
      await api.post(`dimon/tablero/${id}/${endpoint}/`);

      const tablero = tableros.value.find((t) => t.id === id);
      if (tablero) {
        tablero.is_active = newStatus;
      }
      return true;
    } catch (err) {
      error.value = err;
      const message = err.response?.data?.detail || err.response?.data?.message || `Error al ${newStatus ? "activar" : "desactivar"} tablero`;
      toast.showError(message);

      // Revertir cambio en UI
      const tablero = tableros.value.find((t) => t.id === id);
      if (tablero) {
        tablero.is_active = !newStatus;
      }
      return false;
    }
  };
const loadFuentesOptions = async () => {
  try {
    const response = await api.get("dimon/fuentes/");
    console.log('Respuesta de fuentes:', response.data);
    
    // Fix: Properly update the reactive reference
    fuentesOptions.value = response.data.map(fuente => ({
      label: `${fuente.nombre} (${fuente.frecuencia})`,
      value: fuente.id,
      data: fuente
    }));
    
    return fuentesOptions.value; // Return the options for convenience
  } catch (error) {
    console.error('Error cargando fuentes:', error);
    toast.showError('Error al cargar las fuentes');
    throw error; // Re-throw to handle in component
  }
};

  return {
    loading,
    tableros,
    fuentesOptions,
    categoriasOptions,
    error,
    ListTablero,
    CreateTablero,
    UpdateTablero,
    DeleteTablero,
    toggleTableroStatus,
    cleanupWebSocket,
    loadFuentesOptions
  };
});