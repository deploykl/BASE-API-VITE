<template>
    <div class="container-fluid">
        <!-- Modal para crear/editar personal -->
        <ModalBase :visible="showModal" :mode="editing ? 'edit' : 'create'" entityName="personal"
            :confirm-text="isSubmitting ? 'Guardando...' : 'Guardar'" :loading="isSubmitting" @close="closeModal"
            @confirm="handleSubmit">

            <template #content>
                <form @submit.prevent="handleSubmit" class="needs-validation" novalidate>
                    <div class="row g-3">
                        <!-- Columna Izquierda -->
                        <div class="col-md-6">
                            <!-- DNI -->
                            <div class="mb-3">
                                <FloatInput id="dni" label="DNI" v-model="form.dni" icon="pi pi-id-card"
                                    :errors="errors" :invalid="!!errors.dni" size="small" />
                            </div>

                            <!-- Nombre -->
                            <div class="mb-3">
                                <FloatInput id="nombre" label="Nombre" v-model="form.nombre" icon="pi pi-user"
                                    :errors="errors" :invalid="!!errors.nombre" size="small" required />
                            </div>

                            <!-- Email -->
                            <div class="mb-3">
                                <FloatInput id="email" label="Email" v-model="form.email" type="email"
                                    icon="pi pi-envelope" :invalid="!!errors.email" :errors="errors" size="small"
                                    required />
                            </div>

                            <!-- Dependencia -->
                            <div class="mb-3">
                                <FloatInput id="dependencia" label="Dependencia" v-model="form.dependencia"
                                    icon="pi pi-building" :invalid="!!errors.dependencia" :errors="errors"
                                    size="small" />
                            </div>
                        </div>

                        <!-- Columna Derecha -->
                        <div class="col-md-6">
                            <!-- Apellido -->
                            <div class="mb-3">
                                <FloatInput id="apellido" label="Apellido" v-model="form.apellido" icon="pi pi-user"
                                    :invalid="!!errors.apellido" :errors="errors" size="small" required />
                            </div>

                            <!-- Celular -->
                            <div class="mb-3">
                                <FloatInput id="celular" label="Celular" v-model="form.celular" icon="pi pi-phone"
                                    :invalid="!!errors.celular" :errors="errors" size="small" />
                            </div>

                            <!-- Área -->
                            <div class="mb-3">
                                <FloatInput id="area" label="Área" v-model="form.area" icon="pi pi-briefcase"
                                    :invalid="!!errors.area" :errors="errors" size="small" />
                            </div>

                            <!-- Fecha de nacimiento -->
                            <div class="mb-3">
                                <label for="fecha_nac" class="form-label">Fecha de Nacimiento</label>
                                <DatePicker v-model="form.fecha_nac" id="fecha_nac" dateFormat="dd/mm/yy"
                                    :showIcon="true" class="w-100" :class="{ 'is-invalid': !!errors.fecha_nac }" />
                                <div v-if="errors.fecha_nac" class="invalid-feedback d-block">
                                    {{ errors.fecha_nac[0] }}
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Switch de activo -->
                    <div class="row mt-2">
                        <div class="col-12">
                            <div class="form-check form-switch">
                                <input v-model="form.is_active" class="form-check-input" type="checkbox"
                                    id="isActiveCheck" role="switch">
                                <label class="form-check-label" for="isActiveCheck">Activo</label>
                            </div>
                        </div>
                    </div>
                </form>
            </template>
        </ModalBase>

        <!-- Modal de confirmación para eliminar -->
        <ModalBase :visible="showDeleteModal" mode="delete" entityName="personal"
            confirm-text="Eliminar Permanentemente" confirm-class="p-button-danger" :loading="isDeleting"
            @close="closeDeleteModal" @confirm="proceedDelete">
            <template #content>
                ¿Estás seguro de eliminar permanentemente al personal <strong>{{ personalToDelete?.nombre }} {{
                    personalToDelete?.apellido }}</strong>?
                <div class="alert alert-warning mt-3">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Esta acción no se puede deshacer y eliminará todos los datos asociados.
                </div>
            </template>
        </ModalBase>

        <!-- Modal para habilitar/editar módulos -->
        <ModalBase :visible="showModulosModal" :mode="modalMode === 'habilitar' ? 'create' : 'edit'"
            :entityName="modalMode === 'habilitar' ? 'acceso' : 'módulos'"
            :confirm-text="isProcessingModulos ? 'Procesando...' : (modalMode === 'habilitar' ? 'Habilitar' : 'Actualizar')"
            :loading="isProcessingModulos" @close="closeModulosModal" @confirm="confirmarAccionModulos"
            :width="'600px'">

            <template #content>
                <div class="modulos-selection">
                    <h6>Seleccionar módulos para {{ selectedPerson?.nombre }} {{ selectedPerson?.apellido }}:</h6>
                    <div class="modulos-list" style="max-height: 300px; overflow-y: auto;">
                        <!-- Spinner de carga cuando se están cargando los módulos -->
                        <div v-if="personalStore.loading" class="text-center py-4">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Cargando módulos...</span>
                            </div>
                            <p class="mt-2 text-muted">Cargando módulos...</p>
                        </div>

                        <!-- Lista de módulos cuando ya están cargados -->
                        <div v-else>
                            <div v-for="modulo in personalStore.modulos" :key="modulo.id" class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" :id="'modulo-' + modulo.id"
                                    :value="modulo.id" v-model="selectedModulos" :disabled="isProcessingModulos">
                                <label class="form-check-label" :for="'modulo-' + modulo.id">
                                    <strong>{{ modulo.name || modulo.codename }}</strong> - {{ modulo.description }}
                                </label>
                            </div>

                            <div v-if="personalStore.modulos.length === 0" class="text-center py-3 text-muted">
                                No hay módulos disponibles
                            </div>
                        </div>
                    </div>

                    <div v-if="selectedModulos.length === 0 && !personalStore.loading" class="alert alert-info mt-3">
                        <i class="pi pi-info-circle me-2"></i>
                        Debe seleccionar al menos un módulo
                    </div>
                </div>
            </template>
        </ModalBase>

        <!-- Listado de personal -->
        <DataTableWrapper :data="personalStore.personal" :columns="columns" :loading="personalStore.loading"
            :actions="true" :showCreateButton="true" title="GESTIÓN DE PERSONAL" createButtonLabel="Nuevo Personal"
            createButtonIcon="pi pi-user" :expandable="true" @create="openCreateModal"
            @column-filter-change="handleFilterChange">

            <template #body-dni="{ data }">
                {{ data.dni || '-' }}
            </template>
            <template #body-ruc="{ data }">
                {{ data.ruc || '-' }}
            </template>
            <template #body-full_name="{ data }">
                {{ data.full_name || '-' }}
            </template>
            <template #body-sexo="{ data }">
                <div class="sexo-container">
                    <span v-if="!data.sexo">-</span>
                    <div v-else class="sexo-content">
                        <i v-if="data.sexo === 'M'" class="pi pi-mars"
                            style="color: #007bff;font-size: 0.7rem;margin-right: 5px;" title="Masculino"></i>
                        <i v-else-if="data.sexo === 'F'" class="pi pi-venus"
                            style="color: #e83e8c;font-size: 0.7rem;margin-right: 5px;" title="Femenino"></i>
                        <span class="sexo-text">{{ data.sexo }}</span>
                    </div>
                </div>
            </template>
            <template #body-fecha_nac="{ data }">
                <div>
                    {{ data.fecha_nac || '-' }}
                    <span v-if="data.edad" style="font-size:0.7rem;color: #666; margin-left: 5px;">
                        ({{ data.edad }} años)
                    </span>
                </div>
            </template>
            <template #body-celular="{ data }">
                <div class="celular-container">
                    <a v-if="data.celular" :href="`https://wa.me/51${data.celular}`" target="_blank"
                        class="whatsapp-link" title="Enviar mensaje por WhatsApp">
                        <i class="pi pi-whatsapp" style="color: #25D366; margin-right: 5px;"></i>
                    </a>
                    <span class="numero">{{ data.celular || '-' }}</span>
                </div>
            </template>
            <template #body-email="{ data }">
                {{ data.email }}
            </template>
            <template #body-dependencia_nombre="{ data }">
                {{ data.dependencia_nombre || '-' }}
            </template>
            <template #body-area_nombre="{ data }">
                {{ data.area_nombre || '-' }}
            </template>
            <template v-if="isSuperuser" #body-acceso="{ data }">
                <!-- Habilitado -->
                <Badge v-if="data.acceso === true" severity="success" class="p-2">
                    <i class="pi pi-check-circle"></i>
                </Badge>

                <!-- Deshabilitado -->
                <Badge v-else-if="data.acceso === false" severity="danger" class="p-2">
                    <i class="pi pi-times-circle"></i>
                </Badge>

                <!-- Vacío / nulo -->
                <Badge v-else severity="secondary" class="p-2">
                    <i class="pi pi-minus-circle"></i>
                </Badge>
            </template>

            <template #actions="{ data }">
                <div class="d-flex flex-wrap align-items-center justify-content-center gap-1">
                    <!-- Botón Habilitar/Editar Módulos (solo para superusuarios) -->
                    <Button v-if="isSuperuser && !data.acceso && data.email" icon="pi pi-check"
                        class="p-button-sm p-button-outlined p-button-rounded p-button-success"
                        v-tooltip.top="'Habilitar acceso'" @click="openModalHabilitar(data)" />

                    <Button v-if="isSuperuser && data.acceso" icon="pi pi-cog"
                        class="p-button-sm p-button-outlined p-button-rounded p-button-secondary"
                        v-tooltip.top="'Editar módulos'" @click="openModalEditarModulos(data)" />

                    <!-- Botón Deshabilitar Acceso (solo para superusuarios) -->
                    <Button v-if="isSuperuser && data.acceso" icon="pi pi-times"
                        class="p-button-sm p-button-outlined p-button-rounded p-button-warning"
                        v-tooltip.top="'Deshabilitar acceso'" @click="deshabilitarAcceso(data)" />

                    <!-- Botón Resetear Password (solo para superusuarios) -->
                    <Button v-if="isSuperuser && data.acceso" icon="pi pi-key"
                        class="p-button-sm p-button-outlined p-button-rounded p-button-info"
                        v-tooltip.top="'Resetear contraseña'" @click="resetearPassword(data)" />

                    <!-- Botones para todos los usuarios -->
                    <Button icon="pi pi-pencil" class="p-button-sm p-button-outlined p-button-rounded p-button-warning"
                        v-tooltip.top="'Editar'" @click="openEditModal(data)" />

                    <Button icon="pi pi-trash" class="p-button-sm p-button-outlined p-button-rounded p-button-danger"
                        v-tooltip.top="'Eliminar'" @click="confirmDelete(data)" />
                </div>
            </template>

<template #expansion="{ data }">
  <div class="expansion-content p-4">
    <div class="row">
      <!-- Columna 1: Información personal -->
      <div class="col-12 col-md-6 col-lg-3 mb-3">
        <div class="expansion-card p-3 h-100">
          <div class="d-flex align-items-center mb-3">
            <i class="pi pi-user text-primary me-2" style="font-size: 1.35rem;"></i>
            <h6 class="m-0 text-900 fw-semibold">Información Personal</h6>
          </div>
          <div class="field mb-3">
            <label class="text-600 small fw-medium">Nombre completo</label>
            <p class="m-0 text-900 fw-medium">{{ data.full_name || '-' }}</p>
          </div>
          <div class="field mb-3">
            <label class="text-600 small fw-medium">Email</label>
            <p class="m-0 text-900 fw-medium">{{ data.email }}</p>
          </div>
          <div class="field">
            <label class="text-600 small fw-medium">DNI</label>
            <p class="m-0 text-900 fw-medium">{{ data.dni || '-' }}</p>
          </div>
        </div>
      </div>

      <!-- Columna 2: Contacto y estado -->
      <div class="col-12 col-md-6 col-lg-3 mb-3">
        <div class="expansion-card p-3 h-100">
          <div class="d-flex align-items-center mb-3">
            <i class="pi pi-phone text-primary me-2" style="font-size: 1.35rem;"></i>
            <h6 class="m-0 text-900 fw-semibold">Contacto</h6>
          </div>
          <div class="field mb-3">
            <label class="text-600 small fw-medium">Celular</label>
            <div class="d-flex align-items-center">
              <a v-if="data.celular" :href="`https://wa.me/51${data.celular}`" target="_blank"
                class="me-2 text-success">
                <i class="pi pi-whatsapp"></i>
              </a>
              <p class="m-0 text-900 fw-medium">{{ data.celular || '-' }}</p>
            </div>
          </div>
          <div class="field">
            <label class="text-600 small fw-medium">Estado</label>
            <Tag :value="data.is_active ? 'Activo' : 'Inactivo'"
                 :severity="data.is_active ? 'success' : 'danger'" 
                 class="custom-tag" />
          </div>
        </div>
      </div>

      <!-- Columna 3: Información del sistema -->
      <div class="col-12 col-md-6 col-lg-3 mb-3">
        <div class="expansion-card p-3 h-100">
          <div class="d-flex align-items-center mb-3">
            <i class="pi pi-cog text-primary me-2" style="font-size: 1.35rem;"></i>
            <h6 class="m-0 text-900 fw-semibold">Sistema</h6>
          </div>
          <div class="field mb-3">
            <label class="text-600 small fw-medium">Creado por</label>
            <p class="m-0 text-900 fw-medium">{{ data.created_by?.username || 'Sistema' }}</p>
          </div>
          <div class="field">
            <label class="text-600 small fw-medium">Superusuario</label>
            <Tag :value="data.is_superuser ? 'Sí' : 'No'" 
                 :severity="data.is_superuser ? 'warning' : 'secondary'"
                 class="custom-tag" />
          </div>
        </div>
      </div>

      <!-- Columna 4: Grupos -->
      <div class="col-12 col-md-6 col-lg-3 mb-3">
        <div class="expansion-card p-3 h-100">
          <div class="d-flex align-items-center mb-3">
            <i class="pi pi-users text-primary me-2" style="font-size: 1.35rem;"></i>
            <h6 class="m-0 text-900 fw-semibold">Grupos</h6>
          </div>
          <div v-if="data.groups?.length" class="field">
            <label class="text-600 small fw-medium mb-2">Grupos asignados</label>
            <div class="d-flex flex-wrap gap-1">
              <Chip v-for="group in data.groups" :key="group.id" 
                    :label="group.name" 
                    class="custom-chip" />
            </div>
          </div>
          <div v-else class="field">
            <p class="text-600 small m-0">No tiene grupos asignados</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
        </DataTableWrapper>

        <!-- Toast para mensajes de estado -->
        <div class="toast-container position-fixed top-0 end-0 p-3">
            <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header"
                    :class="{ 'bg-success': messageType === 'success', 'bg-danger': messageType === 'error', 'bg-info': messageType === 'info' }">
                    <strong class="me-auto text-white">{{ messageType === 'success' ? 'Éxito' : messageType === 'error'
                        ? 'Error' : 'Información' }}</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    {{ message }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import DataTableWrapper from '@/components/ui/DataTableWrapper.vue';
import { usePersonalStore } from '@/stores/dgos/personalStore';
import FloatInput from '@/components/widgets/FloatInput.vue';
import ModalBase from '@/components/ui/ModalBase.vue';
import DatePicker from 'primevue/datepicker';
import { useRouter } from 'vue-router'
import { api } from "@/components/services/Axios"
import { useToast } from 'primevue/usetoast';

const personalStore = usePersonalStore();
const toast = useToast();
const router = useRouter();

const errors = ref({});
const showModal = ref(false);
const showDeleteModal = ref(false);
const showModulosModal = ref(false);
const editing = ref(false);
const isSubmitting = ref(false);
const personalToDelete = ref(null);
const personalToEdit = ref(null);
const isDeleting = ref(false);
const selectedDependencia = ref(null);
const selectedPerson = ref(null);
const selectedModulos = ref([]);
const modalMode = ref('habilitar');
const message = ref('');
const messageType = ref('info');

// Computed para opciones de filtro
const dependenciaOptions = computed(() => {
    return [...new Set(personalStore.personal.map(p => p.dependencia_nombre))].filter(Boolean);
});

const isSuperuser = computed(() => {
    return localStorage.getItem('is_superuser') === 'true'
})

const areaOptions = computed(() => {
    if (!selectedDependencia.value) {
        return [...new Set(personalStore.personal.map(p => p.area_nombre))].filter(Boolean);
    }

    return personalStore.personal
        .filter(p => p.dependencia_nombre === selectedDependencia.value)
        .map(p => p.area_nombre)
        .filter((v, i, a) => a.indexOf(v) === i && v !== null);
});

// Definimos la estructura del formulario como constante
const FORM_STATE = {
    dni: '',
    ruc: '',
    nombre: '',
    apellido: '',
    email: '',
    dependencia: '',
    area: '',
    fecha_nac: '',
    fecha_inicio: '',
    salario: '',
    sexo: '',
    is_active: true,
};

// Usamos la estructura para el formulario reactivo
const form = ref({ ...FORM_STATE });

// Columnas con filtros dependientes
const columns = ref([
    { field: 'dni', header: 'DNI', bodyTemplate: true, filter: false },
    { field: 'ruc', header: 'RUC', bodyTemplate: true, filter: false },
    { field: 'full_name', header: 'NOMBRE COMPLETO', sortable: true, bodyTemplate: true, filter: false },
    { field: 'sexo', header: 'SEXO', sortable: true, bodyTemplate: true, filter: false },
    { field: 'fecha_nac', header: 'F.NACIMIENTO', sortable: true, bodyTemplate: true, filter: false },
    { field: 'celular', header: 'CELULAR', sortable: false, bodyTemplate: true, filter: false },
    { field: 'email', header: 'EMAIL', sortable: false, bodyTemplate: true, filter: false },
    {
        field: 'dependencia_nombre',
        header: 'DEPENDENCIA',
        sortable: true,
        bodyTemplate: true,
        filter: true,
        filterOptions: dependenciaOptions
    },
    {
        field: 'area_nombre',
        header: 'AREA',
        sortable: true,
        bodyTemplate: true,
        filter: true,
        filterOptions: areaOptions
    },
]);

// Manejar cambios de filtro
const handleFilterChange = (event) => {
    if (event.field === 'dependencia_nombre') {
        selectedDependencia.value = event.value;
        personalStore.setSelectedDependencia(event.value);
    }
};

// Métodos
const resetForm = () => {
    form.value = { ...FORM_STATE };
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
    personalToDelete.value = user;
    showDeleteModal.value = true;
};

const closeDeleteModal = () => {
    showDeleteModal.value = false;
    personalToDelete.value = null;
};

const openEditModal = async (personal) => {
    editing.value = true;
    personalToEdit.value = personal;

    // Resetear formulario manteniendo la reactividad
    Object.assign(form.value, FORM_STATE);

    // Llenar el formulario con los datos del personal
    form.value = {
        ...form.value,
        ...personal,
    };

    showModal.value = true;
};

const proceedDelete = async () => {
    isDeleting.value = true;
    try {
        const success = await personalStore.DeletePersonal(personalToDelete.value.id);
        if (success) {
            closeDeleteModal();
        }
    } catch (error) {
        console.error('Error al eliminar:', error);
    } finally {
        isDeleting.value = false;
    }
};

const handleSubmit = async () => {
    isSubmitting.value = true;
    errors.value = {};

    try {
        if (editing.value) {
            await personalStore.UpdatePersonal(personalToEdit.value.id, form.value);
        } else {
            await personalStore.CreatePersonal(form.value);
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

// Métodos para gestión de módulos
const openModalHabilitar = (person) => {
    selectedPerson.value = person;
    selectedModulos.value = [];
    modalMode.value = 'habilitar';
    showModulosModal.value = true;
};

const openModalEditarModulos = (person) => {
    selectedPerson.value = person;
    modalMode.value = 'editar';

    // Pre-seleccionar los módulos actuales del usuario
    if (person.user && person.user.modulos) {
        selectedModulos.value = person.user.modulos.map(modulo => modulo.id);
    } else {
        selectedModulos.value = [];
    }

    showModulosModal.value = true;
};

const closeModulosModal = () => {
    showModulosModal.value = false;
    selectedPerson.value = null;
    selectedModulos.value = [];
};

const confirmarAccionModulos = async () => {
    if (!selectedPerson.value || selectedModulos.value.length === 0) return;

    try {
        await personalStore.gestionarModulos(
            selectedPerson.value.id,
            selectedModulos.value,
            modalMode.value
        );

        closeModulosModal();
    } catch (error) {
        console.error('Error gestionando módulos:', error);
    }
};

const deshabilitarAcceso = async (person) => {
    if (!confirm(`¿Deshabilitar acceso a ${person.nombre} ${person.apellido}?`)) {
        return;
    }

    try {
        await personalStore.deshabilitarAcceso(person);
    } catch (error) {
        console.error('Error al deshabilitar acceso:', error);
    }
};

const resetearPassword = async (person) => {
    if (!confirm(`¿Resetear contraseña de ${person.nombre} ${person.apellido}?`)) {
        return;
    }

    try {
        await personalStore.resetearPassword(person);
    } catch (error) {
        console.error('Error al resetear contraseña:', error);
    }
};

// Lifecycle
onMounted(async () => {
    try {
        await personalStore.ListPersonal();
        await personalStore.ListModulos();
    } catch (error) {
        console.error('Error loading data:', error);
    }
});
</script>

<style scoped>
.personal-manager {
    padding: 20px;
}

.modal-body {
    max-height: 60vh;
    overflow-y: auto;
}

.btn-group {
    flex-wrap: wrap;
    gap: 5px;
}

.form-check {
    margin-bottom: 8px;
}

.form-check-label {
    margin-left: 5px;
}

.modulos-list {
    border: 1px solid #dee2e6;
    border-radius: 5px;
    padding: 10px;
}
.expansion-content {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
}

.expansion-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  height: 100%;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.expansion-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #3B82F6, #6366F1);
}

.expansion-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.custom-tag {
  border-radius: 20px;
  font-weight: 600;
  padding: 0.35rem 0.75rem;
  font-size: 0.85rem;
}

.custom-chip {
  background: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%);
  color: white;
  border-radius: 20px;
  font-weight: 500;
  font-size: 0.85rem;
  padding: 0.5rem 0.75rem;
}

.field {
  margin-bottom: 1.2rem;
  padding: 0.5rem 0;
}

.field:last-child {
  margin-bottom: 0;
}

.text-xl {
  font-size: 1.35rem;
}

.font-semibold {
  font-weight: 600;
  color: #1f2937;
}

.h-full {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.expansion-card .field label {
  display: block;
  margin-bottom: 0.35rem;
  color: #6b7280;
  font-weight: 500;
  font-size: 0.9rem;
}

.expansion-card .field p {
  color: #374151;
  font-weight: 500;
  font-size: 0.95rem;
  line-height: 1.4;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .expansion-card {
    margin-bottom: 1rem;
  }
  
  .expansion-card:last-child {
    margin-bottom: 0;
  }
}
</style>