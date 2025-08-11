import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/components/services/Axios";
import { useCustomToast } from "@/components/utils/toast"

export const useUserStore = defineStore("userStore", () => {
  const toast = useCustomToast()
  const loading = ref(false);
  const users = ref([]);
  const error = ref(null);

  // Métodos
  const listUsers = async () => {
    error.value = null;

    try {
      const response = await api.get("user/users/");
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

const createUser = async (userData) => {
  try {
    const { password2, ...dataToSend } = userData;
    const response = await api.post("user/users/", dataToSend);

    users.value.unshift(response.data);
    toast.showSuccess("Usuario creado correctamente");
    return { success: true, data: response.data };
  } catch (err) {
    error.value = err;

    // Manejo mejorado de errores
    if (err.response?.data) {
      // Devolver los errores estructurados
      return { 
        success: false, 
        errors: err.response.data,
        message: "Error al crear usuario"
      };
    } else {
      toast.showError(err.message || "Error al crear usuario");
      return { success: false, message: err.message };
    }
  }
};

  const updateUser = async (id, userData) => {
    try {
      const { password2, ...dataToSend } = userData;
      const response = await api.patch(`user/users/${id}/`, dataToSend);

      const index = users.value.findIndex((u) => u.id === id);
      if (index !== -1) {
        users.value[index] = response.data;
      }
      toast.showSuccess("Usuario actualizado correctamente");
      return response.data;
    } catch (err) {
      error.value = err;

      // Manejo mejorado de errores que incluye DNI y celular
      if (err.response?.data) {
        // Mostrar todos los errores de campo específicos
        const fieldErrors = err.response.data;

        // Mostrar errores de campos conocidos
        const knownFields = ["username", "email", "dni", "celular"];
        let hasFieldErrors = false;

        knownFields.forEach((field) => {
          if (fieldErrors[field]) {
            const errorMsg = Array.isArray(fieldErrors[field])
              ? fieldErrors[field][0]
              : fieldErrors[field];
            toast.showError(`${field}: ${errorMsg}`);
            hasFieldErrors = true;
          }
        });

        // Mostrar errores no reconocidos
        if (!hasFieldErrors && fieldErrors.non_field_errors) {
          toast.showError(fieldErrors.non_field_errors.join(", "));
        } else if (!hasFieldErrors) {
          toast.showError(
            err.response.data.detail || "Error al actualizar usuario"
          );
        }
      } else {
        toast.showError(err.message || "Error al actualizar usuario");
      }

      throw err;
    } finally {
    }
  };

  const deleteUser = async (id) => {
    try {
      await api.delete(`user/users/${id}/`);
      users.value = users.value.filter((u) => u.id !== id);
      toast.showSuccess("Usuario eliminado correctamente");
      return true; // Indica éxito
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Error al eliminar usuario";
      toast.showError(message);
      return false; // Indica fallo
    }
  };

  const toggleUserStatus = async (id, newStatus) => {
    try {
      const endpoint = newStatus ? "activate" : "deactivate";
      await api.post(`user/users/${id}/${endpoint}/`);

      const user = users.value.find((u) => u.id === id);
      if (user) {
        user.is_active = newStatus;
      }
      toast.showSuccess(
        `Usuario ${newStatus ? "activado" : "desactivado"} correctamente`
      );
      return true;
    } catch (err) {
      error.value = err;
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        `Error al ${newStatus ? "activar" : "desactivar"} usuario`;
      toast.showError(message);
      throw err;
    } finally {
    }
  };

  const toggleStaffStatus = async (id, newStatus) => {
    try {
      const endpoint = newStatus ? "make_staff" : "remove_staff";
      await api.post(`user/users/${id}/${endpoint}/`);

      const user = users.value.find((u) => u.id === id);
      if (user) {
        user.is_staff = newStatus;
      }
      toast.showSuccess(
        `Usuario ${
          newStatus ? "promovido a staff" : "removido de staff"
        } correctamente`
      );
      return true;
    } catch (err) {
      error.value = err;
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        `Error al ${newStatus ? "promover" : "remover"} staff`;
      toast.showError(message);
      throw err;
    } finally {
    }
  };

  return {
    // Estado
    loading,
    users,
    error,

    // Métodos
    listUsers,
    createUser,
    updateUser,
    deleteUser,
    toggleUserStatus,
    toggleStaffStatus,
  };
});
