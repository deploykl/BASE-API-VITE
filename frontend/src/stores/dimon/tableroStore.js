import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/components/services/Axios";
import { useCustomToast } from "@/components/utils/toast";

export const useTableroStore = defineStore("tableroStore", () => {
  const toast = useCustomToast();
  const tableros = ref([]);
  const error = ref(null);
  const loading = ref(false);

  // Métodos
  const ListTablero = async () => {
    error.value = null;

    try {
      const response = await api.get("dimon/tablero/");
      tableros.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err;
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Error al obtener tableros";
      toast.showError(message);
      throw err;
    } finally {
    }
  };
  // Crear un nuevo tablero
const CreateTablero = async (tableroData) => {
  loading.value = true;

  try {
    const response = await api.post("dimon/tablero/", tableroData);
    tableros.value.unshift(response.data);
    toast.showSuccess("Tablero registrado correctamente");
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
    loading.value = false; // ¡Esto faltaba!
  }
};
  // Actualizar un tablero existente
  const UpdateTablero = async (id, tableroData) => {
    loading.value = true;

    try {
      const response = await api.patch(`dimon/tablero/${id}/`, tableroData);

      const index = tableros.value.findIndex((t) => t.id === id);
      if (index !== -1) {
        tableros.value[index] = response.data;
      }
      toast.showSuccess("Tablero actualizado correctamente");
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
    toast.showSuccess("Tablero eliminado correctamente");
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
    loading.value = false; // Esto es lo que faltaba
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
    toast.showSuccess(
      `Tablero ${newStatus ? "activado" : "desactivado"} correctamente`
    );
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
  } finally {
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
  };
});
