<template>
  <div class="calendar-container">
    <FullCalendar ref="calendarRef" :options="calendarOptions" />
    
    <!-- Modal de Detalles -->
    <div class="modal fade" id="calendarDetailsModal" tabindex="-1" aria-hidden="true">
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
                  <p><strong>Coordenadas:</strong> {{ selectedComision.ipress_norte }}, {{ selectedComision.ipress_este }}</p>
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
            <button 
              v-if="selectedComision?.ipress_norte && selectedComision?.ipress_este"
              class="btn btn-primary"
              @click="showMap"
            >
              <i class="bi bi-map"></i> Ver Ruta en Mapa
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal del Mapa con OpenStreetMap -->
    <div class="modal fade" id="mapModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Ruta a {{ selectedComision?.ipress_nombre }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-12">
                <div id="mapContainer" style="height: 500px; width: 100%; border-radius: 8px;"></div>
              </div>
            </div>
            <div class="row mt-3">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Punto de Partida</label>
                  <input v-model="originAddress" type="text" class="form-control" placeholder="Ingrese dirección de partida">
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Destino</label>
                  <input :value="selectedComision?.ipress_nombre" type="text" class="form-control" readonly>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="calculateRoute"
              :disabled="!originAddress"
            >
              Calcular Ruta
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import bootstrap5Plugin from '@fullcalendar/bootstrap5';
import { Modal } from 'bootstrap';
import { api } from "@/components/services/Axios";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Configuración de iconos para Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

// Coordenadas fijas de salida
const FIXED_START_LOCATION = {
  lat: -12.0736441,
  lng: -77.0394351,
  address: "Ubicación fija de partida"
};

const calendarRef = ref(null);
const selectedComision = ref(null);
let detailsModal = null;
let mapModal = null;
let map = null;
let routeLayer = null;
let startMarker = null;
let endMarker = null;

// Configuración del calendario
const calendarOptions = ref({
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin, bootstrap5Plugin],
  initialView: 'dayGridMonth',
  themeSystem: 'bootstrap5',
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay'
  },
  events: [],
  eventClick: handleEventClick,
  dateClick: handleDateClick,
  eventContent: renderEventContent,
  height: 'auto',
  locale: 'es',
  firstDay: 1,
  eventTimeFormat: {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  },
  eventDisplay: 'block',
  editable: false,
  selectable: true,
  selectMirror: true,
  dayMaxEvents: true,
  weekends: true
});

// Función para inicializar el mapa con Leaflet
const initMap = () => {
  // Destruir el mapa existente si hay uno
  if (map) {
    map.remove();
    map = null;
  }

  const endLat = parseFloat(selectedComision.value.ipress_norte);
  const endLng = parseFloat(selectedComision.value.ipress_este);
  
  // Crear nuevo mapa centrado entre inicio y fin
  map = L.map('mapContainer').setView([
    (FIXED_START_LOCATION.lat + endLat) / 2,
    (FIXED_START_LOCATION.lng + endLng) / 2
  ], 12);

  // Añadir capa de OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(map);

  // Añadir marcador de inicio fijo
  if (startMarker) map.removeLayer(startMarker);
  startMarker = L.marker([FIXED_START_LOCATION.lat, FIXED_START_LOCATION.lng]).addTo(map)
    .bindPopup(`<b>Punto de partida:</b> ${FIXED_START_LOCATION.address}`)
    .openPopup();

  // Añadir marcador en el destino
  if (endMarker) map.removeLayer(endMarker);
  endMarker = L.marker([endLat, endLng]).addTo(map)
    .bindPopup(`<b>Destino:</b> ${selectedComision.value.ipress_nombre}`);
};

// Función para calcular ruta usando OSRM
const calculateRoute = async () => {
  try {
    const endLat = parseFloat(selectedComision.value.ipress_norte);
    const endLng = parseFloat(selectedComision.value.ipress_este);

    // Limpiar ruta anterior si existe
    if (routeLayer) map.removeLayer(routeLayer);

    // Obtener ruta de OSRM
    const response = await fetch(
      `https://router.project-osrm.org/route/v1/driving/${FIXED_START_LOCATION.lng},${FIXED_START_LOCATION.lat};${endLng},${endLat}?overview=full&geometries=geojson`
    );
    
    const routeData = await response.json();

    if (routeData.code !== 'Ok') {
      throw new Error('No se pudo calcular la ruta');
    }

    // Dibujar la ruta
    routeLayer = L.geoJSON(routeData.routes[0].geometry, {
      style: {
        color: '#3388ff',
        weight: 5,
        opacity: 0.7
      }
    }).addTo(map);

    // Ajustar vista para mostrar toda la ruta
    const bounds = L.latLngBounds([
      [FIXED_START_LOCATION.lat, FIXED_START_LOCATION.lng],
      [endLat, endLng]
    ]);
    map.fitBounds(bounds, { padding: [50, 50] });

    // Mostrar información de la ruta
    const distance = (routeData.routes[0].distance / 1000).toFixed(1);
    const duration = (routeData.routes[0].duration / 60).toFixed(0);
    
    L.popup()
      .setLatLng([endLat, endLng])
      .setContent(`
        <b>Información de Ruta</b><br>
        <b>Desde:</b> ${FIXED_START_LOCATION.address}<br>
        <b>Hasta:</b> ${selectedComision.value.ipress_nombre}<br>
        <b>Distancia:</b> ${distance} km<br>
        <b>Tiempo estimado:</b> ${duration} minutos
      `)
      .openOn(map);

  } catch (error) {
    console.error('Error al calcular ruta:', error);
    alert('Error al calcular la ruta: ' + error.message);
  }
};

// Función para mostrar el mapa
const showMap = () => {
  detailsModal.hide();
  mapModal.show();
  
  nextTick(() => {
    initMap();
    calculateRoute(); // Calcula la ruta automáticamente al mostrar el mapa
  });
};

// Transformar comisiones a eventos
function transformToEvents(comisiones) {
  return comisiones.map(comision => ({
    id: comision.id,
    title: `[${comision.vehiculo_info?.placa}] ${comision.conductor_info?.nombre}`,
    start: comision.fecha_salida,
    end: comision.fecha_retorno,
    extendedProps: { comision },
    color: getStatusColor(comision.estado),
    allDay: false
  }));
}

function getStatusColor(estado) {
  switch (estado) {
    case 'PENDIENTE': return '#ffc107';
    case 'EN_CURSO': return '#0dcaf0';
    case 'COMPLETADA': return '#198754';
    case 'CANCELADA': return '#dc3545';
    default: return '#6c757d';
  }
}

function handleEventClick(info) {
  selectedComision.value = info.event.extendedProps.comision;
  detailsModal.show();
}

function handleDateClick(arg) {
  console.log('Fecha clickeada:', arg.dateStr);
}

function renderEventContent(info) {
  const event = info.event;
  return {
    html: `
      <div class="fc-event-main-frame">
        <div class="fc-event-title-container">
          <div class="fc-event-title">${event.title}</div>
        </div>
        <div class="fc-event-time">${info.timeText}</div>
      </div>
    `
  };
}

function formatDateTime(dateString) {
  if (!dateString) return '';
  const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  return new Date(dateString).toLocaleDateString('es-PE', options);
}

function getEstadoBadge(estado) {
  switch (estado) {
    case 'PENDIENTE': return 'warning';
    case 'EN_CURSO': return 'info';
    case 'COMPLETADA': return 'success';
    case 'CANCELADA': return 'danger';
    default: return 'secondary';
  }
}

// Cargar comisiones al montar el componente
onMounted(async () => {
  detailsModal = new Modal(document.getElementById('calendarDetailsModal'));
  mapModal = new Modal(document.getElementById('mapModal'));
  
  try {
    const response = await api.get('dgos/administracion/comision/');
    const comisiones = Array.isArray(response.data) ? response.data : response.data.results;
    calendarOptions.value.events = transformToEvents(comisiones);
  } catch (error) {
    console.error('Error al cargar comisiones:', error);
  }
});

// Exponer funciones
defineExpose({
  updateCalendarSize: () => {
    if (calendarRef.value) {
      const calendarApi = calendarRef.value.getApi();
      calendarApi.updateSize();
    }
  }
});
</script>

<style scoped>
.calendar-container {
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

:deep(.fc) {
  font-family: inherit;
}

:deep(.fc-toolbar-title) {
  font-size: 1.25rem;
  font-weight: 600;
}

:deep(.fc-button) {
  background-color: #0d6efd;
  border-color: #0d6efd;
  color: white;
}

:deep(.fc-button:hover) {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

:deep(.fc-button-primary:not(:disabled).fc-button-active) {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

:deep(.fc-event) {
  cursor: pointer;
  border: none;
  font-size: 0.85em;
  padding: 2px 4px;
}

:deep(.fc-daygrid-event-dot) {
  display: none;
}
 
:deep(.fc-event-time) {
  font-weight: bold;
  margin-right: 4px;
}

:deep(.fc-event-title) {
  white-space: normal;
}

#mapContainer {
  min-height: 500px;
  background-color: #f8f9fa;
}

/* Estilos para los popups del mapa */
:deep(.leaflet-popup-content) {
  font-size: 14px;
}
:deep(.leaflet-popup-content b) {
  color: #0d6efd;
}
</style>