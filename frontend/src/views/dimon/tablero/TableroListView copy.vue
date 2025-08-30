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
      <p>{{ tableroStore.error }}</p>
      <button @click="loadTableros" class="retry-btn">Reintentar</button>
    </div>

    <!-- Content -->
    <div v-else class="tableros-container">
      <div class="header">
        <h1><i class="fas fa-chart-line"></i> Tableros BI</h1>
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input 
            v-model="searchQuery" 
            placeholder="Buscar tablero..." 
            type="text"
          >
        </div>
      </div>

      <div class="tableros-grid">
        <div 
          v-for="tablero in filteredTableros" 
          :key="tablero.id" 
          class="tablero-card"
          @click="openTablero(tablero)"
        >
          <div class="tablero-icon">
            <i :class="getTableroIcon(tablero)"></i>
          </div>
          <div class="tablero-info">
            <h3>{{ tablero.name }}</h3>
            <p>{{ tablero.description || 'Sin descripción' }}</p>
            <div class="tablero-meta">
              <span><i class="fas fa-database"></i> {{ tablero.source }}</span>
              <span><i class="fas fa-sync-alt"></i> {{ tablero.update_frequency || 'N/A' }}</span>
              <span class="tablero-type">{{ getTableroType(tablero) }}</span>
            </div>
          </div>
          <div class="tablero-actions">
            <i class="fas fa-external-link-alt"></i>
          </div>
        </div>
      </div>

      <!-- Modal solo para Power BI -->
      <div v-if="selectedTablero && isPowerBI(selectedTablero)" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ selectedTablero.name }}</h2>
            <button @click="closeModal" class="close-btn">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <iframe 
              :src="selectedTablero.url" 
              frameborder="0" 
              allowFullScreen="true"
              @load="iframeLoaded"
              @error="iframeError"
            ></iframe>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed, watch, onUnmounted } from 'vue';
import { useTableroStore } from '@/stores/dimon/tableroStore';

const tableroStore = useTableroStore();
const searchQuery = ref('');
const selectedTablero = ref(null);

// Detectar tipo de tablero
const isPowerBI = (tablero) => {
  return tablero.source?.toLowerCase().includes('powerbi') || 
         tablero.url?.toLowerCase().includes('powerbi') ||
         !isTableau(tablero);
};

const isTableau = (tablero) => {
  return tablero.source?.toLowerCase().includes('tableau') || 
         tablero.url?.toLowerCase().includes('tableau');
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

// Filtrar tableros basado en la búsqueda
const filteredTableros = computed(() => {
  if (!searchQuery.value) return tableroStore.tableros;
  
  const query = searchQuery.value.toLowerCase();
  return tableroStore.tableros.filter(tablero => 
    tablero.name.toLowerCase().includes(query) || 
    (tablero.description && tablero.description.toLowerCase().includes(query)) ||
    tablero.source.toLowerCase().includes(query)
  );
});

// Abrir tablero
const openTablero = (tablero) => {
  if (isTableau(tablero)) {
    // Tableau se abre en nueva pestaña
    window.open(tablero.url, '_blank', 'noopener,noreferrer');
  } else {
    // Power BI se abre en modal
    selectedTablero.value = tablero;
    document.body.style.overflow = 'hidden';
  }
};

// Cerrar modal
const closeModal = () => {
  selectedTablero.value = null;
  document.body.style.overflow = 'auto';
};

// Manejar eventos del iframe
const iframeLoaded = (event) => {
  console.log('Iframe cargado correctamente');
};

const iframeError = (event) => {
  console.error('Error al cargar el iframe:', event);
  // Opcional: mostrar mensaje de error al usuario
};

// Cargar tableros
const loadTableros = async () => {
  try {
    tableroStore.loading = true;
    await tableroStore.ListTablero();
  } catch (error) {
    console.error('Error loading tableros:', error);
  } finally {
    tableroStore.loading = false;
  }
};

// Inicialización
onMounted(async () => {
  await loadTableros();
});

// Limpiar al desmontar
onUnmounted(() => {
  if (selectedTablero.value) {
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
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box i {
  position: absolute;
  left: 12px;
  color: #a0aec0;
}

.search-box input {
  padding: 10px 15px 10px 40px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  width: 300px;
  font-size: 14px;
}

.tableros-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.tablero-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  cursor: pointer;
  position: relative;
}

.tablero-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.tablero-icon {
  margin-right: 16px;
  display: flex;
  align-items: center;
}

.tablero-icon i {
  font-size: 24px;
  color: #4299e1;
}

.tablero-info {
  flex: 1;
}

.tablero-info h3 {
  margin: 0 0 8px 0;
  color: #2d3748;
  font-size: 16px;
}

.tablero-info p {
  margin: 0 0 12px 0;
  color: #718096;
  font-size: 14px;
  line-height: 1.4;
}

.tablero-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: #a0aec0;
}

.tablero-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.tablero-actions {
  display: flex;
  align-items: flex-start;
}

.tablero-actions i {
  color: #a0aec0;
  font-size: 14px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
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
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h2 {
  margin: 0;
  color: #2d3748;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #718096;
  padding: 4px 8px;
  border-radius: 4px;
}

.close-btn:hover {
  background-color: #f7fafc;
  color: #2d3748;
}

.modal-body {
  flex: 1;
  padding: 0;
  z-index: 1020;
}

.modal-body iframe {
  width: 100%;
  height: 100%;
  border: none;
}

/* Responsive */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .search-box input {
    width: 100%;
  }
  
  .tableros-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    width: 100%;
    height: 85%;
  }
}
</style>