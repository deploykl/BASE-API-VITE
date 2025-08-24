import { useToast } from "primevue/usetoast";

export const useCustomToast = () => {
  const toast = useToast();

  // Mostrar toast genérico
  const showToast = (options) => {
    return toast.add({
      life: 3000,
      closable: false, // Desactiva el cierre manual

      ...options,
    });
  };

  // Toast de éxito
  const showSuccess = (message, summary = "Éxito") => {
    showToast({
      severity: "success",
      summary,
      detail: message,
      class: "custom-toast success-toast",
    });
  };

  // Toast de eliminación (usando severity "error" con clase personalizada)
  const showDelete = (message, summary = "Eliminado") => {
    showToast({
      severity: "error", // Usa el severity error que ya tiene estilo rojo
      summary,
      detail: message,
      life: 4000,
      class: "delete-toast", // Clase adicional para personalización
    });
  };

  // Toast de error
  const showError = (message, summary = "Error") => {
    showToast({
      severity: "error",
      summary,
      detail: message,
      life: 5000,
      class: "custom-toast error-toast",
    });
  };

  // Toast de advertencia
  const showWarning = (message, summary = "Advertencia") => {
    showToast({
      severity: "warn",
      summary,
      detail: message,
      class: "custom-toast warning-toast",
    });
  };

  // Toast informativo
  const showInfo = (message, summary = "Información") => {
    showToast({
      severity: "info",
      summary,
      detail: message,
      class: "custom-toast info-toast",
    });
  };

  // Toast de carga (loading)
  const showLoading = (message, summary = "Cargando") => {
    return showToast({
      severity: "info",
      summary,
      detail: message,
      life: 0, // Persistente hasta que se cierre manualmente
    });
  };

  // Cerrar toast específico
  const dismissToast = (toastRef) => {
    if (toastRef) {
      toast.remove(toastRef);
    }
  };

  return {
    showSuccess,
    showError,
    showDelete,
    showWarning,
    showInfo,
    showLoading,
    dismissToast,
  };
};
