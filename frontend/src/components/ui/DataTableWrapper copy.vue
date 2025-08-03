<template>
  <div class="card">
    <!-- Encabezado modificado con dos filas -->
    <div class="table-header-container">
      <!-- Fila 1: Título -->
      <h2 v-if="title" class="table-title">{{ title }}</h2>

      <!-- Fila 2: Botón y buscador -->
      <div class="header-actions-container">
        <Button v-if="showCreateButton" :icon="createButtonIcon" :label="createButtonLabel" @click="$emit('create')"
          class="p-button-sm" />

        <div class="header-search-container">
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText v-model="searchTerm" placeholder="Buscar..." class="p-inputtext-sm" @input="onSearch" />
          </span>
        </div>
      </div>
    </div>

    <DataTable :value="filteredData" :paginator="true" size="small" :rows="rows" :loading="loading"
      :totalRecords="totalRecords" :sortField="sortField" :sortOrder="sortOrder" removableSort
      paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
      :rowsPerPageOptions="[5, 10, 25, 50, 100]"
      currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} registros" responsiveLayout="scroll"
      :sortable="sortable" class="elegant-table">
      <!-- Slot para header personalizado -->
      <template #header>
        <slot name="header"></slot>
      </template>

      <!-- Índice automático -->
      <Column v-if="showIndex" header="N°" headerClass="header-cell" bodyClass="body-cell" :style="{ width: '5%' }">
        <template #body="slotProps">
          {{ slotProps.index + 1 }}
        </template>
      </Column>

      <!-- Columnas dinámicas -->
      <Column v-for="col in columns" :key="col.field" :field="col.field" :header="col.header" :sortable="col.sortable"
        :style="col.style" headerClass="header-cell" bodyClass="body-cell">
        <template #body="slotProps">
          <slot v-if="col.bodyTemplate" :name="`body-${col.field}`" :data="slotProps.data"></slot>
          <template v-else>
            {{ slotProps.data[col.field] || '-' }}
          </template>
        </template>
      </Column>

      <!-- Columna de acciones -->
      <Column v-if="actions" header="Acciones" :exportable="false" style="min-width: 8rem" headerClass="header-cell"
        bodyClass="body-cell">
        <template #body="slotProps">
          <slot name="actions" :data="slotProps.data"></slot>
        </template>
      </Column>

      <!-- Empty State -->
      <template #empty>
        <div class="empty-state">
          <i class="pi pi-exclamation-circle"></i>
          <p>No se encontraron registros</p>
        </div>
      </template>

      <!-- Loading State -->
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
import { ref, computed } from 'vue';

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
  sortOrder: { type: Number, default: 1 } // 1=ascendente, -1=descendente
});

const emit = defineEmits(['page-change', 'sort-change', 'search', 'create']);

const searchTerm = ref('');

const filteredData = computed(() => {
  if (!searchTerm.value) return props.data;
  return props.data.filter(item =>
    props.columns.some(col =>
      String(item[col.field] || '').toLowerCase().includes(searchTerm.value.toLowerCase())
    )
  );
});


const onSearch = () => {
  emit('search', searchTerm.value);
};
</script>

<style scoped>
.card {
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.elegant-table {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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

.p-input-icon-left>i {
  color: #6c757d;
  left: 1rem;
}

/* Estilos específicos para el header */
.table-header-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.table-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.header-actions-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 0.75rem;
}

.header-search-container {
  width: auto;
  /* Ancho automático según contenido */
}

/* Estilos para el input de búsqueda */
.header-search-container .p-input-icon-left {
  position: relative;
  width: 250px;
  /* Tamaño estándar fijo */
}

.header-search-container .p-input-icon-left>i {
  position: absolute;
  top: 50%;
  left: 0.75rem;
  margin-top: -0.5rem;
  color: #6c757d;
  font-size: 0.9rem;
}

.header-search-container .p-inputtext {
  padding-left: 2rem;
  width: 100%;
  height: 36px;
  /* Altura estándar */
  font-size: 0.875rem;
}

/* Responsive para móviles */
@media (max-width: 768px) {
  .header-actions-container {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }

  .header-search-container {
    width: 100%;
  }

  .header-search-container .p-input-icon-left {
    width: 100%;
  }
}
</style>