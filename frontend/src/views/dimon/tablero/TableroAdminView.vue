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

              <!-- Selección de Fuentes -->
              <div class="mb-3">
                <label for="fuentes" class="form-label">Fuentes relacionadas</label>
                <MultiSelect v-model="selectedFuentes" :options="tableroStore.fuentesOptions" optionLabel="label"
                  optionValue="value" placeholder="Seleccione las fuentes" :maxSelectedLabels="3" class="w-100"
                  :class="{ 'is-invalid': !!errors.fuentes }" />
                <div v-if="errors.fuentes" class="invalid-feedback d-block">
                  {{ errors.fuentes[0] }}
                </div>
                <small class="text-muted">Seleccione una o más fuentes de datos</small>
              </div>
            </div>

            <!-- Columna Derecha -->
            <div class="col-md-6">
              <!-- Frecuencia de actualización -->
              <div class="mb-3">
                <Select id="update_frequency" label="Frecuencia de actualización" v-model="form.update_frequency"
                  :options="frequencyOptions" optionLabel="label" optionValue="value" icon="pi pi-calendar-clock"
                  placeholder="Seleccione frecuencia" :errors="errors" :invalid="!!errors.update_frequency" size="small"
                  required />
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

    <!-- Listado de tableros -->
    <DataTableWrapper :data="tableroStore.tableros" :columns="columns" :loading="tableroStore.loading" :actions="true"
      :showCreateButton="true" title="GESTIÓN DE TABLEROS" createButtonLabel="Nuevo Tablero"
      createButtonIcon="pi pi-chart-bar" :expandable="false" @create="openCreateModal">

      <!-- Template para nombre -->
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
              v-tooltip.top="'Copiar enlace'" @click.stop="copyToClipboard(data.url, true, toast)" />
          </div>
        </div>
      </template>

      <template #body-description="{ data }">
        {{ data.description || '-' }}
      </template>

      <template #body-source="{ data }">
        {{ data.source || '-' }}
      </template>

<template #body-fuentes="{ data }">
  <div v-if="data.fuentes_detalles && data.fuentes_detalles.length">
    <Badge v-for="fuente in data.fuentes_detalles.slice(0, 3)" :key="fuente.id" 
           :value="`${fuente.nombre} - ${fuente.frecuencia || 'N/A'}`" 
           class="me-1 mb-1" severity="info" />
    <Badge v-if="data.fuentes_detalles.length > 3" 
           :value="`+${data.fuentes_detalles.length - 3}`" 
           severity="secondary"
           v-tooltip.top="`${data.fuentes_detalles.length - 3} fuentes adicionales`" />
  </div>
  <span v-else class="text-muted">-</span>
</template>

      <template #body-update_frequency="{ data }">
        {{ data.update_frequency || '-' }}
      </template>

      <template #body-created_by_username="{ data }">
        {{ data.created_by_username ? data.created_by_username : 'Sistema' }}
      </template>

      <template #body-updated_at="{ data }">
        {{ formatDateTime(data.updated_at) }}
      </template>

      <template #body-last_updated="{ data }">
        {{ formatDateTime(data.last_updated) }}
      </template>

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
          <Button v-if="isOwner(data)" icon="pi pi-pencil"
            class="p-button-sm p-button-outlined p-button-rounded p-button-warning" v-tooltip.top="'Editar'"
            @click="openEditModal(data)" />

          <Button v-if="isOwner(data)" icon="pi pi-trash"
            class="p-button-sm p-button-outlined p-button-rounded p-button-danger" v-tooltip.top="'Eliminar'"
            @click="confirmDelete(data)" />

          <span v-else class="text-muted small">
            <i class="pi pi-lock"></i> Solo el creador
          </span>
        </div>
      </template>

    </DataTableWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch, onUnmounted } from 'vue';
import MultiSelect from 'primevue/multiselect';
import ToggleSwitch from 'primevue/toggleswitch';

import ModalBase from '@/components/ui/ModalBase.vue';
import DataTableWrapper from '@/components/ui/DataTableWrapper.vue';
import { useTableroStore } from '@/stores/dimon/tableroStore';
import FloatInput from '@/components/widgets/FloatInput.vue';
import { formatDateTime, copyToClipboard } from '@/components/utils/format';
import { useCustomToast } from "@/components/utils/toast";

const tableroStore = useTableroStore();
const toast = useCustomToast();

// Estados reactivos
const showModal = ref(false);
const showDeleteModal = ref(false);
const editing = ref(false);
const isSubmitting = ref(false);
const isDeleting = ref(false);
const tableroToDelete = ref(null);
const tableroToEdit = ref(null);
const errors = ref({});
const selectedFuentes = ref([]);
const fuentesOptions = ref([]);

// Estructura del formulario
const FORM_STATE = {
  name: '',
  url: '',
  description: '',
  source: '',
  last_updated: '',
  update_frequency: '',
  is_active: true,
  fuentes: []
};

const form = ref({ ...FORM_STATE });

// Opciones de frecuencia
const frequencyOptions = ref([
  { label: 'Diaria', value: 'Diaria' },
  { label: 'Semanal', value: 'Semanal' },
  { label: 'Quincenal', value: 'Quincenal' },
  { label: 'Mensual', value: 'Mensual' },
  { label: 'Trimestral', value: 'Trimestral' },
  { label: 'Semestral', value: 'Semestral' },
  { label: 'Anual', value: 'Anual' }
]);

// Columnas de la tabla
const columns = ref([
  { field: 'name', header: 'Nombre', sortable: true, filter: false },
  { field: 'url', header: 'URL', bodyTemplate: true, filter: false },
  { field: 'description', header: 'DESCRIPCIÓN', bodyTemplate: true, filter: false },
  { field: 'fuentes', header: 'FUENTES', bodyTemplate: true, filter: false },
  { field: 'update_frequency', header: 'FRECUENCIA', bodyTemplate: true, filter: false, sortable: true },
  { field: 'created_by_username', header: 'CREADO', bodyTemplate: true, filter: true },
  { field: 'last_updated', header: 'Ult. Actualización', bodyTemplate: true, filter: false },
  { field: 'updated_at', header: 'F. MOD', bodyTemplate: true, filter: false, sortable: true },
  { field: 'is_active', header: 'ESTADO', bodyTemplate: true, filter: false, sortable: true },
]);

// Métodos
const resetForm = () => {
  form.value = { ...FORM_STATE };
  selectedFuentes.value = [];
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

const confirmDelete = (tablero) => {
  tableroToDelete.value = tablero;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  setTimeout(() => {
    tableroToDelete.value = null;
  }, 300);
};

const openEditModal = async (tablero) => {
  editing.value = true;
  tableroToEdit.value = tablero;

  // Resetear formulario
  Object.assign(form.value, FORM_STATE);

  // Asignar valores del tablero
  const normalizedFrequency = frequencyOptions.value.find(
    opt => opt.value.toLowerCase() === tablero.update_frequency?.toLowerCase()
  )?.value || tablero.update_frequency;

  form.value = {
    ...form.value,
    ...tablero,
    update_frequency: normalizedFrequency,
    last_updated: tablero.last_updated ? new Date(tablero.last_updated) : null,
    is_active: tablero.is_active !== undefined ? tablero.is_active : true
  };

  // Cargar fuentes seleccionadas
  selectedFuentes.value = tablero.fuentes_ids || tablero.fuentes_detalles?.map(f => f.id) || [];

  await nextTick();
  showModal.value = true;
};

const proceedDelete = async () => {
  isDeleting.value = true;
  try {
    const success = await tableroStore.DeleteTablero(tableroToDelete.value.id);
    if (success) {
      closeDeleteModal();
      toast.showSuccess('Tablero eliminado correctamente');
    }
  } catch (error) {
    toast.showError('Error al eliminar el tablero');
  } finally {
    isDeleting.value = false;
  }
};

const handleSubmit = async () => {
  isSubmitting.value = true;
  errors.value = {};

  // Validaciones
  if (!form.value.update_frequency) {
    errors.value.update_frequency = ['La frecuencia de actualización es obligatoria'];
    isSubmitting.value = false;
    return;
  }

  try {
    const dataToSend = {
      ...form.value,
      fuentes: selectedFuentes.value
    };

    if (editing.value) {
      await tableroStore.UpdateTablero(tableroToEdit.value.id, dataToSend);
      toast.showSuccess('Tablero actualizado correctamente');
    } else {
      await tableroStore.CreateTablero(dataToSend);
      toast.showSuccess('Tablero creado correctamente');
    }
    closeModal();
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data;
    } else {
      toast.showError('Error al guardar el tablero');
    }
  } finally {
    isSubmitting.value = false;
  }
};

const truncateUrl = (url) => {
  if (!url) return '-';
  if (url.length <= 30) return url;
  return `${url.substring(0, 15)}...${url.substring(url.length - 10)}`;
};

const openUrl = (url) => {
  if (!url) return;
  window.open(url.startsWith('http') ? url : `https://${url}`, '_blank');
};

const isOwner = (tablero) => {
  try {
    const currentUserId = localStorage.getItem('user_id');
    if (!currentUserId) return false;

    const userId = parseInt(currentUserId);
    const isSuperuser = localStorage.getItem('is_superuser') === 'true';
    if (isSuperuser) return true;

    if (tablero.created_by_id) {
      return tablero.created_by_id === userId;
    }

    if (tablero.created_by && typeof tablero.created_by === 'number') {
      return tablero.created_by === userId;
    }

    if (tablero.created_by && typeof tablero.created_by === 'object') {
      return tablero.created_by.id === userId;
    }

    const currentUsername = localStorage.getItem('username');
    if (currentUsername && tablero.created_by_username) {
      return tablero.created_by_username === currentUsername;
    }

    return false;
  } catch (error) {
    console.error('Error verificando propiedad:', error);
    return false;
  }
};


// Watchers
watch(
  () => form.value.source,
  (newValue) => {
    if (newValue) {
      form.value.source = newValue.toUpperCase();
    }
  }
);

// Lifecycle hooks
onMounted(async () => {
  try {
    tableroStore.loading = true;
    await tableroStore.ListTablero();
    await tableroStore.loadFuentesOptions(); // This now properly updates the store

    // No need to reassign, the store's reactive reference is already updated
  } catch (error) {
    console.error('Error inicializando:', error);
  } finally {
    tableroStore.loading = false;
  }
});

onUnmounted(() => {
  tableroStore.cleanupWebSocket();
});
</script>

<style scoped>
.p-multiselect {
  width: 100%;
}

.custom-badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
}

.text-truncate {
  max-width: 200px;
}
</style>