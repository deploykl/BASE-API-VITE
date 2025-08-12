<template>
  <div class="container-fluid">
    <ModalBase :visible="showModal" :mode="editing ? 'edit' : 'create'" entityName="tablero"
      :confirm-text="isSubmitting ? 'Guardando...' : 'Guardar'" :loading="isSubmitting" @close="closeModal"
      @confirm="handleSubmit">

      <template #content>
        <form @submit.prevent="handleSubmit" class="needs-validation" novalidate>
          <div class="row g-3">
            <!-- Columna Izquierda -->
            <div class="col-md-6">
              <!-- Nombre del tablero -->
              <div class="mb-3">
                <FloatInput id="name" label="Nombre del tablero" v-model="form.name" icon="pi pi-table" :errors="errors"
                  :invalid="!!errors.name" size="small" required />
              </div>

              <!-- URL -->
              <div class="mb-3">
                <FloatInput id="url" label="URL" v-model="form.url" type="url" icon="pi pi-link" :invalid="!!errors.url"
                  :errors="errors" size="small" placeholder="https://ejemplo.com/tablero" />
              </div>

              <!-- Fuente de datos -->
              <div class="mb-3">
                <FloatInput id="source" label="Fuente de datos" v-model="form.source" icon="pi pi-database"
                  :invalid="!!errors.source" :errors="errors" size="small" />
              </div>
            </div>

            <!-- Columna Derecha -->
            <div class="col-md-6">
              <!-- Frecuencia de actualización -->
              <div class="mb-3">
                <Select id="update_frequency" label="Frecuencia de actualización" v-model="form.update_frequency"
                  :options="frequencyOptions" optionLabel="label" optionValue="value" icon="pi pi-calendar-clock"
                  placeholder="Seleccione frecuencia" :errors="errors" :invalid="!!errors.update_frequency"
                  size="small" required/>
                <div v-if="errors.update_frequency" class="invalid-feedback d-block">
                  {{ errors.update_frequency[0] }}
                </div>
              </div>

              <!-- Última actualización -->
              <div class="mb-3">
                <label for="last_updated" class="form-label">Última actualización</label>
                <DatePicker v-model="form.last_updated" id="last_updated" dateFormat="dd/mm/yy" :showIcon="true"
                  :showTime="true" class="w-100" :class="{ 'is-invalid': !!errors.last_updated }" />
                <div v-if="errors.last_updated" class="invalid-feedback d-block">
                  {{ errors.last_updated[0] }}
                </div>
              </div>

              <!-- Descripción -->
              <div class="mb-3">
                <label for="description" class="form-label">Descripción</label>
                <Textarea v-model="form.description" id="description" rows="3" class="w-100 form-control"
                  :class="{ 'is-invalid': !!errors.description }" />
                <div v-if="errors.description" class="invalid-feedback d-block">
                  {{ errors.description[0] }}
                </div>
              </div>
            </div>
          </div>

          <!-- Switch de activo -->
          <div class="row mt-2">
            <div class="col-12">
              <div class="form-check form-switch">
                <input v-model="form.is_active" class="form-check-input" type="checkbox" id="isActiveCheck"
                  role="switch">
                <label class="form-check-label" for="isActiveCheck">Activo</label>
              </div>
            </div>
          </div>
        </form>
      </template>
    </ModalBase>
    <!-- Modal de confirmación para eliminar -->
    <ModalBase :visible="showDeleteModal" mode="delete" entityName="tablero" confirm-text="Eliminar Permanentemente"
      confirm-class="p-button-danger" :loading="isDeleting" @close="closeDeleteModal" @confirm="proceedDelete">
      <template #content>
        ¿Estás seguro de eliminar permanentemente el tablero <strong>{{ tableroToDelete?.name }}</strong>?
        <div class="alert alert-warning mt-3">
          <i class="fas fa-exclamation-triangle me-2"></i>
          Esta acción no se puede deshacer y eliminará todos los datos asociados al tablero.
        </div>
      </template>
    </ModalBase>

    <!-- Listado de usuarios -->
    <DataTableWrapper :data="tableroStore.tableros" :columns="columns" :loading="tableroStore.loading" :actions="true"
      :showCreateButton="true" title="GESTIÓN DE TABLEROS" createButtonLabel="Nuevo Tablero"
      createButtonIcon="pi pi-chart-bar" :expandable="false" @create="openCreateModal">
      <!-- sortField="is_active" :sortOrder="-1" para poner estado activo -->

      <!-- Template para full_name -->
      <template #body-full_name="{ data }">
        {{ data.name || '-' }}
      </template>
      <template #body-url="{ data }">
        <div class="d-flex justify-content-between align-items-center w-100">
          <span class="text-truncate pe-2 flex-grow-1">
            {{ truncateUrl(data.url) }}
          </span>
          <div class="d-flex gap-2">
            <Button icon="pi pi-external-link" class="p-button-sm p-button-text p-button-rounded p-button-secondary"
              v-tooltip.top="'Abrir enlace'" @click.stop="openUrl(data.url)" />
            <Button icon="pi pi-copy" class="p-button-sm p-button-text p-button-rounded p-button-secondary"
              v-tooltip.top="'Copiar enlace'" @click.stop="copyToClipboard(data.url)" />
          </div>
        </div>
      </template>
      <template #body-description="{ data }">
        {{ data.description }}
      </template>
      <template #body-source="{ data }">
        {{ data.source }}
      </template>

      <template #body-update_frequency="{ data }">
        {{ data.update_frequency }}
      </template>
      <!-- Template para created_by -->
      <template #body-created_by_username="{ data }">
        {{ data.created_by_username ? data.created_by_username : 'Sistema' }}
      </template>
      <template #body-created_at="{ data }">
        {{ formatDateTime(data.created_at) }}
      </template>
      <template #body-updated_at="{ data }">
        {{ formatDateTime(data.updated_at) }}
      </template>
      <template #body-last_updated="{ data }">
        {{ formatDateTime(data.last_updated) }}
      </template>
      <!-- Template para is_active -->
      <template #body-is_active="{ data }">
        <div class="d-flex flex-column align-items-center">
          <ToggleSwitch v-model="data.is_active" @change="tableroStore.toggleTableroStatus(data.id, data.is_active)"
            class="mb-1" />
          <span class="badge custom-badge" :class="data.is_active ? 'bg-success' : 'bg-danger'">
            {{ data.is_active ? 'Activo' : 'Inactivo' }}
          </span>
        </div>
      </template>


      <template #actions="{ data }">
        <div class="d-flex gap-1">
          <!-- Botón Editar -->
          <Button icon="pi pi-pencil" class="p-button-sm p-button-outlined p-button-rounded p-button-warning"
            v-tooltip.top="'Editar'" @click="openEditModal(data)" />

          <Button icon="pi pi-times" class="p-button-sm p-button-outlined p-button-rounded p-button-danger"
            v-tooltip.top="'Eliminar'" @click="confirmDelete(data)" />
        </div>
      </template>

    </DataTableWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch } from 'vue';

import ModalBase from '@/components/ui/ModalBase.vue';
import DataTableWrapper from '@/components/ui/DataTableWrapper.vue';
import { useTableroStore } from '@/stores/dimon/tableroStore';
import FloatInput from '@/components/widgets/FloatInput.vue';
import { useCustomToast } from "@/components/utils/toast";

const tableroStore = useTableroStore();
const errors = ref({});

const showModal = ref(false);
const showDeleteModal = ref(false);
const editing = ref(false);
const isSubmitting = ref(false);
const resetPassword = ref(false);
const tableroToDelete = ref(null);
const tableroToEdit = ref(null);
const isDeleting = ref(false);
const toast = useCustomToast();

// Definimos la estructura del formulario como constante
const FORM_STATE = {
  name: '',
  url: '',
  description: '',
  source: '',
  last_updated: '',
  update_frequency: '',
  created_by_username: '',
  created_at: '',
  updated_at: '',
  is_active: 'true',
};
// Usamos la estructura para el formulario reactivo
const form = ref({ ...FORM_STATE });

const columns = ref([
  {
    field: 'name',
    header: 'Nombre',
    sortable: true,
    filter: false,
    filterOptions: computed(() =>
      tableroStore.tableros.map(u => u.name).filter((v, i, a) => a.indexOf(v) === i)
    ),
  },
  { field: 'url', header: 'URL', bodyTemplate: true, filter: false },
  { field: 'description', header: 'DESCRIPCIÓN', bodyTemplate: true, filter: false },
  { field: 'source', header: 'FUENTES', bodyTemplate: true, filter: false },
  { field: 'update_frequency', header: 'FRECUENCIA', bodyTemplate: true, filter: false, sortable: true },
  { field: 'created_by_username', header: 'CREADO', bodyTemplate: true, filter: true },
  { field: 'last_updated', header: 'Ult. Actualización', bodyTemplate: true, filter: false },
  { field: 'created_at', header: 'F. CREACIÓN', bodyTemplate: true, filter: false, sortable: true },
  { field: 'updated_at', header: 'F. MOD', bodyTemplate: true, filter: false, sortable: true },
  { field: 'is_active', header: 'is_active', bodyTemplate: true, filter: false, sortable: true },

]);

const frequencyOptions = ref([
  { label: 'Diaria', value: 'Diaria' },
  { label: 'Semanal', value: 'Semanal' },
  { label: 'Quincenal', value: 'Quincenal' },
  { label: 'Mensual', value: 'Mensual' },
  { label: 'Trimestral', value: 'Trimestral' },
  { label: 'Semestral', value: 'Semestral' },
]);
// Métodos
const resetForm = () => {
  form.value = { ...FORM_STATE };
  resetPassword.value = false;
  errors.value = {};
};

const openCreateModal = () => {
  resetForm();
  editing.value = false;
  showModal.value = true;
};
const closeModal = () => {
  showModal.value = false;
  resetForm();
};

const confirmDelete = (user) => {
  tableroToDelete.value = user;
  showDeleteModal.value = true;
};
const closeDeleteModal = () => {
  try {
    showDeleteModal.value = false;
    // Pequeño delay para la animación antes de resetear
    setTimeout(() => {
      tableroToDelete.value = null;
    }, 300);
  } catch (error) {
    console.error("Error al cerrar modal:", error);
  }
};
const openEditModal = async (tablero) => {
  editing.value = true;
  tableroToEdit.value = tablero;

  // Resetear formulario manteniendo la reactividad
  Object.assign(form.value, FORM_STATE);

  // Asignar valores del tablero, normalizando la frecuencia
  const normalizedFrequency = frequencyOptions.value.find(
    opt => opt.value.toLowerCase() === tablero.update_frequency?.toLowerCase()
  )?.value || tablero.update_frequency;

  form.value = {
    ...form.value,
    ...tablero,
    update_frequency: normalizedFrequency, // Usar el valor normalizado
    last_updated: tablero.last_updated ? new Date(tablero.last_updated) : null
  };

  // Esperar a que el modal y los componentes estén renderizados
  await nextTick();
  showModal.value = true;

  console.log('Valor asignado a form.update_frequency:', form.value.update_frequency);
  console.log('Opciones disponibles:', frequencyOptions.value);
};

const proceedDelete = async () => {
  isDeleting.value = true;
  try {
    const success = await tableroStore.DeleteTablero(tableroToDelete.value.id);
    if (success) {
      closeDeleteModal();
    }
  } catch (error) {
  } finally {
    isDeleting.value = false;
  }
};
const handleSubmit = async () => {
  isSubmitting.value = true;
  errors.value = {}; // Limpiar errores anteriores

  // Validación manual para frecuencia de actualización
  if (!form.value.update_frequency) {
    errors.value.update_frequency = ['La frecuencia de actualización es obligatoria'];
    isSubmitting.value = false;
    return;
  }

  try {
    if (editing.value) {
      await tableroStore.UpdateTablero(tableroToEdit.value.id, form.value);
    } else {
      await tableroStore.CreateTablero(form.value);
    }
    closeModal();
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data;
    } else {
      console.error('Error al guardar:', error);
    }
  } finally {
    isSubmitting.value = false;
  }
};

// Inicialización
onMounted(async () => {
  try {
    tableroStore.loading = true;
    await tableroStore.ListTablero();
  } catch (error) {
  } finally {
    tableroStore.loading = false;
  }
});

// Método para truncar la URL
const truncateUrl = (url) => {
  if (!url) return '-';
  if (url.length <= 30) return url;
  return `${url.substring(0, 15)}...${url.substring(url.length - 10)}`;
};

// Método para abrir URL
const openUrl = (url) => {
  if (!url) return;
  window.open(url.startsWith('http') ? url : `https://${url}`, '_blank');
};

// Método para copiar al portapapeles
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    toast.showInfo('URL copiada al portapapeles', 'Copiado exitoso');
  } catch (err) {
    toast.showError('Error al copiar la URL');
  }
};
const formatDateTime = (dateString) => {
  if (!dateString) return '-';
  try {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('es-PE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
    // Resultado: 11/08/2025 10:14
  } catch {
    return dateString;
  }
};
// En tu script setup, añade este watch:
watch(
  () => form.value.source,
  (newValue) => {
    if (newValue) {
      form.value.source = newValue.toUpperCase();
    }
  }
);
</script>

<style scoped></style>