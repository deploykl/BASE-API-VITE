import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from "@/components/services/Axios";
import { useCustomToast } from "@/components/utils/toast";

export const usePersonalStore = defineStore("personalStore", () => {
  const toast = useCustomToast();
  const loading = ref(false);
  const personal = ref([]);
  const modulos = ref([]); // Añadir módulos al store
  const dependencias = ref([]);
  const areas = ref([]);
  const error = ref(null);
  const selectedDependencia = ref(null);

  // Computed para las opciones de filtro de áreas
  const areaFilterOptions = computed(() => {
    if (!selectedDependencia.value) {
      return [...new Set(personal.value.map((u) => u.area_nombre))].filter(
        (v) => v !== null && v !== undefined
      );
    }

    return personal.value
      .filter((u) => u.dependencia_nombre === selectedDependencia.value)
      .map((u) => u.area_nombre)
      .filter((v, i, a) => a.indexOf(v) === i && v !== null);
  });

  // Métodos
  const setSelectedDependencia = (dependencia) => {
    selectedDependencia.value = dependencia;
  };

  const ListPersonal = async () => {
    error.value = null;
    try {
      const response = await api.get("dgos/administracion/personal");
      personal.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err;
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Error al obtener personal";
      toast.showError(message);
      throw err;
    }
  };
  const ListDependencias = async () => {
    try {
      const response = await api.get("dgos/administracion/dependencia/"); // Ajusta la URL según tu API
      dependencias.value = response.data;
      return response.data;
    } catch (err) {
      const message =
        err.response?.data?.message || "Error al cargar dependencias";
      toast.showError(message);
      throw err;
    }
  };
   const ListAreas = async () => {
    try {
      const response = await api.get("dgos/administracion/area/"); // Ajusta la URL según tu API
      areas.value = response.data;
      return response.data;
    } catch (err) {
      const message =
        err.response?.data?.message || "Error al cargar areas";
      toast.showError(message);
      throw err;
    }
  };
  const ListAreasByDependencia = async (dependenciaId) => {
  try {
    const response = await api.get(`dgos/administracion/area/?dependencia=${dependenciaId}`);
    return response.data;
  } catch (err) {
    const message = err.response?.data?.message || "Error al cargar áreas";
    toast.showError(message);
    throw err;
  }
};
  // NUEVO: Obtener módulos disponibles
  const ListModulos = async () => {
    try {
      const response = await api.get("/user/modulo/");
      modulos.value = response.data;
      return response.data;
    } catch (err) {
      const message =
        err.response?.data?.message || "Error al cargar los módulos";
      toast.showError(message);
      throw err;
    }
  };

  // Crear un nuevo tablero
  const CreatePersonal = async (personalData) => {
    loading.value = true;

    try {
      const response = await api.post(
        "dgos/administracion/personal",
        personalData
      );
      personal.value.unshift(response.data);
      toast.showSuccess("Personal creado correctamente");
      return response.data;
    } catch (err) {
      error.value = err;

      if (err.response?.data) {
        for (const [field, messages] of Object.entries(err.response.data)) {
          const errorMsg = Array.isArray(messages) ? messages[0] : messages;
          toast.showError(`${field}: ${errorMsg}`);
        }
      } else {
        toast.showError(err.message || "Error al registrar personal");
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Actualizar un tablero existente
  const UpdatePersonal = async (id, personalData) => {
    loading.value = true;

    try {
      const response = await api.patch(
        `dgos/administracion/personal/${id}/`,
        personalData
      );

      const index = personal.value.findIndex((t) => t.id === id);
      if (index !== -1) {
        personal.value[index] = response.data;
      }
      toast.showSuccess("Personal actualizado correctamente");
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
  const DeletePersonal = async (id) => {
    loading.value = true;

    try {
      await api.delete(`dgos/administracion/personal/${id}/`);
      personal.value = personal.value.filter((t) => t.id !== id);
      toast.showSuccess("Personal eliminado correctamente");
      return true;
    } catch (err) {
      error.value = err;
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Error al eliminar personal";
      toast.showError(message);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // NUEVO: Gestionar módulos de usuario
  const gestionarModulos = async (personId, modulosIds, mode = "habilitar") => {
    loading.value = true;
    try {
      let response;

      if (mode === "habilitar") {
        response = await api.post(
          `/dgos/administracion/personal/${personId}/habilitar_acceso/`,
          { modulos: modulosIds }
        );
      } else {
        response = await api.put(
          `/dgos/administracion/personal/${personId}/modulos/`,
          { modulos: modulosIds }
        );
      }

      if (response.data.success) {
        toast.showSuccess(response.data.message);
        await ListPersonal(); // Recargar datos
        return response.data;
      } else {
        toast.showError(response.data.message);
        throw new Error(response.data.message);
      }
    } catch (err) {
      const message =
        err.response?.data?.message ||
        `Error al ${mode === "habilitar" ? "habilitar" : "editar"} módulos`;
      toast.showError(message);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const deshabilitarAcceso = async (person) => {
    if (
      !confirm(`¿Deshabilitar acceso a ${person.nombre} ${person.apellido}?`)
    ) {
      return;
    }

    loading.value = true;
    try {
      const response = await api.post(
        `/dgos/administracion/personal/${person.id}/deshabilitar_acceso/`
      );

      if (response.data.success) {
        toast.showSuccess(response.data.message);
        await ListPersonal();
      } else {
        toast.showError(response.data.message);
      }
    } catch (err) {
      const message =
        err.response?.data?.message || "Error al deshabilitar acceso";
      toast.showError(message);
    } finally {
      loading.value = false;
    }
  };

  const resetearPassword = async (person) => {
    if (
      !confirm(`¿Resetear contraseña de ${person.nombre} ${person.apellido}?`)
    ) {
      return;
    }

    loading.value = true;
    try {
      const response = await api.post(
        `/dgos/administracion/personal/${person.id}/resetear_password/`
      );

      if (response.data.success) {
        toast.showSuccess(response.data.message);
      } else {
        toast.showError(response.data.message);
      }
    } catch (err) {
      const message =
        err.response?.data?.message || "Error al resetear contraseña";
      toast.showError(message);
    } finally {
      loading.value = false;
    }
  };

  return {
    // Estado
    loading,
    personal,
    modulos,
    dependencias,
    areas,
    error,
    selectedDependencia,
    areaFilterOptions,

    // Métodos
    ListPersonal,
    ListModulos,
    ListDependencias,
    ListAreas,
    ListAreasByDependencia,
    CreatePersonal,
    UpdatePersonal,
    DeletePersonal,
    gestionarModulos,
    deshabilitarAcceso,
    resetearPassword,
    setSelectedDependencia,
  };
});
