<template>
  <DataTable
    :value="data"
    :paginator="true"
    :rows="rows"
    :loading="loading"
    :totalRecords="totalRecords"
    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
    :rowsPerPageOptions="[5,10,25,50]"
    currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} registros"
    responsiveLayout="scroll"
    :stripedRows="striped"
    :removableSort="sortable"
    @page="onPageChange"
    @sort="onSortChange"
  >
      <!-- Slot para el header personalizado -->
    <template #header v-if="$slots.header">
      <div class="flex justify-content-between align-items-center p-3">
        <slot name="header"></slot>
      </div>
    </template>
    
    <!-- Columna para el índice -->
    <Column header="N°" :style="{ width: '5%' }">
      <template #body="{ index }">
        {{ index + 1 }}
      </template>
    </Column>

    <!-- Columnas dinámicas -->
    <Column 
      v-for="col in columns" 
      :key="col.field" 
      :field="col.field" 
      :header="col.header" 
      :sortable="col.sortable"
      :style="col.style"
    >
      <template #body="{data}" v-if="col.bodyTemplate">
        <slot :name="`body-${col.field}`" :data="data"></slot>
      </template>
    </Column>

    <!-- Columna de acciones -->
    <Column v-if="actions" header="Acciones" :exportable="false" style="min-width: 8rem">
      <template #body="{data}">
        <slot name="actions" :data="data"></slot>
      </template>
    </Column>

    <template #empty>
      <div class="text-center py-4">
        <i class="pi pi-exclamation-circle mr-2"></i>
        No se encontraron registros
      </div>
    </template>

    <template #loading>
      <div class="text-center py-4">
        <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="4" />
        Cargando datos...
      </div>
    </template>
  </DataTable>
</template>

<script setup>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ProgressSpinner from 'primevue/progressspinner';

const props = defineProps({
  data: { type: Array, required: true },
  columns: { type: Array, required: true },
  loading: { type: Boolean, default: false },
  totalRecords: { type: Number, default: 0 },
  rows: { type: Number, default: 10 },
  striped: { type: Boolean, default: true },
  sortable: { type: Boolean, default: true },
  actions: { type: Boolean, default: false }
});

const emit = defineEmits(['page-change', 'sort-change']);

const onPageChange = (event) => {
  emit('page-change', event);
};

const onSortChange = (event) => {
  emit('sort-change', event);
};
</script>

<style scoped>
/* Estilos opcionales para personalizar */
</style>