<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Gestión de Comisiones</h1>
      <nav>
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><router-link to="/">Inicio</router-link></li>
          <li class="breadcrumb-item active">Comisiones</li>
        </ol>
      </nav>
    </div>

    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="card-title">Listado de Comisiones</h5>
                <button class="btn btn-primary" @click="showCreateModal">
                  <i class="bi bi-plus-circle"></i> Nueva Comisión
                </button>
              </div>

              <!-- Filtros -->
              <div class="row mb-3">
                <div class="col-md-3">
                  <input v-model="filters.search" type="text" class="form-control" placeholder="Buscar...">
                </div>
                <div class="col-md-2">
                  <select v-model="filters.estado" class="form-select">
                    <option value="">Todos los estados</option>
                    <option value="PENDIENTE">Pendientes</option>
                    <option value="EN_CURSO">En curso</option>
                    <option value="COMPLETADA">Completadas</option>
                  </select>
                </div>
                <div class="col-md-2">
                  <button class="btn btn-outline-secondary" @click="resetFilters">
                    <i class="bi bi-arrow-counterclockwise"></i> Limpiar
                  </button>
                </div>
              </div>

              <!-- Tabla de comisiones -->
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">Vehículo</th>
                      <th scope="col">Conductor</th>
                      <th scope="col">Fecha Salida</th>
                      <th scope="col">Destino</th>
                      <th scope="col">Estado</th>
                      <th scope="col">Acciones</th>
                    </tr>
                  </thead>
                  <tbody v-if="loading">
                    <tr>
                      <td colspan="7" class="text-center">
                        <div class="spinner-border text-primary" role="status">
                          <span class="visually-hidden">Cargando...</span>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                  <tbody v-else>
                    <tr v-for="comision in comisiones" :key="comision.id">
                      <td>{{ comision.id }}</td>
                      <td>{{ comision.vehiculo_info.marca }} - {{ comision.vehiculo_info.placa }}</td>
                      <td>{{ comision.conductor_info.apellido }}, {{ comision.conductor_info.nombre }}</td>
                      <td>{{ formatDate(comision.fecha_salida) }}</td>
                      <td>{{ comision.ipress_nombre }}</td>
                      <td>
                        <span :class="`badge bg-${getEstadoBadge(comision.estado)}`">
                          {{ comision.estado }}
                        </span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-outline-primary me-1" @click="viewDetails(comision)">
                          <i class="pi pi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-warning me-1" @click="editComision(comision)">
                          <i class="pi pi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" @click="confirmDelete(comision)">
                          <i class="pi pi-trash"></i>
                        </button>
                      </td>
                    </tr>
                    <tr v-if="!comisiones || comisiones.length === 0">
                      <td colspan="7" class="text-center">No se encontraron comisiones</td>
                    </tr>
                  </tbody>
                </table>
              </div>

            
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modal de creación/edición -->
    <div class="modal fade" id="comisionModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modalTitle }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveComision">
              <div class="row g-3">
                <!-- Sección Vehículo -->
                <div class="col-md-6">
                  <label class="form-label">Vehículo *</label>
                  <select v-model="form.vehiculo" class="form-select" required>
                    <option v-for="vehiculo in vehiculos" :key="vehiculo.id" :value="vehiculo.id">
                      {{ vehiculo.marca }} {{ vehiculo.modelo }} - {{ vehiculo.placa }}
                    </option>
                  </select>
                </div>

                <!-- Sección Conductor -->
                <div class="col-md-6">
                  <label class="form-label">Conductor *</label>
                  <select v-model="form.conductor" class="form-select" required>
                    <option v-for="conductor in conductores" :key="conductor.id" :value="conductor.id">
                      {{ conductor.apellido }}, {{ conductor.nombre }} ({{ conductor.dni }})
                    </option>
                  </select>
                </div>

                <!-- Sección Participantes -->
                <div class="col-12">
                  <label class="form-label">Participantes</label>
                  <select v-model="form.participantes" class="form-select" multiple>
                    <option v-for="persona in personalDisponible" :key="persona.id" :value="persona.id">
                      {{ persona.apellido }}, {{ persona.nombre }} ({{ persona.dni }})
                    </option>
                  </select>
                  <small class="text-muted">Máximo {{ maxParticipantes }} participantes (incluyendo conductor)</small>
                </div>

                <!-- Sección Fechas -->
                <div class="col-md-6">
                  <label class="form-label">Fecha de Salida *</label>
                  <input v-model="form.fecha_salida" type="datetime-local" class="form-control" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Fecha de Retorno *</label>
                  <input v-model="form.fecha_retorno" type="datetime-local" class="form-control" required>
                </div>

                <!-- Sección IPRESS -->
                <div class="col-12">
                  <h6 class="mt-3">Datos del IPRESS Destino</h6>
                  <hr>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Nombre IPRESS *</label>
                  <input v-model="form.ipress_nombre" type="text" class="form-control" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Código IPRESS</label>
                  <input v-model="form.ipress_codigo" type="text" class="form-control">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Departamento *</label>
                  <input v-model="form.ipress_departamento" type="text" class="form-control" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Provincia *</label>
                  <input v-model="form.ipress_provincia" type="text" class="form-control" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Distrito *</label>
                  <input v-model="form.ipress_distrito" type="text" class="form-control" required>
                </div>

                <!-- Sección Comisión -->
                <div class="col-md-6">
                  <label class="form-label">Tipo de Comisión *</label>
                  <input v-model="form.tipo" type="text" class="form-control" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Motivo *</label>
                  <input v-model="form.motivo" type="text" class="form-control" required>
                </div>
                <div class="col-12">
                  <label class="form-label">Observaciones</label>
                  <textarea v-model="form.observaciones" class="form-control" rows="3"></textarea>
                </div>
              </div>

              <div class="modal-footer mt-3">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" class="btn btn-primary" :disabled="saving">
                  <span v-if="saving" class="spinner-border spinner-border-sm" role="status"></span>
                  {{ saving ? 'Guardando...' : 'Guardar' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Detalles -->
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
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { Modal } from 'bootstrap';
import { useToast } from 'primevue/usetoast';
import { api } from "@/components/services/Axios"

const toast = useToast();

// Datos y estados
const comisiones = ref([]);
const loading = ref(false);
const saving = ref(false);
const vehiculos = ref([]);
const conductores = ref([]);
const personalDisponible = ref([]);
const selectedComision = ref(null);
const maxParticipantes = ref(4); // Máximo 4 participantes + 1 conductor = 5 (capacidad del vehículo)

// Filtros y paginación
const filters = ref({
  search: '',
  estado: ''
});
const pagination = ref({
  current_page: 1,
  last_page: 1,
  per_page: 10,
  total: 0
});

// Formulario
const form = ref({
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
});

// Modales
let comisionModal = null;
let detailsModal = null;

// Computed
const modalTitle = computed(() => form.value.id ? 'Editar Comisión' : 'Nueva Comisión');

// Métodos
const fetchComisiones = async () => {
  try {
    loading.value = true;
    const params = {
      page: pagination.value.current_page,
      search: filters.value.search,
      estado: filters.value.estado
    };

    const response = await api.get('dgos/administracion/comision/', { params });
    
    // Verifica si la respuesta es un array directo o tiene estructura paginada
    if (Array.isArray(response.data)) {
      // Si es array directo (sin paginación)
      comisiones.value = response.data;
      pagination.value = {
        current_page: 1,
        last_page: 1,
        per_page: response.data.length,
        total: response.data.length
      };
    } else {
      // Si tiene estructura paginada
      comisiones.value = response.data.results || [];
      pagination.value = {
        current_page: response.data.current_page || 1,
        last_page: response.data.last_page || 1,
        per_page: response.data.per_page || 10,
        total: response.data.total || 0
      };
    }
  } catch (error) {
    console.error('Error al cargar comisiones:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudo cargar el listado de comisiones',
      life: 3000
    });
    comisiones.value = [];
  } finally {
    loading.value = false;
  }
};

const fetchVehiculos = async () => {
  try {
    const response = await api.get('dgos/administracion/vehiculo/');
    vehiculos.value = response.data;
  } catch (error) {
    console.error('Error al cargar vehículos:', error);
  }
};

const fetchConductores = async () => {
  try {
    const response = await api.get('dgos/administracion/personal/', {
      params: { es_conductor: true, activo: true }
    });
    conductores.value = response.data;
  } catch (error) {
    console.error('Error al cargar conductores:', error);
  }
};

const fetchPersonalDisponible = async () => {
  try {
    const response = await api.get('dgos/administracion/personal/', {
      params: { activo: true }
    });
    personalDisponible.value = response.data;
  } catch (error) {
    console.error('Error al cargar personal disponible:', error);
  }
};

const showCreateModal = () => {
  resetForm();
  comisionModal.show();
};

const editComision = (comision) => {
  form.value = {
    id: comision.id,
    vehiculo: comision.vehiculo,
    conductor: comision.conductor,
    participantes: comision.participantes_info.map(p => p.id),
    tipo: comision.tipo,
    motivo: comision.motivo,
    fecha_salida: formatDateTimeForInput(comision.fecha_salida),
    fecha_retorno: formatDateTimeForInput(comision.fecha_retorno),
    ipress_codigo: comision.ipress_codigo,
    ipress_nombre: comision.ipress_nombre,
    ipress_departamento: comision.ipress_departamento,
    ipress_provincia: comision.ipress_provincia,
    ipress_distrito: comision.ipress_distrito,
    ipress_disa: comision.ipress_disa,
    ipress_institucion: comision.ipress_institucion,
    ipress_norte: comision.ipress_norte,
    ipress_este: comision.ipress_este,
    observaciones: comision.observaciones,
    estado: comision.estado
  };
  comisionModal.show();
};

const viewDetails = (comision) => {
  selectedComision.value = comision;
  detailsModal.show();
};

const saveComision = async () => {
  try {
    saving.value = true;

    const data = { ...form.value };

    if (data.id) {
      await api.put(`dgos/administracion/comision/${data.id}/`, data);
      toast.add({
        severity: 'success',
        summary: 'Éxito',
        detail: 'Comisión actualizada correctamente',
        life: 3000
      });
    } else {
      await api.post('dgos/administracion/comision/', data);
      toast.add({
        severity: 'success',
        summary: 'Éxito',
        detail: 'Comisión creada correctamente',
        life: 3000
      });
    }

    comisionModal.hide();
    fetchComisiones();
  } catch (error) {
    console.error('Error al guardar comisión:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudo guardar la comisión',
      life: 3000
    });
  } finally {
    saving.value = false;
  }
};

const confirmDelete = (comision) => {
  if (confirm(`¿Está seguro de eliminar la comisión #${comision.id}?`)) {
    deleteComision(comision.id);
  }
};

const deleteComision = async (id) => {
  try {
    await api.delete(`dgos/administracion/comision/${id}/`);
    toast.add({
      severity: 'success',
      summary: 'Éxito',
      detail: 'Comisión eliminada correctamente',
      life: 3000
    });
    fetchComisiones();
  } catch (error) {
    console.error('Error al eliminar comisión:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudo eliminar la comisión',
      life: 3000
    });
  }
};

const resetForm = () => {
  form.value = {
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
};

const resetFilters = () => {
  filters.value = {
    search: '',
    estado: ''
  };
  fetchComisiones();
};

const changePage = (page) => {
  if (page >= 1 && page <= pagination.value.last_page) {
    pagination.value.current_page = page;
    fetchComisiones();
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('es-PE', options);
};

const formatDateTime = (dateString) => {
  if (!dateString) return '';
  const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  return new Date(dateString).toLocaleDateString('es-PE', options);
};

const formatDateTimeForInput = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toISOString().slice(0, 16);
};

const getEstadoBadge = (estado) => {
  switch (estado) {
    case 'PENDIENTE': return 'warning';
    case 'EN_CURSO': return 'info';
    case 'COMPLETADA': return 'success';
    case 'CANCELADA': return 'danger';
    default: return 'secondary';
  }
};

// Inicialización
onMounted(() => {
  comisionModal = new Modal(document.getElementById('comisionModal'));
  detailsModal = new Modal(document.getElementById('detailsModal'));

  fetchComisiones();
  fetchVehiculos();
  fetchConductores();
  fetchPersonalDisponible();
});
</script>

<style scoped>
/* Estilos personalizados */
.card {
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.table-responsive {
  overflow-x: auto;
}

.badge {
  font-size: 0.85em;
}

.modal-content {
  border-radius: 10px;
}

.form-label {
  font-weight: 500;
}

/* Estilos para los selects múltiples */
select[multiple] {
  min-height: 120px;
}

/* Ajustes para dispositivos móviles */
@media (max-width: 768px) {
  .pagination {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>