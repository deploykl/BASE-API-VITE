<template>
  <Toaster 
    position="bottom-right" 
    :theme="theme"
    :rich-colors="true"
    :expand="true"
    :visible-toasts="3"
  />
</template>

<script setup>
import { ref } from 'vue'
import { Toaster } from 'vue-sonner'

const theme = ref('dark') // Puedes cambiarlo dinámicamente
</script>

<style>
/* Estilos personalizados */
.custom-toast {
  font-family: 'TuFuente', sans-serif;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.custom-toast[data-type='success'] {
  background-color: #001401;
  color: white;
}

.custom-toast[data-type='error'] {
  background-color: #f44336;
  color: white;
}

.custom-toast[data-type='warning'] {
  background-color: #ff9800;
  color: white;
}

.custom-toast[data-type='info'] {
  background-color: #2196f3;
  color: white;
}

/* Estilos para el toast de confirmación */
.sonner-confirm {
  padding: 12px;
}

.confirm-title {
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 500;
}

.confirm-buttons {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.confirm-button {
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-size: 13px;
  transition: background-color 0.2s;
}

.confirm-button-yes {
  background-color: #4caf50;
  color: white;
}

.confirm-button-no {
  background-color: #f44336;
  color: white;
}
</style>