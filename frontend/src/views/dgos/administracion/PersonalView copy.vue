<template>
    <div class="personal-manager">

        <!-- Listado de usuarios -->
        <DataTableWrapper :data="personalStore.personal" :columns="columns" :loading="personalStore.loading"
            :actions="true" :showCreateButton="true" title="GESTIÓN DE PERSONAL" createButtonLabel="Nuevo Personal"
            createButtonIcon="pi pi-user" :expandable="true" @create="openCreateModal" @column-filter-change="handleFilterChange">
            <!-- sortField="is_active" :sortOrder="-1" para poner estado activo -->

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
                        <i v-if="data.sexo === 'M'" class="pi pi-mars" style="color: #007bff;font-size: 0.7rem;margin-right: 5px;" title="Masculino"></i>
                        <i v-else-if="data.sexo === 'F'" class="pi pi-venus" style="color: #e83e8c;font-size: 0.7rem;margin-right: 5px;"
                            title="Femenino"></i>
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
<template #body-acceso="{ data }">
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

            <!-- NUEVAS ACCIONES EN EL DATATABLE -->
            <template #actions="{ data }">
                <div class="d-flex gap-1">
                    <!-- Botón Editar -->
                    <Button icon="pi pi-pencil" class="p-button-sm p-button-outlined p-button-rounded p-button-warning"
                        v-tooltip.top="'Editar'" @click="openEditModal(data)" />

                    <!-- Botón Habilitar/Editar Módulos -->
                    <Button v-if="!data.acceso && data.email" icon="pi pi-check" 
                        class="p-button-sm p-button-outlined p-button-rounded p-button-success"
                        v-tooltip.top="'Habilitar acceso'" @click="openModalHabilitar(data)" />

                    <Button v-if="data.acceso" icon="pi pi-cog" 
                        class="p-button-sm p-button-outlined p-button-rounded p-button-secondary"
                        v-tooltip.top="'Editar módulos'" @click="openModalEditarModulos(data)" />

                    <!-- Botón Deshabilitar Acceso -->
                    <Button v-if="data.acceso" icon="pi pi-times" 
                        class="p-button-sm p-button-outlined p-button-rounded p-button-warning"
                        v-tooltip.top="'Deshabilitar acceso'" 
                        @click="personalStore.deshabilitarAcceso(data)" />

                    <!-- Botón Resetear Password -->
                    <Button v-if="data.acceso" icon="pi pi-key" 
                        class="p-button-sm p-button-outlined p-button-rounded p-button-info"
                        v-tooltip.top="'Resetear contraseña'" 
                        @click="personalStore.resetearPassword(data)" />

                    <!-- Botón Eliminar -->
                    <Button icon="pi pi-trash" class="p-button-sm p-button-outlined p-button-rounded p-button-danger"
                        v-tooltip.top="'Eliminar'" @click="confirmDelete(data)" />
                </div>
            </template>









            <!-- Template de expansión personalizado -->
            <template #expansion="{ data }">
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Nombre completo:</strong> {{ data.full_name || '-' }}</p>
                        <p><strong>Email:</strong> {{ data.email }}</p>
                        <p><strong>DNI:</strong> {{ data.dni || '-' }}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Celular:</strong> {{ data.celular || '-' }}</p>
                        <p><strong>Creado por:</strong> {{ data.created_by?.username || 'Sistema' }}</p>
                        <p><strong>Estado:</strong>
                            <Tag :value="data.is_active ? 'Activo' : 'Inactivo'"
                                :severity="data.is_active ? 'success' : 'danger'" />
                        </p>
                        <p><strong>is_superuser:</strong> {{ data.is_superuser || '-' }}</p>

                    </div>
                </div>

                <div class="mt-3" v-if="data.groups?.length">
                    <h6>Grupos asignados:</h6>
                    <div class="d-flex flex-wrap gap-2">
                        <Tag v-for="group in data.groups" :key="group.id" :value="group.name" severity="info" />
                    </div>
                </div>
            </template>

        </DataTableWrapper>


        <!-- Modal para habilitar/editar módulos -->
        <div class="modal fade" id="modulosModal" tabindex="-1" aria-labelledby="modulosModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modulosModalLabel">
                            {{ modalMode === 'habilitar' ? 'Habilitar acceso' : 'Editar módulos' }}
                            para {{ selectedPerson?.nombre }} {{ selectedPerson?.apellido }}
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="modulos-selection">
                            <h6>Seleccionar módulos:</h6>
                            <div v-for="modulo in modulos" :key="modulo.id" class="form-check">
                                <input class="form-check-input" type="checkbox" :id="'modulo-' + modulo.id"
                                    :value="modulo.id" v-model="selectedModulos">
                                <label class="form-check-label" :for="'modulo-' + modulo.id">
                                    {{ modulo.name || modulo.codename }} - {{ modulo.description }}
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" @click="confirmarAccionModulos"
                            :disabled="loading || selectedModulos.length === 0">
                            <span v-if="loading" class="spinner-border spinner-border-sm" role="status"
                                aria-hidden="true"></span>
                            {{ modalMode === 'habilitar' ? 'Habilitar' : 'Actualizar' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="d-flex justify-content-center align-items-center my-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
            <span class="ms-2">Cargando...</span>
        </div>

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

import { useRouter } from 'vue-router'
import { api } from "@/components/services/Axios"
import { Modal, Toast } from 'bootstrap'

const personalStore = usePersonalStore();
const errors = ref({});
const showModal = ref(false);
const showDeleteModal = ref(false);
const editing = ref(false);
const isSubmitting = ref(false);
const selectedDependencia = ref(null);
// Computed para opciones de filtro
const dependenciaOptions = computed(() => {
  return [...new Set(personalStore.personal.map(p => p.dependencia_nombre))].filter(Boolean);
});

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
    acceso: '',
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
    { field: 'acceso', header: 'ACCESO', sortable: false, bodyTemplate: true, filter: false },

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

};

// Lifecycle
onMounted(async () => {
  try {
    await personalStore.ListPersonal();
    await personalStore.ListModulos(); // Cargar módulos al inicializar
  } catch (error) {
    console.error('Error loading data:', error);
  }
});
















































const router = useRouter()

// Estados reactivos
const personal = ref([])
const modulos = ref([])
const loading = ref(false)
const searchTerm = ref('')
const filterAcceso = ref('all')
const message = ref('')
const messageType = ref('info')
const selectedPerson = ref(null)
const selectedModulos = ref([])
const modalMode = ref('habilitar') // 'habilitar' o 'editar'

// Computed
const filteredPersonal = computed(() => {
    let filtered = personal.value

    // Filtrar por búsqueda
    if (searchTerm.value) {
        const term = searchTerm.value.toLowerCase()
        filtered = filtered.filter(person =>
            person.dni?.toLowerCase().includes(term) ||
            person.nombre?.toLowerCase().includes(term) ||
            person.apellido?.toLowerCase().includes(term) ||
            (person.email && person.email.toLowerCase().includes(term))
        )
    }

    // Filtrar por estado de acceso
    if (filterAcceso.value !== 'all') {
        const accesoFilter = filterAcceso.value === 'true'
        filtered = filtered.filter(person => person.acceso === accesoFilter)
    }

    return filtered
})

// Métodos
const showMessage = (text, type = 'info') => {
    message.value = text
    messageType.value = type

    const toastEl = document.getElementById('liveToast')
    const toast = new Toast(toastEl)
    toast.show()

    setTimeout(() => {
        if (message.value === text) {
            message.value = ''
        }
    }, 5000)
}

const getModulosNames = (modulosArray) => {
    return modulosArray.map(m => m.name || m.codename).join(', ')
}

const fetchPersonal = async () => {
    loading.value = true
    try {
        const response = await api.get('/dgos/administracion/personal/')
        personal.value = response.data.map(person => ({
            ...person,
            // Asegurar que user.modulos siempre sea un array
            user: person.user ? {
                ...person.user,
                modulos: person.user.modulos || []
            } : null
        }))
        showMessage('Datos cargados correctamente', 'success')
    } catch (error) {
        console.error('Error fetching personal:', error)
        if (error.response?.status === 401) {
            showMessage('No autorizado. Por favor inicie sesión.', 'error')
            router.push('/login')
        } else {
            showMessage('Error al cargar los datos', 'error')
        }
    } finally {
        loading.value = false
    }
}

const fetchModulos = async () => {
    try {
        const response = await api.get('/user/modulo/')
        modulos.value = response.data
    } catch (error) {
        console.error('Error fetching módulos:', error)
        showMessage('Error al cargar los módulos', 'error')
    }
}

const openModalHabilitar = (person) => {
    selectedPerson.value = person
    selectedModulos.value = []
    modalMode.value = 'habilitar'

    nextTick(() => {
        const modalElement = document.getElementById('modulosModal')
        const modal = new Modal(modalElement)
        modal.show()
    })
}

const openModalEditarModulos = (person) => {
  selectedPerson.value = person;
  modalMode.value = 'editar';

  // Pre-seleccionar los módulos actuales del usuario
  if (person.user && person.user.modulos) {
    selectedModulos.value = person.user.modulos.map(modulo => modulo.id);
  } else {
    selectedModulos.value = [];
  }

  nextTick(() => {
    const modalElement = document.getElementById('modulosModal');
    const modal = new Modal(modalElement);
    modal.show();
  });
};

const confirmarAccionModulos = async () => {
  if (!selectedPerson.value) return;

  try {
    await personalStore.gestionarModulos(
      selectedPerson.value.id,
      selectedModulos.value,
      modalMode.value
    );

    // Cerrar el modal
    const modalElement = document.getElementById('modulosModal');
    const modal = Modal.getInstance(modalElement);
    modal.hide();
  } catch (error) {
    console.error('Error gestionando módulos:', error);
  }
};




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
</style>