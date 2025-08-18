<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Gestión de Comisiones</h1>
    </div>

    <!-- Listado de usuarios -->
    <DataTableWrapper :data="comisionStore.comision" :columns="columns" :loading="comisionStore.loading" :actions="true"
      :showCreateButton="true" title="GESTIÓN DE COMISIÓN" createButtonLabel="Nueva Salida"
      createButtonIcon="pi pi-chart-bar" :expandable="false" @create="openCreateModal">
      <!-- sortField="is_active" :sortOrder="-1" para poner estado activo -->

      <!-- Template para full_name -->
      <template #body-ipress_nombre="{ data }">
        {{ data.ipress_nombre }}
      </template>
      <template #body-fecha_salida="{ data }">
        {{ formatDateTime(data.fecha_salida) }}
      </template>
      <template #body-fecha_retorno="{ data }">
        {{ formatDateTime(data.fecha_retorno) }}
      </template>

      <template #body-participantes="{ data }">
        {{ data.participantes }}
      </template>
      <template #body-conductor_nombre="{ data }">
        {{ data.conductor_nombre }}
      </template>

      <template #body-update_frequency="{ data }">
        {{ data.update_frequency }}
      </template>
      <!-- Template para created_by -->
      <template #body-created_by_username="{ data }">
        {{ data.created_by_username ? data.created_by_username : 'Sistema' }}
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
          <ToggleSwitch v-model="data.is_active" @change="comisionStore.togglecomisiontatus(data.id, data.is_active)"
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

    <CalendarView ref="calendarViewRef" />


    <ModalBase :visible="showModal" :mode="form.id ? 'edit' : 'create'" entityName="comisión"
      :confirm-text="isSubmitting ? 'Guardando...' : 'Guardar'" :loading="isSubmitting" @close="closeModal"
      @confirm="handleSubmit">
      <template #content>
        <form @submit.prevent="saveComision" class="needs-validation" novalidate>
          <div class="row g-3">
            <!-- Columna Izquierda -->
            <div class="col-md-6">
              <!-- Vehículo -->
              <div class="mb-3">
                <label class="form-label">Vehículo *</label>
                <select v-model="form.vehiculo" class="form-select" :class="{ 'is-invalid': !!errors.vehiculo }"
                  required>
                  <option value="">Seleccione un vehículo</option>
                  <option v-for="vehiculo in comisionStore.vehiculos" :key="vehiculo.id" :value="vehiculo.id">
                    {{ vehiculo.marca }} {{ vehiculo.modelo }} - {{ vehiculo.placa }}
                    <span v-if="vehiculo.estado">({{ vehiculo.estado }})</span>
                  </option>
                </select>
                <div v-if="errors.vehiculo" class="invalid-feedback d-block">
                  {{ errors.vehiculo[0] }}
                </div>
              </div>

              <!-- Conductor -->
              <div class="col-md-6">
                <label class="form-label">Conductor *</label>
                <select v-model="form.conductor" class="form-select" :class="{ 'is-invalid': !!errors.conductor }"
                  required>
                  <option value="">Seleccione un conductor</option>
                  <option v-for="conductor in comisionStore.conductores" :key="conductor.id" :value="conductor.id">
                    {{ conductor.apellido }}, {{ conductor.nombre }} ({{ conductor.dni }})
                  </option>
                </select>
                <div v-if="errors.conductor" class="invalid-feedback d-block">
                  {{ errors.conductor[0] }}
                </div>
              </div>

              <!-- Fechas -->
              <div class="mb-3">
                <label class="form-label">Fecha de Salida *</label>
                <input v-model="form.fecha_salida" type="datetime-local" class="form-control"
                  :class="{ 'is-invalid': !!errors.fecha_salida }" required>
                <div v-if="errors.fecha_salida" class="invalid-feedback d-block">
                  {{ errors.fecha_salida[0] }}
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Fecha de Retorno *</label>
                <input v-model="form.fecha_retorno" type="datetime-local" class="form-control"
                  :class="{ 'is-invalid': !!errors.fecha_retorno }" required>
                <div v-if="errors.fecha_retorno" class="invalid-feedback d-block">
                  {{ errors.fecha_retorno[0] }}
                </div>
              </div>
            </div>

            <!-- Columna Derecha -->
            <div class="col-md-6">
              <!-- IPRESS -->
              <div class="mb-3">
                <label class="form-label">Nombre IPRESS *</label>
                <input v-model="form.ipress_nombre" type="text" class="form-control"
                  :class="{ 'is-invalid': !!errors.ipress_nombre }" required>
                <div v-if="errors.ipress_nombre" class="invalid-feedback d-block">
                  {{ errors.ipress_nombre[0] }}
                </div>
              </div>

              <!-- Tipo y Motivo -->
              <div class="mb-3">
                <label class="form-label">Tipo de Comisión *</label>
                <input v-model="form.tipo" type="text" class="form-control" :class="{ 'is-invalid': !!errors.tipo }"
                  required>
                <div v-if="errors.tipo" class="invalid-feedback d-block">
                  {{ errors.tipo[0] }}
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Motivo *</label>
                <input v-model="form.motivo" type="text" class="form-control" :class="{ 'is-invalid': !!errors.motivo }"
                  required>
                <div v-if="errors.motivo" class="invalid-feedback d-block">
                  {{ errors.motivo[0] }}
                </div>
              </div>

              <!-- Coordenadas -->
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Norte *</label>
                  <input v-model="form.ipress_norte" type="text" class="form-control"
                    :class="{ 'is-invalid': !!errors.ipress_norte }" required>
                  <div v-if="errors.ipress_norte" class="invalid-feedback d-block">
                    {{ errors.ipress_norte[0] }}
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Este *</label>
                  <input v-model="form.ipress_este" type="text" class="form-control"
                    :class="{ 'is-invalid': !!errors.ipress_este }" required>
                  <div v-if="errors.ipress_este" class="invalid-feedback d-block">
                    {{ errors.ipress_este[0] }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Participantes -->
          <div class="mb-3">
            <label class="form-label">Participantes</label>
            <select v-model="form.participantes" class="form-select" multiple
              :class="{ 'is-invalid': !!errors.participantes }">
              <option v-for="persona in comisionStore.participantes" :key="persona.id" :value="persona.id"
                :disabled="isParticipanteDisabled(persona.id)">
                {{ persona.apellido }}, {{ persona.nombre }} ({{ persona.dni }})
                <span v-if="persona.dependencia_nombre"> - {{ persona.dependencia_nombre }}</span>
              </option>
            </select>
            <small class="text-muted">Máximo {{ maxParticipantes }} participantes (incluyendo conductor)</small>
            <div v-if="errors.participantes" class="invalid-feedback d-block">
              {{ errors.participantes[0] }}
            </div>
          </div>

          <!-- Observaciones -->
          <div class="mb-3">
            <label class="form-label">Observaciones</label>
            <textarea v-model="form.observaciones" class="form-control" rows="3"
              :class="{ 'is-invalid': !!errors.observaciones }"></textarea>
            <div v-if="errors.observaciones" class="invalid-feedback d-block">
              {{ errors.observaciones[0] }}
            </div>
          </div>
        </form>
      </template>
    </ModalBase>
    
    <!-- Modal de confirmación para eliminar -->
    <ModalBase :visible="showDeleteModal" mode="delete" entityName="comision" confirm-text="Eliminar Permanentemente"
      confirm-class="p-button-danger" :loading="isDeleting" @close="closeDeleteModal" @confirm="proceedDelete">
      <template #content>
        ¿Estás seguro de eliminar permanentemente la programación <strong>{{ tableroToDelete?.name }}</strong>?
        <div class="alert alert-warning mt-3">
          <i class="fas fa-exclamation-triangle me-2"></i>
          Esta acción no se puede deshacer y eliminará todos los datos asociados al tablero.
        </div>
      </template>
    </ModalBase>
    <!-- Modal de Detalles
    <div class="modal fade" id="detailsModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Detalles de Comisión #{{ selectedComision?.id }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="selectedComision">
              <div class="row">
                <div class="col-md-6">
                  <h6>Información del Vehículo</h6>
                  <p><strong>Marca/Modelo:</strong> {{ selectedComision.vehiculo_info.marca }} {{
                    selectedComision.vehiculo_info.modelo }}</p>
                  <p><strong>Placa:</strong> {{ selectedComision.vehiculo_info.placa }}</p>
                  <p><strong>Asientos:</strong> {{ selectedComision.vehiculo_info.asientos }}</p>
                </div>
                <div class="col-md-6">
                  <h6>Información de la Comisión</h6>
                  <p><strong>Tipo:</strong> {{ selectedComision.tipo }}</p>
                  <p><strong>Motivo:</strong> {{ selectedComision.motivo }}</p>
                  <p><strong>Estado:</strong> <span :class="`badge bg-${getEstadoBadge(selectedComision.estado)}`">
                      {{ selectedComision.estado }}
                    </span></p>
                </div>
              </div>

              <div class="row mt-3">
                <div class="col-md-6">
                  <h6>Fechas</h6>
                  <p><strong>Salida:</strong> {{ formatDateTime(selectedComision.fecha_salida) }}</p>
                  <p><strong>Retorno:</strong> {{ formatDateTime(selectedComision.fecha_retorno) }}</p>
                </div>
                <div class="col-md-6">
                  <h6>IPRESS Destino</h6>
                  <p><strong>Nombre:</strong> {{ selectedComision.ipress_nombre }}</p>
                  <p><strong>Ubicación:</strong> {{ selectedComision.ipress_departamento }} / {{
                    selectedComision.ipress_provincia }} / {{ selectedComision.ipress_distrito }}</p>
                  <p><strong>Norte:</strong> {{ selectedComision.ipress_norte }}</p>
                  <p><strong>Este:</strong> {{ selectedComision.ipress_este }}</p>

                </div>
              </div>

              <div class="row mt-3">
                <div class="col-12">
                  <h6>Personal Asignado</h6>
                  <table class="table table-sm">
                    <thead>
                      <tr>
                        <th>Rol</th>
                        <th>DNI</th>
                        <th>Apellidos y Nombres</th>
                        <th>Dependencia</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Conductor</td>
                        <td>{{ selectedComision.conductor_info.dni }}</td>
                        <td>{{ selectedComision.conductor_info.apellido }}, {{ selectedComision.conductor_info.nombre }}
                        </td>
                        <td>{{ selectedComision.conductor_info.dependencia_nombre }}</td>
                      </tr>
                      <tr v-for="(participante, index) in selectedComision.participantes_info" :key="index">
                        <td>Participante</td>
                        <td>{{ participante.dni }}</td>
                        <td>{{ participante.apellido }}, {{ participante.nombre }}</td>
                        <td>{{ participante.dependencia_nombre }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div class="row mt-3" v-if="selectedComision.observaciones">
                <div class="col-12">
                  <h6>Observaciones</h6>
                  <p>{{ selectedComision.observaciones }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
          </div>
        </div>
      </div>
    </div>-->
  </main>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch } from 'vue';
import CalendarView from '@/views/dgos/administracion/CalendarView.vue';
import { formatDateTime, formatDateTimeForInput } from '@/components/utils/format';


import ModalBase from '@/components/ui/ModalBase.vue';
import DataTableWrapper from '@/components/ui/DataTableWrapper.vue';
import { useComisionStore } from '@/stores/dgos/comisionStore';
import FloatInput from '@/components/widgets/FloatInput.vue';

const comisionStore = useComisionStore();
const errors = ref({});
const showModal = ref(false);
const showDeleteModal = ref(false);
const editing = ref(false);
const isSubmitting = ref(false);
const tableroToDelete = ref(null);
const tableroToEdit = ref(null);
const isDeleting = ref(false);
const maxParticipantes = 4; // Ajusta según la capacidad del vehículo
const isParticipanteDisabled = (id) => {
  // Opcional: deshabilitar si ya está seleccionado o se alcanzó el máximo
  return form.value.participantes.includes(id) ||
    form.value.participantes.length >= maxParticipantes;
};
// Formulario
const FORM_STATE = {
  id: null,
  vehiculo: null,
  conductor: null,
  participantes: [],
  tipo: '',
  motivo: '',
  fecha_salida: '',
  fecha_retorno: '',
  ipress_codigo: '',
  ipress_nombre: '',
  ipress_departamento: '',
  ipress_provincia: '',
  ipress_distrito: '',
  ipress_disa: '',
  ipress_institucion: '',
  ipress_norte: '',
  ipress_este: '',
  observaciones: '',
  estado: 'PENDIENTE'
};

// Usamos la estructura para el formulario reactivo
const form = ref({ ...FORM_STATE });

const columns = ref([
  {
    field: 'ipress_nombre',
    header: 'IPRESS',
    sortable: true,
    filter: false,
    filterOptions: computed(() =>
      comisionStore.comision.map(u => u.name).filter((v, i, a) => a.indexOf(v) === i)
    ),
  },
  { field: 'fecha_salida', header: 'F. SALIDA', bodyTemplate: true, filter: false },
  { field: 'fecha_retorno', header: 'F. RETORNO', bodyTemplate: true, filter: false },
  { field: 'participantes', header: 'PROFESIONAL', bodyTemplate: true, filter: false },
  { field: 'conductor_nombre', header: 'CONDUCTOR', bodyTemplate: true, filter: false, sortable: true },
  { field: 'created_by_username', header: 'CREADO', bodyTemplate: true, filter: true },

]);

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
const openEditModal = async (comision) => {
  editing.value = true;
  tableroToEdit.value = comision;

  // Resetear formulario manteniendo la reactividad
  Object.assign(form.value, FORM_STATE);

  form.value = {
    ...form.value,
    ...comision,
    // Formatear fechas para el input
    fecha_salida: formatDateTimeForInput(comision.fecha_salida),
    fecha_retorno: formatDateTimeForInput(comision.fecha_retorno)
  };

  // Esperar a que el modal y los componentes estén renderizados
  await nextTick();
  showModal.value = true;

};
const handleSubmit = async () => {
  isSubmitting.value = true;
  errors.value = {}; // Limpiar errores anteriores
  //console.log('Datos del formulario a enviar:', JSON.stringify(form.value, null, 2));

  try {
    if (editing.value) {
      await comisionStore.UpdateComision(tableroToEdit.value.id, form.value);
    } else {
      await comisionStore.CreateComision(form.value);
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
const proceedDelete = async () => {
  isDeleting.value = true;
  try {
    const success = await comisionStore.DeleteComision(tableroToDelete.value.id);
    if (success) {
      closeDeleteModal();
    }
  } catch (error) {
  } finally {
    isDeleting.value = false;
  }
};
// Inicialización
onMounted(async () => {
  try {
    comisionStore.loading = true;
    await Promise.all([
      comisionStore.ListComision(),
      comisionStore.ListConductores(),
      comisionStore.ListVehiculos(),
      comisionStore.ListParticipantes()
    ]);
  } catch (error) {
  } finally {
    comisionStore.loading = false;
  }
});





/*const viewDetails = (comision) => {
  selectedComision.value = comision;
  detailsModal.show();
};*/




const getEstadoBadge = (estado) => {
  switch (estado) {
    case 'PENDIENTE': return 'warning';
    case 'EN_CURSO': return 'info';
    case 'COMPLETADA': return 'success';
    case 'CANCELADA': return 'danger';
    default: return 'secondary';
  }
};


</script>

<style scoped></style>