<template>
  <!-- Este template puede estar vacío -->
</template>

<script>
import Swal from 'sweetalert2';

// Función para mostrar una alerta de éxito
export const SwalSuccess = async (title = 'Elemento Agregado!', text = 'Ha sido agregado correctamente.') => {
  await Swal.fire({
    title,
    text,
    icon: 'success',
    timer: 1000,
    showConfirmButton: false,
    timerProgressBar: true,
    customClass: {
      container: 'swal2-custom-success',
      popup: 'swal2-custom-success',
      header: 'swal2-custom-success',
      title: 'swal2-custom-success',
      htmlContainer: 'swal2-custom-success',
      confirmButton: 'swal2-custom-success'
    }
  });
};

export const SwalUpdate = async () => {
  await Swal.fire({
    title: 'Elemento Actualizada!',
    text: 'El elemento ha sido actualizada correctamente.',
    icon: 'success',
    showConfirmButton: false,
    timer: 1000,
    timerProgressBar: true,
    position: "top-end",
    customClass: {
      container: 'swal2-custom-update',
      popup: 'swal2-custom-update',
      header: 'swal2-custom-update',
      title: 'swal2-custom-update',
      htmlContainer: 'swal2-custom-update',
      confirmButton: 'swal2-custom-update'
    }
  });
};

// Función para mostrar una alerta de error
export const SwalError = async (text = 'Ocurrió un error inesperado.') => {
  await Swal.fire({
    title: 'Error!',
    text,
    icon: 'error',
    confirmButtonText: 'Entendido',
    customClass: {
      container: 'swal2-custom-error',
      popup: 'swal2-custom-error',
      header: 'swal2-custom-error',
      title: 'swal2-custom-error',
      htmlContainer: 'swal2-custom-error',
      confirmButton: 'swal2-custom-error'
    }
  });
};

// Función para mostrar una alerta de advertencia con confirmación
export const SwalWarning = async (title = '¿Estás seguro?', text = "No podrás recuperar una vez eliminado.", showCancel = true) => {
  const result = await Swal.fire({
    title,
    text,
    icon: 'warning',
    showCancelButton: showCancel,
    confirmButtonText: 'Sí, continuar',
    cancelButtonText: showCancel ? 'Cancelar' : undefined,
    customClass: {
      container: 'swal2-custom-delete',
      popup: 'swal2-custom-delete',
      header: 'swal2-custom-delete',
      title: 'swal2-custom-delete',
      htmlContainer: 'swal2-custom-delete',
      confirmButton: 'swal2-custom-delete',
      cancelButton: showCancel ? 'swal2-custom-delete' : undefined,
    },
  });
  return result;
};

// Función para mostrar una alerta de eliminación
export const SwalDelete = async () => {
  await Swal.fire({
    title: '¡Eliminado!',
    text: 'El elemento ha sido eliminado.',
    icon: 'success',
    showConfirmButton: false,
    timer: 1000,
    timerProgressBar: true,
    customClass: {
      container: 'swal2-custom-delete',
      popup: 'swal2-custom-delete',
      header: 'swal2-custom-delete',
      title: 'swal2-custom-delete',
      htmlContainer: 'swal2-custom-delete',
      confirmButton: 'swal2-custom-delete',
    },
  });
};

export default {
  SwalSuccess, SwalUpdate, SwalError, SwalWarning, SwalDelete
}
</script>

<style scoped>
/* Estilos si los necesitas */
</style>