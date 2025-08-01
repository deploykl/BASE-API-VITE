<template>
  <Dialog
    v-model:visible="internalVisible"
    :modal="true"
    :style="{ width: width }"
    :header="dynamicTitle"
    :breakpoints="{ '960px': '75vw', '640px': '90vw' }"
    @hide="handleClose"
  >
    <!-- Slot para el contenido principal -->
    <div class="dialog-content">
      <slot name="content"></slot>
    </div>
    
    <!-- Slot para el footer -->
    <template #footer>
      <slot name="footer">
        <Button 
          label="Cancelar" 
          icon="pi pi-times" 
          @click="handleClose" 
          class="p-button-text" 
          :disabled="loading"
        />
        <Button 
          :label="confirmText" 
          icon="pi pi-check" 
          @click="handleConfirm" 
          :loading="loading" 
          :class="confirmClass"
        />
      </slot>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'; // Añade computed aquí

const props = defineProps({
  visible: Boolean,
  title: String,
  mode: {  // Nuevo prop para el modo de operación
    type: String,
    default: 'create',
    validator: value => ['create', 'edit', 'delete'].includes(value)
  },
  entityName: {  // Nombre de la entidad (ej: "usuario")
    type: String,
    default: 'registro'
  },
  width: {
    type: String,
    default: '50vw'
  },
  confirmText: {
    type: String,
    default: 'Confirmar'
  },
  confirmClass: {
    type: String,
    default: ''
  },
  loading: Boolean
});
const dynamicTitle = computed(() => {
  const titles = {
    create: `Crear nuevo ${props.entityName}`,
    edit: `Editar ${props.entityName}`,
    delete: `Confirmar eliminación`
  };
  return props.title || titles[props.mode]; // Usa el título personalizado o el generado
});
const emit = defineEmits(['update:visible', 'close', 'confirm']);

const internalVisible = ref(props.visible);

watch(() => props.visible, (newVal) => {
  internalVisible.value = newVal;
});

const handleConfirm = async () => {
  try {
    await emit('confirm');
  } catch (error) {
    console.error('Error en confirmación:', error);
  }
};

const handleClose = () => {
  internalVisible.value = false;
  emit('update:visible', false);
  emit('close');
};
</script>

<style scoped>


.dialog-content {
  padding: 1.5rem 0; /* 1.5rem arriba/abajo, 0 en lados */
}
</style>