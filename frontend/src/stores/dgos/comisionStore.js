import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/components/services/Axios";
import { useCustomToast } from "@/components/utils/toast";


export const useComisionStore = defineStore("comisionStore", () => {
  const toast = useCustomToast();
  const comision = ref([]);
  const error = ref(null);
  const loading = ref(false);
const conductores = ref([]);
const vehiculos = ref([]);
const participantes = ref([]);

  // Métodos
  const ListComision = async () => {
    error.value = null;

    try {
      const response = await api.get("dgos/administracion/comision/");
      comision.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err;
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Error al obtener comision";
      toast.showError(message);
      throw err;
    } finally {
    }
  };
  const ListConductores = async () => {
  try {
    const response = await api.get("dgos/administracion/personal/?es_conductor=true");
    conductores.value = response.data;
    return response.data;
  } catch (err) {
    error.value = err;
    toast.showError("Error al obtener conductores");
    throw err;
  }
};

  const ListVehiculos = async () => {
  try {
    const response = await api.get("dgos/administracion/vehiculo/");
    vehiculos.value = response.data;
    return response.data;
  } catch (err) {
    error.value = err;
    toast.showError("Error al obtener vehiculos");
    throw err;
  }
};
  const ListParticipantes = async () => {
  try {
    const response = await api.get("dgos/administracion/personal/?es_conductor=false");
    participantes.value = response.data;
    return response.data;
  } catch (err) {
    error.value = err;
    toast.showError("Error al obtener participantes");
    throw err;
  }
};
  // Crear un nuevo tablero
const CreateComision = async (Data) => {
  loading.value = true;

  try {
    const response = await api.post("dgos/administracion/comision/", Data);
    comision.value.unshift(response.data);
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
  const UpdateComision = async (id, Data) => {
    loading.value = true;

    try {
      const response = await api.patch(`dgos/administracion/comision/${id}/`, Data);

      const index = comision.value.findIndex((t) => t.id === id);
      if (index !== -1) {
        comision.value[index] = response.data;
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
const DeleteComision = async (id) => {
  loading.value = true;

  try {
    await api.delete(`dgos/administracion/comision/${id}/`);
    comision.value = comision.value.filter((t) => t.id !== id);
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



  return {
    // Estado
    loading,
    comision,
    error,
    conductores, 
    vehiculos, 
    participantes, 

    // Métodos
    ListComision,
    ListConductores,
    ListVehiculos,
    ListParticipantes,
    CreateComision,
    UpdateComision,
    DeleteComision,
  };
});