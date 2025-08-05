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
  const showLoading = (message) => {
    return showToast({
      severity: "info",
      detail: message,
      class: "custom-toast loading-toast",
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
    showWarning,
    showInfo,
    showLoading,
    dismissToast,
  };
};
