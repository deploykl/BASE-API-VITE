<template>
  <main id="main" class="main">
    <!-- Loading state -->
    <div v-if="tableroStore.loading" class="loading-container">
      <div class="spinner"></div>
      <p>Cargando tableros...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="tableroStore.error" class="error-container">
      <i class="fas fa-exclamation-triangle"></i>
      <h3>Error al cargar los tableros</h3>
      <p>{{ tableroStore.error.message || 'Error desconocido' }}</p>
      <button @click="loadTableros" class="retry-btn">Reintentar</button>
    </div>

    <!-- Content -->
    <div v-else class="tableros-container">
      <div class="header">
        <h1><i class="fas fa-chart-line"></i> Tableros BI</h1>
        <div class="filters-container">
          <div class="search-box">
            <i class="fas fa-search"></i>
            <input 
              v-model="searchQuery" 
              placeholder="Buscar tablero..." 
              type="text"
            >
          </div>
          
          <!-- Filtro por categoría -->
          <div class="filter-box">
            <i class="fas fa-filter"></i>
            <select v-model="selectedCategory" class="category-filter">
              <option value="">Todas las categorías</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>

          <!-- Filtro por fuente -->
          <div class="filter-box">
            <i class="fas fa-database"></i>
            <select v-model="selectedFuente" class="category-filter">
              <option value="">Todas las fuentes</option>
              <option v-for="fuente in fuentes" :key="fuente.id" :value="fuente.id">
                {{ fuente.nombre }} - {{ fuente.frecuencia || 'N/A' }}
              </option>
            </select>
          </div>

          <!-- Botón para limpiar filtros -->
          <button @click="clearFilters" class="clear-filters-btn">
            <i class="fas fa-times"></i> Limpiar
          </button>
        </div>
      </div>

      <div class="tableros-grid">
        <div 
          v-for="tablero in filteredTableros" 
          :key="tablero.id" 
          class="tablero-card"
          :class="{ 'disabled': !tablero.is_active }"
          @click="openTablero(tablero)"
        >
          <!-- Indicador de estado desactivado -->
          <div v-if="!tablero.is_active" class="disabled-overlay">
            <div class="disabled-label">
              <i class="fas fa-ban"></i> Desactivado
            </div>
          </div>
          
          <div class="tablero-icon">
            <i :class="getTableroIcon(tablero)"></i>
          </div>
          <div class="tablero-info">
            <h3>{{ tablero.name }}</h3>
            <p class="description">{{ tablero.description || 'Sin descripción' }}</p>
            
            <!-- Fuentes del tablero -->
            <div v-if="tablero.fuentes_detalles && tablero.fuentes_detalles.length" class="fuentes-container">
              <div class="fuentes-label">
                <i class="fas fa-database"></i> Fuentes:
              </div>
              <div class="fuentes-list">
                <span 
                  v-for="fuente in tablero.fuentes_detalles.slice(0, 2)" 
                  :key="fuente.id" 
                  class="fuente-badge"
                  :class="getFuenteCategoryClass(fuente)"
                >
                  {{ fuente.nombre }} - {{ fuente.frecuencia || 'N/A' }}
                </span>
                <span v-if="tablero.fuentes_detalles.length > 2" class="more-fuentes">
                  +{{ tablero.fuentes_detalles.length - 2 }} más
                </span>
              </div>
            </div>
            <div v-else class="no-fuentes">
              <i class="fas fa-info-circle"></i> Sin fuentes asignadas
            </div>

            <div class="tablero-meta">
              <span><i class="fas fa-sync-alt"></i> {{ tablero.update_frequency || 'N/A' }}</span>
              <span class="tablero-type">{{ getTableroType(tablero) }}</span>
            </div>
          </div>
          <div class="tablero-actions">
            <i class="fas fa-external-link-alt"></i>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="filteredTableros.length === 0" class="empty-state">
        <i class="fas fa-search"></i>
        <h3>No se encontraron tableros</h3>
        <p>Intenta con otros términos de búsqueda o cambia los filtros</p>
      </div>

      <!-- Modal para ambos tipos de tableros -->
      <div v-if="showModal && selectedTablero" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ selectedTablero.name }}</h2>
            <div class="modal-subtitle">
              <span v-if="selectedTablero.fuentes_detalles?.length" class="modal-fuentes">
                Fuentes: {{ selectedTablero.fuentes_detalles.map(f => f.nombre).join(', ') }}
              </span>
            </div>
            <button @click="closeModal" class="close-btn">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <!-- Power BI - usa iframe -->
            <div v-if="isPowerBI(selectedTablero)" class="iframe-container">
              <iframe 
                :src="selectedTablero.url" 
                frameborder="0" 
                allowFullScreen="true"
                @load="iframeLoaded"
                @error="iframeError"
              ></iframe>
            </div>
            
            <!-- Tableau - usa código embed -->
            <div v-else-if="isTableau(selectedTablero)" class="tableau-container">
              <div v-html="selectedTablero.codigo_embed"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted, nextTick } from 'vue';
import { useTableroStore } from '@/stores/dimon/tableroStore';

const tableroStore = useTableroStore();
const searchQuery = ref('');
const selectedCategory = ref('');
const selectedFuente = ref('');
const selectedTablero = ref(null);
const showModal = ref(false);

// Computed: Obtener todas las categorías únicas de las fuentes
const categories = computed(() => {
  const allCategories = new Set();
  
  tableroStore.tableros.forEach(tablero => {
    if (tablero.fuentes_detalles) {
      tablero.fuentes_detalles.forEach(fuente => {
        if (fuente.categoria_nombre) {
          allCategories.add(fuente.categoria_nombre);
        }
      });
    }
  });
  
  return Array.from(allCategories).sort();
});

// Computed: Obtener todas las fuentes únicas de los tableros
const fuentes = computed(() => {
  const allFuentes = new Map();
  
  tableroStore.tableros.forEach(tablero => {
    if (tablero.fuentes_detalles) {
      tablero.fuentes_detalles.forEach(fuente => {
        if (!allFuentes.has(fuente.id)) {
          allFuentes.set(fuente.id, {
            id: fuente.id,
            nombre: fuente.nombre,
            frecuencia: fuente.frecuencia,
            categoria: fuente.categoria_nombre
          });
        }
      });
    }
  });
  
  return Array.from(allFuentes.values()).sort((a, b) => 
    a.nombre.localeCompare(b.nombre)
  );
});

// Detectar tipo de tablero
const isPowerBI = (tablero) => {
  return tablero.source?.toLowerCase().includes('powerbi') || 
         tablero.url?.toLowerCase().includes('powerbi');
};

const isTableau = (tablero) => {
  return tablero.source?.toLowerCase().includes('tableau') || 
         tablero.url?.toLowerCase().includes('tableau') ||
         (tablero.codigo_embed && tablero.codigo_embed.includes('tableau'));
};

const getTableroIcon = (tablero) => {
  if (isTableau(tablero)) return 'fas fa-chart-pie';
  if (isPowerBI(tablero)) return 'fas fa-chart-bar';
  return 'fas fa-chart-line';
};

const getTableroType = (tablero) => {
  if (isTableau(tablero)) return 'Tableau';
  if (isPowerBI(tablero)) return 'Power BI';
  return 'BI';
};

// Obtener clase CSS para la categoría de la fuente
const getFuenteCategoryClass = (fuente) => {
  if (!fuente.categoria_nombre) return 'category-default';
  
  // Mapeo de categorías a clases CSS
  const categoryClasses = {
    'ventas': 'category-sales',
    'marketing': 'category-marketing',
    'finanzas': 'category-finance',
    'operaciones': 'category-operations',
    'recursos humanos': 'category-hr',
    'tecnología': 'category-tech',
    'tecnologia': 'category-tech'
  };
  
  const normalizedCategory = fuente.categoria_nombre.toLowerCase();
  return categoryClasses[normalizedCategory] || 'category-default';
};

// Limpiar todos los filtros
const clearFilters = () => {
  searchQuery.value = '';
  selectedCategory.value = '';
  selectedFuente.value = '';
};

// Filtrar y ordenar tableros basado en búsqueda, categoría, fuente y frecuencia
const filteredTableros = computed(() => {
  let filtered = tableroStore.tableros;
  
  // Filtro por búsqueda
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(tablero => 
      tablero.name.toLowerCase().includes(query) || 
      (tablero.description && tablero.description.toLowerCase().includes(query)) ||
      tablero.source.toLowerCase().includes(query) ||
      (tablero.fuentes_detalles && tablero.fuentes_detalles.some(fuente => 
        fuente.nombre.toLowerCase().includes(query)
      ))
    );
  }
  
  // Filtro por categoría
  if (selectedCategory.value) {
    filtered = filtered.filter(tablero => 
      tablero.fuentes_detalles && 
      tablero.fuentes_detalles.some(fuente => 
        fuente.categoria_nombre === selectedCategory.value
      )
    );
  }
  
  // Filtro por fuente específica
  if (selectedFuente.value) {
    const fuenteId = parseInt(selectedFuente.value);
    filtered = filtered.filter(tablero => 
      tablero.fuentes_detalles && 
      tablero.fuentes_detalles.some(fuente => 
        fuente.id === fuenteId
      )
    );
  }
  
  // Ordenar por frecuencia de actualización del tablero
  const frecuenciaOrden = {
    'Diario': 1,
    'Semanal': 2,
    'Mensual': 3,
    'Anual': 4,
    'Diaria': 1,
    'Quincenal': 2,
    'Trimestral': 3,
    'Semestral': 4,
    'N/A': 5
  };
  
  return filtered.sort((a, b) => {
    const prioridadA = frecuenciaOrden[a.update_frequency] || 5;
    const prioridadB = frecuenciaOrden[b.update_frequency] || 5;
    
    return prioridadA - prioridadB;
  });
});

// Abrir tablero
const openTablero = (tablero) => {
  if (!tablero.is_active) return;
  
  selectedTablero.value = tablero;
  showModal.value = true;
  document.body.style.overflow = 'hidden';
  
  // Si es Tableau, esperar a que el modal se renderice y luego ejecutar el script
  if (isTableau(tablero)) {
    nextTick(() => {
      setTimeout(() => {
        const tableauScripts = document.querySelectorAll('script[src*="tableau"]');
        tableauScripts.forEach(script => script.remove());
        
        if (tablero.codigo_embed) {
          // Extraer y ejecutar el script del código embed
          const scriptContent = tablero.codigo_embed.match(/<script\b[^>]*>([\s\S]*?)<\/script>/);
          if (scriptContent && scriptContent[1]) {
            try {
              new Function(scriptContent[1])();
            } catch (error) {
              console.error('Error ejecutando script de Tableau:', error);
            }
          }
        }
      }, 100);
    });
  }
};

// Cerrar modal
const closeModal = () => {
  showModal.value = false;
  selectedTablero.value = null;
  document.body.style.overflow = 'auto';
};

// Manejar eventos del iframe
const iframeLoaded = (event) => {
  console.log('Iframe cargado correctamente');
};

const iframeError = (event) => {
  console.error('Error al cargar el iframe:', event);
};

// Cargar tableros
const loadTableros = async () => {
  try {
    await tableroStore.ListTablero();
  } catch (error) {
    console.error('Error loading tableros:', error);
  }
};

// Inicialización
onMounted(async () => {
  await loadTableros();
});

// Limpiar al desmontar
onUnmounted(() => {
  if (showModal.value) {
    document.body.style.overflow = 'auto';
  }
});
</script>

<style scoped>
.main {
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fb;
  min-height: 100vh;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  color: #4a5568;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #4299e1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  padding: 40px;
  color: #e53e3e;
}

.error-container i {
  font-size: 48px;
  margin-bottom: 16px;
}

.retry-btn {
  background-color: #4299e1;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 16px;
}

.retry-btn:hover {
  background-color: #3182ce;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #718096;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.header h1 {
  color: #2d3748;
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0;
}

.filters-container {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.search-box, .filter-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box i, .filter-box i {
  position: absolute;
  left: 12px;
  color: #a0aec0;
  z-index: 1;
}

.search-box input, .category-filter {
  padding: 10px 15px 10px 40px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  outline: none;
}

.search-box input {
  width: 250px;
}

.search-box input:focus, .category-filter:focus {
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

.category-filter {
  width: 200px;
  cursor: pointer;
  appearance: none;
}

.clear-filters-btn {
  background-color: #e2e8f0;
  color: #4a5568;
  border: none;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.clear-filters-btn:hover {
  background-color: #cbd5e0;
}

.tableros-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.tablero-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  display: flex;
  cursor: pointer;
  position: relative;
  min-height: 200px;
}

.tablero-card:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.tablero-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.disabled-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.disabled-label {
  background-color: #e53e3e;
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.tablero-icon {
  margin-right: 16px;
  display: flex;
  align-items: flex-start;
}

.tablero-icon i {
  font-size: 24px;
  color: #4299e1;
  margin-top: 4px;
}

.tablero-card.disabled .tablero-icon i {
  color: #a0aec0;
}

.tablero-info {
  flex: 1;
}

.tablero-info h3 {
  margin: 0 0 8px 0;
  color: #2d3748;
  font-size: 16px;
  font-weight: 600;
  line-height: 1.3;
}

.tablero-card.disabled .tablero-info h3 {
  color: #a0aec0;
}

.description {
  margin: 0 0 12px 0;
  color: #718096;
  font-size: 14px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.fuentes-container {
  margin: 12px 0;
  padding: 12px;
  background-color: #f8fafc;
  border-radius: 8px;
  border-left: 4px solid #4299e1;
}

.fuentes-label {
  font-size: 12px;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.fuentes-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.fuente-badge {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 500;
  color: white;
  white-space: nowrap;
}

/* Estilos para diferentes categorías */
.category-default { background-color: #718096; }
.category-sales { background-color: #4299e1; }
.category-marketing { background-color: #48bb78; }
.category-finance { background-color: #9f7aea; }
.category-operations { background-color: #ed8936; }
.category-hr { background-color: #ecc94b; color: #2d3748; }
.category-tech { background-color: #f56565; }

.more-fuentes {
  font-size: 11px;
  color: #718096;
  font-style: italic;
  align-self: center;
}

.no-fuentes {
  font-size: 12px;
  color: #a0aec0;
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 8px 0;
}

.tablero-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
  font-size: 12px;
  color: #a0aec0;
}

.tablero-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.tablero-type {
  background-color: #e2e8f0;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
  color: #4a5568;
}

.tablero-actions {
  display: flex;
  align-items: flex-start;
}

.tablero-actions i {
  color: #a0aec0;
  font-size: 14px;
  margin-top: 4px;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 95%;
  height: 90%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.modal-header h2 {
  margin: 0;
  color: #2d3748;
  font-size: 1.5rem;
  flex: 1;
}

.modal-subtitle {
  flex: 1;
  margin-left: 16px;
}

.modal-fuentes {
  font-size: 14px;
  color: #718096;
  font-style: italic;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #718096;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: #e2e8f0;
  color: #2d3748;
}

.modal-body {
  flex: 1;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.iframe-container, .tableau-container {
  flex: 1;
  width: 100%;
  height: 100%;
}

.iframe-container iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.tableau-container {
  overflow: auto;
}

.tableau-container > div {
  width: 100%;
  height: 100%;
  min-height: 600px;
}

/* Asegurar que el contenido de Tableau se vea bien */
.tableau-container .tableauPlaceholder {
  width: 100% !important;
  height: 100% !important;
}

.tableau-container .tableauViz {
  width: 100% !important;
  height: 100% !important;
}

/* Responsive */
@media (max-width: 1024px) {
  .filters-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box input, .category-filter {
    width: 100%;
  }
  
  .clear-filters-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .filters-container {
    width: 100%;
    gap: 12px;
  }
  
  .tableros-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    width: 100%;
    height: 85%;
    margin: 0;
  }
  
  .modal-header {
    flex-direction: column;
    gap: 12px;
  }
  
  .modal-subtitle {
    margin-left: 0;
  }
  
  .modal-body {
    height: calc(100% - 80px);
  }
}

@media (max-width: 480px) {
  .main {
    padding: 16px;
  }
  
  .fuentes-list {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .fuente-badge {
    width: fit-content;
  }
  
  .tablero-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .modal-overlay {
    padding: 10px;
  }
  
  .modal-content {
    height: 90%;
  }
}
</style>