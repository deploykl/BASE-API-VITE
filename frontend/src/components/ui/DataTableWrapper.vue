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
      currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} registros" responsiveLayout="scroll"
      :sortable="sortable" class="elegant-table" filterDisplay="menu" :globalFilterFields="globalFilterFields"
      :expandedRows="expandedRows" dataKey="id" @rowExpand="onRowExpand" @rowCollapse="onRowCollapse" ref="dt">

      <template #header>
        <slot name="header"></slot>
        <div class="flex flex-wrap justify-end gap-2">
          <Button icon="pi pi-plus" label="Mostrar Todo" @click="expandAll" class="p-button-text p-button-sm" />
          <Button icon="pi pi-minus" label="Ocultar Todo" @click="collapseAll" class="p-button-text p-button-sm me-2" />
          <!-- Botón de Exportación CSV -->
          <Button icon="pi pi-file-excel" label="CSV" @click="exportCSV" class="p-button-sm me-2" severity="success"
            :loading="exportingCSV" />
          <Button icon="pi pi-file-pdf outline" label="PDF" @click="exportPDF" class="p-button-sm me-2" severity="danger" />
          <Button icon="pi pi-file-excel" label="Excel" @click="exportExcel" class="p-button-sm me-2" 
            severity="info" />
          <Button icon="pi pi-file-excel" label="CSV 2" @click="exportCSV2" class="p-button-sm" severity="success" />

        </div>
      </template>

      <!-- Columna expander -->
      <Column expander style="width: 2rem" headerClass="header-cell">
        <template #header>
          +/-
        </template>
      </Column>
      <!-- Slot para contenido expandido -->
      <template #expansion="slotProps">
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
              placeholder="Seleccionar" @change="filterCallback()" class="w-full" />
          </template>
          <template v-else-if="col.filterOptions">
            <Dropdown v-model="filterModel.value" :options="col.filterOptions" :placeholder="`Seleccionar`"
              @change="filterCallback()" class="w-full" />
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
  dataKey: { type: String, default: 'id' }  // Asegúrate de tener esto

});

const emit = defineEmits([
  'page-change',
  'sort-change',
  'search',
  'create',
  'filter-change',
  'column-filter',
  'row-expand',
  'row-collapse'
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

const exportPDF = async () => {
  // Configuración del documento con estilo moderno
  const doc = new jsPDF({
    orientation: "portrait",
    unit: "mm",
    format: "a4",
    filters: ["ASCIIHexEncode"]
  });

  const title = props.title || "Reporte";
  const date = new Date().toLocaleDateString();
  const recordCount = filteredData.value.length;
  const pageWidth = doc.internal.pageSize.getWidth();
  const margin = 14; // Margen izquierdo base

  // Color palette moderna (azul corporativo + grises)
  const primaryColor = [41, 128, 185];
  const secondaryColor = [99, 110, 114];
  const lightGray = [241, 242, 246];

  // Encabezado estilizado
  doc.setFillColor(...primaryColor);
  doc.rect(0, 0, pageWidth, 25, 'F');

  // Logo con efecto de borde circular
  try {
    const svgUrl = (await import('@/assets/logo.png?url')).default;
    const img = new Image();
    await new Promise((resolve, reject) => {
      img.onload = resolve;
      img.onerror = reject;
      img.src = svgUrl;
    });

    // Tamaño deseado en el PDF (en mm)
    const targetSize = 20;

    // Calcular relación de aspecto
    const aspectRatio = img.width / img.height;

    // Crear canvas con tamaño intermedio para mejor calidad
    const canvas = document.createElement('canvas');
    const intermediateSize = 100; // Tamaño intermedio para mejor calidad
    canvas.width = intermediateSize;
    canvas.height = intermediateSize / aspectRatio;
    const ctx = canvas.getContext('2d');

    // Aplicar suavizado
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';

    // Crear máscara circular
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, canvas.width / 2, 0, Math.PI * 2);
    ctx.closePath();
    ctx.clip();

    // Dibujar imagen con tamaño intermedio
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    const logoData = canvas.toDataURL('image/png', 1.0); // Calidad máxima

    // Añadir al PDF con el tamaño final deseado
    doc.addImage(logoData, 'PNG', margin, 5, targetSize, targetSize / aspectRatio);
  } catch (error) {
    console.error('Error al cargar el logo:', error);
    // Fallback elegante
    doc.setFillColor(255, 255, 255);
    doc.circle(margin + 10, 15, 8, 'F');
  }

  // Calcular posición del texto (logo + espacio de 7mm ≈ 20px)
  const textStartX = margin + 20 + 7; // margen(14) + logo(20) + espacio(7)

  // Título principal (en blanco sobre fondo azul)
  doc.setFontSize(16);
  doc.setTextColor(255, 255, 255);
  doc.setFont("helvetica", "bold");
  doc.text(title, textStartX, 15);

  // Subtítulo con fecha y conteo
  doc.setFontSize(10);
  doc.text(`Generado el ${date} • ${recordCount} registros`, textStartX, 22);

  // Reset de estilos para el contenido
  doc.setTextColor(...secondaryColor);
  doc.setFont("helvetica", "normal");

  // Función para formatear valores consistentemente
  const formatCellValue = (value, column) => {
    if (value === null || value === undefined) return '-';
    
    // Manejo especial para campos booleanos (como staff)
    if (column.dataType === 'boolean' || typeof value === 'boolean') {
      return value ? 'Sí' : 'No';
    }
    // Formatear fechas
    else if (column.dataType === 'date') {
      return value ? new Date(value).toLocaleDateString() : '-';
    }
    // Formatear números
    else if (column.dataType === 'numeric') {
      return new Intl.NumberFormat('es-ES').format(value);
    }
    // Valor por defecto (string)
    return value || '-';
  };

  // Preparar datos para la tabla
  const headers = props.columns.map(col => ({
    title: col.header,
    dataKey: col.field,
    dataType: col.dataType
  }));

  const data = filteredData.value.map(row => {
    const rowData = {};
    props.columns.forEach(col => {
      if (col.bodyTemplate) {
        rowData[col.field] = col.field === "full_name"
          ? (row.full_name || "-")
          : "-";
      } else {
        rowData[col.field] = formatCellValue(row[col.field], col);
      }
    });
    return rowData;
  });

  // Generar tabla con estilo moderno
  autoTable(doc, {
    head: [headers.map(h => h.title)],
    body: data.map(row => headers.map(header => row[header.dataKey])),
    startY: 30,
    styles: {
      fontSize: 9,
      cellPadding: 3,
      overflow: "linebreak",
      textColor: secondaryColor,
      font: "helvetica"
    },
    headStyles: {
      fillColor: primaryColor,
      textColor: 255,
      fontStyle: "bold",
      fontSize: 9
    },
    alternateRowStyles: {
      fillColor: lightGray
    },
    margin: { top: 30 },
    tableLineColor: [189, 195, 199],
    tableLineWidth: 0.2
  });

  // Pie de página
  const footerY = doc.lastAutoTable.finalY + 10;
  doc.setFontSize(8);
  doc.setTextColor(...secondaryColor);
  doc.text(`© ${new Date().getFullYear()} - Sistema de Gestión`, pageWidth - 20, footerY, { align: "right" });

  // Guardar el PDF
  doc.save(`${title.replace(/\s/g, "_")}_${date.replace(/\//g, "-")}.pdf`);
};

// Agrega esta función en tus métodos
const exportExcel = () => {
  // Preparar los datos
  const headers = props.columns.map(col => ({
    title: col.header,
    dataKey: col.field,
    dataType: col.dataType
  }));

  // Crear matriz de datos incluyendo encabezados
  const excelData = [
    // Fila de encabezado
    headers.map(h => h.title),
    // Filas de datos
    ...filteredData.value.map(row => {
      return headers.map(col => {
        // Formatear valores según tipo
        const value = row[col.dataKey];
        
        // Manejar valores null/undefined
        if (value === null || value === undefined) return '';
        
        // Caso especial para booleanos (incluyendo el campo staff)
        if (col.dataType === 'boolean' || typeof value === 'boolean') {
          return value ? 'Sí' : 'No'; // Mostrar "No" cuando es false
        }
        // Formatear fechas
        else if (col.dataType === 'date') {
          return value ? new Date(value).toLocaleDateString() : '';
        } 
        // Formatear números
        else if (col.dataType === 'numeric') {
          return Number(value) || 0;
        }
        // Valor por defecto (string)
        return value || '';
      });
    })
  ];

  // Crear hoja de trabajo
  const ws = utils.aoa_to_sheet(excelData);

  // Estilos para encabezados
  const headerStyle = {
    fill: { fgColor: { rgb: "2c3e50" } }, // Fondo oscuro
    font: { bold: true, color: { rgb: "FFFFFF" } }, // Texto blanco en negrita
    alignment: { horizontal: "center" }
  };

  // Aplicar estilos a la primera fila (encabezados)
  const range = utils.decode_range(ws['!ref']);
  for (let C = range.s.c; C <= range.e.c; ++C) {
    const cellAddress = utils.encode_cell({ r: 0, c: C });
    if (!ws[cellAddress].s) ws[cellAddress].s = {};
    Object.assign(ws[cellAddress].s, headerStyle);
  }

  // Ajustar anchos de columnas
  ws['!cols'] = headers.map(col => ({
    wch: Math.max(10, Math.min(30, col.title.length * 1.3))
  }));

  // Crear libro y guardar
  const wb = utils.book_new();
  utils.book_append_sheet(wb, ws, "Datos");

  const dateStr = new Date().toISOString().slice(0, 10);
  writeFile(wb, `${props.title || 'Reporte'}_${dateStr}.xlsx`);
};

const exportCSV2 = () => {
  exportingCSV.value = true;

  // Preparar los encabezados
  const headers = props.columns
    .filter(col => !col.excludeFromExport)
    .map(col => `"${col.header.replace(/"/g, '""')}"`); // Escapar comillas en encabezados

  // Preparar los datos
  const data = filteredData.value.map(row => {
    return props.columns
      .filter(col => !col.excludeFromExport)
      .map(col => {
        const value = row[col.field];
        
        // Manejar valores null/undefined primero
        if (value === null || value === undefined) return '';
        
        // Caso especial para booleanos (incluyendo el campo staff)
        if (col.dataType === 'boolean' || typeof value === 'boolean') {
          return value ? 'Sí' : 'No'; // Mostrar "No" cuando es false
        }
        // Formatear fechas
        else if (col.dataType === 'date') {
          return `"${value ? new Date(value).toLocaleDateString() : ''}"`;
        }
        // Formatear números
        else if (col.dataType === 'numeric') {
          return value ? Number(value) : '';
        }
        // Valor por defecto (string)
        return `"${String(value).replace(/"/g, '""')}"`; // Escapar comillas
      });
  });

  // Crear contenido CSV
  let csvContent = '';
  
  // Encabezados
  csvContent += headers.join(',') + '\r\n';
  
  // Datos
  data.forEach(row => {
    csvContent += row.join(',') + '\r\n';
  });

  // Crear blob y descargar
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);

  link.setAttribute('href', url);
  link.setAttribute('download', `${props.title || 'Reporte'}_${new Date().toISOString().slice(0, 10)}.csv`);
  link.style.visibility = 'hidden';

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  exportingCSV.value = false;
};


</script>

<style scoped>
.card {
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

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
  gap: 1rem;
}

.right-actions-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.header-search-container {
  min-width: 250px;
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
  font-size: 0.9rem;
}

.header-search-container .p-inputtext {
  padding-left: 2rem;
  width: 100%;
  height: 36px;
  font-size: 0.875rem;
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

@media (max-width: 768px) {
  .header-actions-container {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }

  .right-actions-container {
    width: 100%;
    justify-content: flex-end;
  }

  .header-search-container {
    width: 100%;
  }
}

/* expansion  */
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
  /* Ajusta este valor según necesites */
}
</style>