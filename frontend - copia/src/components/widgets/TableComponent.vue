<template>
    <div>
        <!-- Filtros y Número de filas por página (en la misma fila) -->
        <div class="col-md-12">
            <div class="row g-1 justify-content-start align-items-center">
                <!-- Filtros para cada header -->
                <div v-for="header in headers" :key="header.key" class="col-md-3">
                    <!-- Si el filtro está activo, muestra la etiqueta -->
                    <div class="filter-label" v-if="isFilterActive(header.key)">
                        {{ header.label }}
                    </div>
                    <!-- Select para filtrar si es filtrable -->
                    <select v-if="header.filterable" class="form-select" v-model="filters[header.key]"
                        @change="applyFilters">
                        <option value="">-- Todos --</option>
                        <option v-for="value in uniqueValues(header.key)" :key="value" :value="value">
                            {{ formatFilterOption(header.key, value) }}
                        </option>
                    </select>
                </div>

                <!-- Select para seleccionar cantidad de filas por página -->
                <div class="col-md-1">
                    <label for="rows-per-page" class="form-label">Pag.</label>
                    <select id="rows-per-page" class="form-select" v-model="rowsPerPage" @change="applyFilters">
                        <option value="10">10</option>
                        <option value="15">15</option>
                        <option value="25">25</option>
                        <option value="50">50</option>
                    </select>
                </div>
            </div>
        </div>


        <!-- Buscador global y Selección múltiple (en la misma fila) -->
        <div class="mb-3">
            <div class="row align-items-center">
                <!-- Selección múltiple y botón de eliminación -->
                <div class="col-md-6 d-flex justify-content-start">
                    <button type="button" class="btn btn-danger mt-3 mb-2 me-2" @click="deleteSelectedItems"
                        :disabled="selectedItems.length === 0">
                        <i class="fas fa-trash-alt"></i> Elim. Sel.
                        <span v-if="selectedItems.length > 0" class="badge rounded-pill bg-white text-danger ms-2">
                            {{ selectedItems.length }}
                        </span>
                    </button>
                    <export-buttons-vue />
                </div>
                <!-- Buscador global -->
                <div class="col-md-6 mb-2 d-flex justify-content-end">
                    <div class="search-container">
                        <div class="input-group">
                            <input type="text" v-model="searchTerm" class="search-input" placeholder="Buscar..." />
                            <span class="input-group-text">
                                <i class="fas fa-search"></i>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="table-responsive">
            <table class="table table-hover table-sm">
                <thead>
                    <tr>
                        <th class="">
                            <input type="checkbox" :checked="isAllSelected" @change="toggleAll" />
                            <i class="fas fa-trash-alt"></i>
                        </th>
                        <th>N°</th>
                        <th v-for="header in headers" :key="header.key" :class="getColumnStyle(header.key).class">
                            <div class="d-flex">
                                <span>{{ header.label }}</span>
                            </div>
                        </th>
                        <th v-if="showActions">OPCIONES</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in paginatedItems" :key="item.id">
                        <td>
                            <input type="checkbox" :value="item.id" v-model="selectedItems" />
                        </td>
                        <td>{{ startIndex + index + 1 }}</td>
                        <td v-for="header in headers.filter(header => header.key !== 'id')" :key="header.key">
                            <span v-html="formatValue(header.key, item[header.key])"></span>
                        </td>
                        <td v-if="showActions" class="justify-content-between">
                            <button type="button" class="btn btn-warning btn-sm me-2" @click="$emit('edit', item)">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button type="button" class="btn btn-danger btn-sm" @click="$emit('delete', item.id)">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <!-- Controles de Paginación -->
        <div class="d-flex justify-content-between align-items-center mt-3">
            <div>
                <button class="btn btn-custom btn-sm me-2" :disabled="currentPage <= 1" @click="currentPage = 1"
                    title="Primera página">
                    <i class="fas fa-angle-double-left"></i>
                </button>
                <button class="btn btn-custom btn-sm me-2" :disabled="currentPage <= 1" @click="currentPage--"
                    title="Página anterior">
                    <i class="fas fa-chevron-left"></i>
                </button>
                <span class="pagination-info text-muted">
                    Página <strong>{{ currentPage }}</strong> de <strong>{{ totalPages }}</strong> | Total: <strong>{{
                        totalRecords }}</strong>
                </span>
                <button class="btn btn-custom btn-sm ms-2" :disabled="currentPage >= totalPages" @click="currentPage++"
                    title="Página siguiente">
                    <i class="fas fa-chevron-right"></i>
                </button>
                <button class="btn btn-custom btn-sm ms-2" :disabled="currentPage >= totalPages"
                    @click="currentPage = totalPages" title="Última página">
                    <i class="fas fa-angle-double-right"></i>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, defineEmits } from 'vue';
import ExportButtonsVue from './buttons/ExportButtons.vue';
const startIndex = computed(() => (currentPage.value - 1) * rowsPerPage.value);

// Props
const props = defineProps({
    headers: {
        type: Array,
        required: true,
    },
    items: {
        type: Array,
        required: true,
    },
    showActions: {
        type: Boolean,
        default: true,
    },
    columnStyles: {
        type: Object,
        default: () => ({}),
    },
});

// Emitir eventos
const emit = defineEmits(['edit', 'delete', 'delete-multiple']);

// Estado reactivo
const searchTerm = ref('');
const filters = ref(
    props.headers.reduce((acc, header) => {
        if (header.filterable) {
            acc[header.key] = '';
        }
        return acc;
    }, {})
);
const rowsPerPage = ref(15);
const currentPage = ref(1);
const selectedItems = ref([]);
const sortKey = ref('');
const sortOrder = ref('asc');

// Propiedades computadas
const filteredItems = computed(() => {
    if (!props.items) return [];

    let items = props.items;

    // Aplicar filtro por término de búsqueda
    if (searchTerm.value) {
        const lowerCaseSearchTerm = searchTerm.value.toLowerCase();
        items = items.filter(item =>
            Object.values(item).some(value =>
                String(value).toLowerCase().includes(lowerCaseSearchTerm)
            )
        );
    }

    // Aplicar filtros de columnas
    for (const key in filters.value) {
        if (filters.value[key] !== '') {
            items = items.filter(item =>
                String(item[key]) === String(filters.value[key])
            );
        }
    }

    // Aplicar ordenación
    if (sortKey.value) {
        items.sort((a, b) => {
            const aValue = a[sortKey.value];
            const bValue = b[sortKey.value];
            if (aValue < bValue) return sortOrder.value === 'asc' ? -1 : 1;
            if (aValue > bValue) return sortOrder.value === 'asc' ? 1 : -1;
            return 0;
        });
    }

    return items;
});

const paginatedItems = computed(() => {
    const start = (currentPage.value - 1) * rowsPerPage.value;
    const end = start + rowsPerPage.value;

    const filtered = filteredItems.value;

    if (filtered.length === 0) return [];

    return filtered.slice(start, end);
});

const totalPages = computed(() => {
    return Math.ceil(filteredItems.value.length / rowsPerPage.value);
});

const isFilterActive = (key) => {
    const header = props.headers.find(header => header.key === key);
    return header && header.filterable;
};

const isAllSelected = computed(() => {
    if (!filteredItems.value) return false;
    return selectedItems.value.length === filteredItems.value.length;
});

const formatValue = (header, value) => {
    if (header === 'estado') {
        const badgeClass = value ? 'badge text-bg-success' : 'badge text-bg-danger';
        const iconClass = value ? 'bi bi-check-circle me-1' : 'bi bi-exclamation-octagon me-1';
        const text = value ? 'Activo' : 'Inactivo';
        return `<span class="${badgeClass}"><i class="${iconClass}"></i>${text}</span>`;
    }
    return value;
};

const formatFilterOption = (header, value) => {
    if (header === 'estado') {
        return value === 'true' ? 'Activo' : 'Inactivo';
    }
    return value;
};

const uniqueValues = (key) => {
    if (key === 'estado') {
        return ['true', 'false'];
    }
    const values = new Set(props.items.map(item => item[key] === undefined ? 'VACÍO' : item[key]));
    return Array.from(values).map(value => String(value));
};

const getColumnStyle = (key) => {
    const columnStyle = props.columnStyles?.[key];
    return columnStyle ? { class: columnStyle } : {}; // Aplica la clase directamente
};


// Observadores
watch([filters, rowsPerPage, searchTerm], () => {
    currentPage.value = 1; // Reiniciar a la primera página al aplicar filtros o búsqueda
});

const applyFilters = () => {
    currentPage.value = 1; // Restablecer a la primera página al aplicar filtros
};

const sort = (key, order) => {
    sortKey.value = key;
    sortOrder.value = order;
};

function deleteSelectedItems() {
    if (selectedItems.value.length === 0) return;

    // Emitir el evento para eliminar los elementos seleccionados
    emit('delete-multiple', selectedItems.value);

    // Aquí no restablecemos selectedItems
    // Puedes optar por mantenerlo como está o realizar alguna acción adicional
}
const totalRecords = computed(() => {
    return filteredItems.value.length;
});


function toggleAll(event) {
    if (event.target.checked) {
        selectedItems.value = filteredItems.value.map(item => item.id);
    } else {
        selectedItems.value = [];
    }
}


</script>

<style scoped>
.table td,
.table th {
    vertical-align: middle;
}

.search-container {
    position: relative;
    display: flex;
    align-items: center;
}

.search-input {
    width: 150px;
    transition: width 0.4s ease-in-out;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    padding: 0.375rem 0.75rem;
}

.search-input:focus {
    width: 250px;
    border-color: #80bdff;
    outline: none;
}

.input-group-text {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    border-left: 0;
    border-radius: 0 0.25rem 0.25rem 0;
    display: flex;
    align-items: center;
    padding: 0.375rem 0.75rem;
}

.input-group-text i {
    color: #007bff;
}

/* ICONS ASC Y DESC  */
.sort-icons {
    display: flex;
    flex-direction: column;
    /* Alinea los íconos en una columna */
    align-items: center;
    /* Centra los íconos horizontalmente */
    gap: 0px;
    /* Espacio entre los íconos */
    margin-left: auto;
    /* Alinea el contenedor de íconos a la derecha */
}

.sort-icons i {
    cursor: pointer;
    font-size: 12px;
    /* Tamaño del ícono */
    color: #6c757d;
    /* Color por defecto de los íconos */
}

.sort-icons .text-primary {
    color: #8f1212;
    /* Color del ícono activo */
}

.card-footer {
    border-top: 1px solid #dee2e6;
}

/*  ======================  TABLE ========================*/
.table {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    /* Añade sombra a la tabla */
    overflow: hidden;
    /* Asegura que las esquinas redondeadas se mantengan */
    border-radius: 20px;
    transition: transform 0.2s ease;
}

.table th {
    background-color: #54618E;
    padding: 5px 10px 5px 10px;
    color: white;
    border-radius: 1px;
    box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.2);
    /* Sombra inferior en los encabezados */

}

.table th::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 5px;
    background-color: #54618E;
    transform: scaleX(0);
    transition: transform 0.5s ease;
}

.table th:hover::after {
    transform: scaleX(1);
}

.table tbody::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 5px;
    background-color: #54618E;
    transform: scaleX(0);
    transition: transform 0.5s ease;
}

.table tbody:hover::after {
    transform: scaleX(1);
}

.table td {
    vertical-align: middle;
    /* Alineación vertical de los contenidos de las celdas */
    text-align: justify;
    transition: background-color 0.3s ease;
    padding-left: 10px;

}

.table tbody tr {
    transition: background-color 0.3s ease;
}

.table tbody tr:hover {
    transition: background-color 0.2s ease;
    /* Añade una transición suave */
}

.table td:hover {
    background-color: transparent;
    /* Evita que el color de fondo se aplique a las celdas */
}

/* PAGINACIÓN */
.btn-custom {
    background-color: #54618E;
    color: white;
    border-radius: 4px;
    /* Bordes redondeados en los botones */

}

.btn-custom:disabled {
    background-color: #b0b0b0;
    /* Un color gris claro para el estado deshabilitado */
    color: #6c757d;
    /* Un color gris oscuro para el texto deshabilitado */
    cursor: not-allowed;
    /* Cambia el cursor para mostrar que el botón no está disponible */
}

.btn-custom:hover {
    background-color: white !important;
    /* Color más oscuro al pasar el mouse sobre los botones */
    color: #54618E;
    border: 1px solid #54618E;
}
</style>
