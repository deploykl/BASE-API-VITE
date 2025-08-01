<template>
  <Dialog
    v-model:visible="internalVisible"
    :modal="true"
    :style="{ width: width }"
    :header="dynamicTitle"
    :breakpoints="{ '960px': '75vw', '640px': '90vw' }"
    @hide="handleClose"
  >
    <div class="dialog-content">
      <slot name="content"></slot>
    </div>
    
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
import { ref, watch, computed } from 'vue';

const props = defineProps({
  visible: Boolean,
  title: String,
  mode: {
    type: String,
    default: 'create',
    validator: value => ['create', 'edit', 'delete', 'view', 'custom'].includes(value)
  },
  entityName: {
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
  loading: Boolean,
  hideFooter: Boolean
});

const emit = defineEmits(['update:visible', 'close', 'confirm']);

const internalVisible = ref(props.visible);

const dynamicTitle = computed(() => {
  const titles = {
    create: `Crear ${props.entityName}`,
    edit: `Editar ${props.entityName}`,
    delete: `Eliminar ${props.entityName}`,
    view: `Detalles de ${props.entityName}`
  };
  return props.title || titles[props.mode] || props.entityName;
});

watch(() => props.visible, (newVal) => {
  internalVisible.value = newVal;
});

const handleConfirm = () => {
  emit('confirm');
};

const handleClose = () => {
  internalVisible.value = false;
  emit('update:visible', false);
  emit('close');
};
</script>

<style scoped>
.dialog-content {
  padding: 1.5rem 0;
}
</style>