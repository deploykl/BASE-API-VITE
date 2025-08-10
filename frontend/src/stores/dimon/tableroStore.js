import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/components/services/Axios";
import { useCustomToast } from "@/components/utils/toast";

export const useTableroStore = defineStore("tableroStore", () => {
  const toast = useCustomToast();
  const tableros = ref([]);
  const error = ref(null);

// Métodos
  const ListTablero = async () => {
    error.value = null;

    try {
      const response = await api.get("dimon/tablero/");
      users.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err;
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Error al obtener usuarios";
      toast.showError(message);
      throw err;
    } finally {
    }
  };

return {
    tableros,
    error,

    // Métodos
    ListTablero,
  };
});
