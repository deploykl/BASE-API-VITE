<template>
  <div class="card">
    <div class="table-header-container">
      <h2 v-if="title" class="table-title">{{ title }}</h2>

      <div class="header-actions-container">
        <Button v-if="showCreateButton" :icon="createButtonIcon" :label="createButtonLabel" @click="$emit('create')"
          class="p-button-sm create-button" />

        <div class="right-actions-container">
          <Button type="button" icon="pi pi-filter-slash" label="Clear" class="p-button-sm clear-button"
            @click="clearFilter()" text />

          <div class="header-search-container">
            <span class="p-input-icon-left">
              <i class="pi pi-search" />
              <InputText v-model="searchTerm" placeholder="Buscar..." class="p-inputtext-sm" @input="onSearch" />
            </span>
          </div>
        </div>
      </div>
    </div>

    <DataTable :value="filteredData" v-model:filters="filters" :paginator="true" size="small" :rows="rows"
      :loading="loading" :totalRecords="totalRecords" :sortField="sortField" :sortOrder="sortOrder" removableSort
      paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
      :rowsPerPageOptions="[5, 10, 25, 50, 100]"
      currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} registros" responsiveLayout="stack"
      :sortable="sortable" class="elegant-table" filterDisplay="menu" :globalFilterFields="globalFilterFields"
      :expandedRows="expandedRows" dataKey="id" @rowExpand="onRowExpand" @rowCollapse="onRowCollapse" ref="dt"
      :rowClass="rowClass" :rowStyle="rowStyle">

      <template #header>
        <div class="d-flex align-items-center flex-wrap gap-2">
          <!-- Botón(es) que vengan desde PersonalView -->
          <slot name="header"></slot>

          <!-- Botones propios del DataTableWrapper -->
          <template v-if="expandable">
            <Button icon="pi pi-plus" label="Mostrar Todo" @click="expandAll" class="p-button-text p-button-sm" />
            <Button icon="pi pi-minus" label="Ocultar Todo" @click="collapseAll"
              class="p-button-text p-button-sm me-1" />
          </template>
        </div>
      </template>

      <!-- Columna expander (condicional) -->
      <Column v-if="expandable" expander style="width: 2rem" headerClass="header-cell">
        <template #header>
          +/-
        </template>
      </Column>

      <!-- Slot para contenido expandido (condicional) -->
      <template v-if="expandable" #expansion="slotProps">
        <div class="p-3 expansion-content">
          <slot name="expansion" :data="slotProps.data"></slot>
        </div>
      </template>

      <Column v-if="showIndex" header="N°" headerClass="header-cell" bodyClass="body-cell" :style="{ width: '5%' }">
        <template #body="slotProps">
          {{ slotProps.index + 1 }}
        </template>
      </Column>

      <Column v-for="col in columns" :key="col.field" :field="col.field" :header="col.header" :sortable="col.sortable"
        :style="col.style" headerClass="header-cell" bodyClass="body-cell" :showFilterMenu="col.filter !== false"
        :filterField="col.filterField || col.field" :dataType="col.dataType || 'text'" :showFilterMatchModes="false"
        :filterMenuStyle="{ width: '14rem' }">
        <template #body="slotProps">
          <slot v-if="col.bodyTemplate" :name="`body-${col.field}`" :data="slotProps.data"></slot>
          <template v-else>
            {{ formatValue(slotProps.data[col.field], col) }}
          </template>
        </template>

        <template #filter="{ filterModel, filterCallback }" v-if="col.filter !== false">
          <template v-if="col.dataType === 'boolean'">
            <Dropdown v-model="filterModel.value" :options="booleanOptions" optionLabel="label" optionValue="value"
              placeholder="Seleccionar"
              @change="() => { filterCallback(); handleFilterChange(col.field, filterModel.value); }" class="w-full" />
          </template>
          <template v-else-if="col.filterOptions">
            <Dropdown v-model="filterModel.value" :options="col.filterOptions" :placeholder="`Seleccionar`"
              @change="() => { filterCallback(); handleFilterChange(col.field, filterModel.value); }" class="w-full" />
          </template>
          <template v-else>
            <InputText v-model="filterModel.value" type="text" @input="filterCallback" class="w-full"
              placeholder="Buscar..." @change="handleFilterChange(col.field, filterModel.value)" />
          </template>
        </template>
      </Column>

      <Column v-if="actions" header="Acciones" :exportable="false" style="min-width: 8rem" headerClass="header-cell"
        bodyClass="body-cell">
        <template #body="slotProps">
          <slot name="actions" :data="slotProps.data"></slot>
        </template>
      </Column>

      <template #empty>
        <div class="empty-state">
          <i class="pi pi-exclamation-circle"></i>
          <p>No se encontraron registros</p>
        </div>
      </template>

      <template #loading>
        <div class="loading-state">
          <ProgressSpinner />
          <p>Cargando datos...</p>
        </div>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { jsPDF } from "jspdf";
import autoTable from "jspdf-autotable";
import { utils, writeFile } from 'xlsx';

const FilterMatchMode = {
  CONTAINS: 'contains',
  STARTS_WITH: 'startsWith',
  ENDS_WITH: 'endsWith',
  EQUALS: 'equals',
  NOT_EQUALS: 'notEquals',
  IN: 'in',
  LESS_THAN: 'lt',
  LESS_THAN_OR_EQUAL_TO: 'lte',
  GREATER_THAN: 'gt',
  GREATER_THAN_OR_EQUAL_TO: 'gte',
  BETWEEN: 'between',
  DATE_IS: 'dateIs',
  DATE_IS_NOT: 'dateIsNot',
  DATE_BEFORE: 'dateBefore',
  DATE_AFTER: 'dateAfter'
};

const props = defineProps({
  data: { type: Array, required: true },
  columns: { type: Array, required: true },
  loading: { type: Boolean, default: false },
  totalRecords: { type: Number, default: 0 },
  rows: { type: Number, default: 10 },
  striped: { type: Boolean, default: true },
  sortable: { type: Boolean, default: true },
  actions: { type: Boolean, default: false },
  title: { type: String, default: '' },
  showCreateButton: { type: Boolean, default: false },
  createButtonLabel: { type: String, default: 'Nuevo' },
  showIndex: { type: Boolean, default: true },
  createButtonIcon: { type: String, default: 'pi pi-plus' },
  sortField: { type: String, default: '' },
  sortOrder: { type: Number, default: 1 },
  filterOptions: { type: Array, default: () => [] },
  globalFilterFields: { type: Array, default: () => [] },
  dataKey: { type: String, default: 'id' }, // Asegúrate de tener esto
  expandable: { type: Boolean, default: false }
});

const emit = defineEmits([
  'page-change',
  'sort-change',
  'search',
  'create',
  'filter-change',
  'column-filter',
  'row-expand',
  'row-collapse',
  'column-filter-change', // Nueva emisión para cambios de filtro por columna
  'filter-change', // Agrega esta emisión

]);

const STORAGE_KEY = 'tableFilters';

// Filtros
const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  ...props.columns.reduce((acc, col) => {
    if (col.filter !== false) {
      acc[col.field] = {
        value: null,
        matchMode: col.dataType === 'boolean' ? FilterMatchMode.EQUALS : (col.filterMatchMode || FilterMatchMode.CONTAINS)
      };
    }
    return acc;
  }, {})
});
// Agrega este método para manejar cambios de filtro
const handleFilterChange = (field, value) => {
  emit('column-filter-change', { field, value });

  // Si es el campo de dependencia, también actualiza el filtro global
  if (field === 'dependencia_nombre') {
    emit('filter-change', { field: 'dependencia', value });
  }
};
// Agrega estas nuevas propiedades
const expandedRows = ref([]);
const searchTerm = ref('');

// Agrega esta línea al inicio de las refs
const dt = ref();

// Estado para controlar la carga
const exportingCSV = ref(false);

const exportCSV = () => {
  exportingCSV.value = true; // Activar spinner

  // Pequeño delay para que se vea el spinner
  setTimeout(() => {
    dt.value.exportCSV(); // Llamar a la exportación real

    // Desactivar spinner después de un breve momento
    setTimeout(() => {
      exportingCSV.value = false;
    }, 3000);
  }, 300);
};
const booleanOptions = ref([
  { label: 'Activo', value: true },
  { label: 'Inactivo', value: false }
]);
const onRowExpand = (event) => {
  emit('row-expand', event.data);
};

const onRowCollapse = (event) => {
  emit('row-collapse', event.data);
};
// Guardar filtros en localStorage
const saveFiltersToStorage = () => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      searchTerm: searchTerm.value,
      filters: filters.value,
      timestamp: new Date().getTime()
    }));
  } catch (e) {
    console.error('Error al guardar filtros:', e);
  }
};

// Cargar filtros desde localStorage
const loadFiltersFromStorage = () => {
  try {
    const savedData = localStorage.getItem(STORAGE_KEY);
    if (savedData) {
      const { searchTerm: savedSearchTerm, filters: savedFilters } = JSON.parse(savedData);

      // Validar que los filtros cargados coincidan con las columnas actuales
      const validFilters = { ...filters.value };
      Object.keys(savedFilters).forEach(key => {
        if (key in validFilters) {
          validFilters[key] = savedFilters[key];
        }
      });

      searchTerm.value = savedSearchTerm || '';
      filters.value = validFilters;
    }
  } catch (e) {
    console.error('Error al cargar filtros:', e);
    localStorage.removeItem(STORAGE_KEY);
  }
};

// Formatear valores para visualización
const formatValue = (value, column) => {
  if (value === null || value === undefined || value === '') return '-';

  if (column.dataType === 'date') {
    return new Date(value).toLocaleDateString();
  }

  if (column.dataType === 'numeric') {
    return new Intl.NumberFormat('es-ES').format(value);
  }

  if (column.dataType === 'boolean') {
    return value ? 'Sí' : 'No';
  }

  return value;
};

// Búsqueda
const onSearch = () => {
  emit('search', searchTerm.value);
};

/// Datos filtrados
const filteredData = computed(() => {
  if (!props.data) return [];

  let result = [...props.data]; // Copia los datos originales

  // Filtro global (búsqueda)
  if (searchTerm.value) {
    result = result.filter(item =>
      props.columns.some(col =>
        String(item[col.field] || '').toLowerCase().includes(searchTerm.value.toLowerCase())
      )
    );
  }

  // Filtros por columna
  for (const [field, filter] of Object.entries(filters.value)) {
    if (field === 'global' || filter?.value === null || filter?.value === '') continue;

    const column = props.columns.find(col => col.field === field);
    const filterValue = filter.value;

    result = result.filter(item => {
      const itemValue = item[field];

      // Caso especial para booleanos
      if (column?.dataType === 'boolean') {
        return itemValue === filterValue;
      }

      // Filtrado normal para otros tipos
      const strItemValue = String(itemValue || '').toLowerCase();
      const strFilterValue = String(filterValue).toLowerCase();

      switch (filter.matchMode) {
        case 'startsWith': return strItemValue.startsWith(strFilterValue);
        case 'contains': return strItemValue.includes(strFilterValue);
        case 'equals': return strItemValue === strFilterValue;
        default: return strItemValue.includes(strFilterValue);
      }
    });
  }

  return result;
});

// Limpiar todos los filtros
const clearFilter = () => {
  searchTerm.value = '';
  filters.value.global.value = null;

  Object.keys(filters.value).forEach(key => {
    if (key !== 'global') {
      filters.value[key].value = null;
    }
  });

  // Limpiar también el localStorage
  localStorage.removeItem(STORAGE_KEY);

  emit('search', '');
  emit('filter-change', { cleared: true });
};
const expandAll = () => {
  if (!props.data || props.data.length === 0) return;

  // Usa el mismo formato que en el ejemplo de PrimeVue
  expandedRows.value = props.data.reduce((acc, item) => {
    acc[item[props.dataKey]] = true;
    return acc;
  }, {});
};
const rowClass = (data) => {
  return [
    {
      'inactive-row': data.is_active === false,
      'active-row': data.is_active === true,
      'cesado-row': data.estado_nombre === 'Cesado' // Añade esta línea
    }
  ];
};

const rowStyle = (data) => {
  if (data.estado_nombre === 'Cesado') {
    return {
      backgroundColor: '#fff5f5', // Fondo rojo claro para cesados
      'box-shadow': 'inset 5px 0 0 #dc3545' // Borde rojo intenso para cesados
    };
  } else if (data.is_active === false) {
    return {
      backgroundColor: '#f8f9fa',
      color: '#868e96',
      'box-shadow': 'inset 5px 0 0 #f04343' // Borde rojo para inactivos
    };
  } else if (data.is_active === true) {
    return {
      //backgroundColor: '#f0fff0', // Fondo verde claro para activos
      'box-shadow': 'inset 5px 0 0 #11ba82' // Borde verde para activos
    };
  }
  return {};
};

const collapseAll = () => {
  expandedRows.value = []; // Contrae todas las filas
  emit('row-collapse');
};
// Cargar filtros al montar el componente
onMounted(() => {
  loadFiltersFromStorage();
});

// Observar cambios en los filtros para guardarlos y emitir eventos
watch([searchTerm, filters], () => {
  saveFiltersToStorage();

  // Emitir eventos
  if (filters.value.global?.value !== null) {
    emit('search', filters.value.global.value);
  }

  for (const [field, filter] of Object.entries(filters.value)) {
    if (field !== 'global' && filter?.value !== null) {
      emit('column-filter', { field, value: filter.value });
    }
  }
}, { deep: true });

</script>

<style scoped>
/* Estilos base */
.card {
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  width: calc(100% - 2rem);
  margin: 0 auto;
  box-sizing: border-box;
  overflow: hidden;
}

.table-header-container {
  display: flex;
  flex-direction: column;
  gap: 0.70rem;
  margin-bottom: 1rem;
}

.table-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #343F54;
}

.header-actions-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 1rem;
}

.right-actions-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.header-search-container {
  min-width: 300px;
}

.header-search-container .p-input-icon-left {
  position: relative;
}

.header-search-container .p-input-icon-left>i {
  position: absolute;
  top: 50%;
  left: 0.75rem;
  margin-top: -0.5rem;
  color: #6c757d;
  font-size: 1rem;
}

.header-search-container .p-inputtext {
  padding-left: 2rem;
  width: 100%;
  height: 36px;
  font-size: 1rem;
}

.empty-state,
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #6c757d;
}

.empty-state i,
.loading-state i {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #adb5bd;
}

.p-inputtext {
  border-radius: 6px;
  border: 1px solid #ced4da;
  transition: all 0.3s;
}

.p-inputtext:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 0.2rem rgba(99, 102, 241, 0.25);
}

:deep(.header-cell) {
  color: #495057;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  border-top: 2px solid #364257;
  border-bottom: 2px solid #364257;
}

:deep(.p-column-filter-matchmode-dropdown),
:deep(.p-column-filter-operator) {
  display: none !important;
}

:deep(.p-column-filter-constraint) {
  padding: 0 !important;
}

.expansion-content {
  background: #f8f9fa;
  border-left: 4px solid var(--primary-color);
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
}

:deep(.p-datatable .p-row-toggler) {
  color: var(--primary-color);
}

:deep(.p-datatable .p-row-expanded) {
  background-color: #f8f9fa;
}

:deep(.p-datatable) {
  font-size: 0.85rem;
}

/* Estilos para móviles */
@media screen and (max-width: 768px) {
  .card {
    width: 100%;
    padding: 0.75rem;
    margin: 0;
    box-shadow: none;
    box-sizing: border-box;
    border: 1px solid #e0e0e0;
  }



  .header-actions-container {
    flex-direction: column;
    gap: 0.5rem;
  }

  .right-actions-container {
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
  }

  .header-search-container {
    width: 100%;
    min-width: unset;
  }

  .export-buttons {
    flex-direction: column;
    gap: 0.5rem;
  }

  .export-buttons .p-button {
    width: 100%;
    margin-right: 0 !important;
    margin-bottom: 0.5rem;
  }

  :deep(.p-datatable) {
    width: 100% !important;
    max-width: 100vw;
    overflow-x: auto;
    display: block;
  }

  :deep(.p-datatable-wrapper) {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  :deep(.p-datatable.p-datatable-stack) .p-datatable-thead>tr>th,
  :deep(.p-datatable.p-datatable-stack) .p-datatable-tbody>tr>td {
    display: block !important;
    width: 100% !important;
    text-align: left !important;
    box-sizing: border-box;
  }

  :deep(.p-datatable.p-datatable-stack) .p-datatable-thead>tr>th {
    position: absolute;
    top: -9999px;
    left: -9999px;
  }

  :deep(.p-datatable.p-datatable-stack) .p-datatable-tbody>tr>td:before {
    content: attr(data-label);
    font-weight: bold;
    display: inline-block;
    width: 40%;
    vertical-align: top;
    padding-right: 1rem;
  }

  :deep(.p-datatable.p-datatable-stack) .p-datatable-tbody>tr>td {
    border: 0 none !important;
    padding: 0.5rem !important;
    display: flex;
    align-items: center;
  }

  :deep(.p-datatable.p-datatable-stack) .p-datatable-tbody>tr {
    border-bottom: 1px solid #e0e0e0;
    padding: 0.5rem 0;
    display: block;
    width: 100%;
  }

  :deep(.p-paginator) {
    flex-direction: column;
    gap: 0.5rem;
  }

  :deep(.p-paginator .p-paginator-pages) {
    margin: 0.5rem 0;
  }

  .expansion-content {
    padding: 0.75rem;
  }

  .bottom-center {
    text-align: center;
  }
}

/* Estilos para pantallas muy pequeñas */
@media screen and (max-width: 400px) {
  .card {
    padding: 0.5rem;
  }

  :deep(.p-datatable) {
    font-size: 0.8rem;
  }

  .table-title {
    font-size: 1rem;
  }

  .header-search-container .p-inputtext {
    font-size: 0.8rem;
  }
}

/* Nuevos estilos para cesado */
:deep(.cesado-row) {
  background-color: #fff5f5 !important;
  border-left: 4px solid #dc3545 !important;
}

:deep(.cesado-row:hover) {
  background-color: #ffe6e6 !important;
}

/* Para el panel de expansión cuando es cesado */
:deep(.cesado-row + tr .expansion-content) {
  background-color: #fff5f5 !important;
}

:deep(.cesado-row + tr .expansion-card) {
  border-left: 4px solid #dc3545 !important;
  background-color: #fffafa !important;
}

/* Badge específico para estado cesado */
.badge-cesado {
  background-color: #dc3545 !important;
  color: white !important;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
}

/* Estilo para el panel de expansión cuando es cesado */
:deep(.bg-cesado) {
  background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%) !important;
}

:deep(.bg-cesado .expansion-card) {
  background-color: #fffafa !important;
  border-left: 4px solid #dc3545 !important;
}
</style>