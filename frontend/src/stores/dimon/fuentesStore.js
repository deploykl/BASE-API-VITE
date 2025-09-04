import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/components/services/Axios";
import { useCustomToast } from "@/components/utils/toast";

export const useFuentesStore = defineStore("fuentesStore", () => {
  const toast = useCustomToast();
  const fuentes = ref([]);
  const error = ref(null);
  const loading = ref(false);

  // Listar todas las fuentes
  const ListFuentes = async () => {
    error.value = null;
    loading.value = true;

    try {
      const response = await api.get("dimon/fuentes/"); // Asegúrate de tener esta URL
      fuentes.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err;
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Error al obtener fuentes";
      toast.showError(message);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Crear una nueva fuente
  const CreateFuente = async (fuenteData) => {
    loading.value = true;

    try {
      const response = await api.post("dimon/fuentes/", fuenteData);
      fuentes.value.unshift(response.data);
      return response.data;
    } catch (err) {
      error.value = err;
      if (err.response?.data) {
        for (const [field, messages] of Object.entries(err.response.data)) {
          const errorMsg = Array.isArray(messages) ? messages[0] : messages;
          toast.showError(`${field}: ${errorMsg}`);
        }
      } else {
        toast.showError(err.message || "Error al crear fuente");
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    // Estado
    loading,
    fuentes,
    error,

    // Métodos
    ListFuentes,
    CreateFuente,
  };
});