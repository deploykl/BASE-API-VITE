<template>
  <!-- Botón flotante de música (solo visible cuando el panel está oculto) -->
  <div class="music-floating-btn" v-if="!showMusicPanel" @click="toggleMusicPanel">
    <i :class="isPlaying ? 'pi pi-pause' : 'pi pi-volume-up'"></i>
  </div>

  <!-- Panel de controles de música (visible cuando está activo o reproduciendo) -->
  <div class="music-player-panel" v-if="showMusicPanel || isPlaying">
    <div class="d-flex align-items-center">
      <button class="btn btn-sm btn-outline-primary rounded-circle me-2" @click="togglePlayback">
        <i :class="isPlaying ? 'pi pi-pause' : 'pi pi-play'"></i>
      </button>
      <small class="text-muted status-indicator">
        {{ isPlaying ? 'Reproduciendo' : 'Pausado' }}
      </small>
      <button class="btn btn-sm btn-outline-secondary rounded-circle ms-2" @click="hideMusicPanel">
        <i class="pi pi-times"></i>
      </button>
    </div>

    <div class="volume-controls mt-2">
      <i class="pi pi-volume-down text-primary"></i>
      <input type="range" class="form-range volume-slider" min="0" max="1" step="0.1" :value="volume"
        @input="adjustVolume($event.target.value)">
      <i class="pi pi-volume-up text-primary"></i>
    </div>
  </div>
  <div class="modern-container">
    <!-- Barra de navegación -->
    <nav class="navbar navbar-expand-lg navbar-modern fixed-top">
      <div class="container">
        <router-link to="/" class="navbar-brand navbar-brand-modern">
          <img src="/src/assets/img/logo2.png" alt="Logo HGA" class="navbar-logo me-2">
          DGOS
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent"
          aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <button class="nav-link" href="#" @click="scrollToSection('modules')">Módulos</button>
            </li>
            <li class="nav-item">
              <button class="nav-link" href="#" @click="scrollToSection('benefits')">Beneficios</button>
            </li>
            <li class="nav-item">
              <button class="nav-link" href="#" @click="scrollToSection('features')">Características</button>
            </li>
            <li class="nav-item">
              <button class="nav-link" href="#" @click="scrollToSection('about')">Nosotros</button>
            </li>
            <li class="nav-item">
              <button class="nav-link" href="#" @click="scrollToSection('contact')">Contacto</button>
            </li>
          </ul>

          <div class="d-flex">
            <button v-if="isAuthenticated" @click="goToDashboard" class="btn btn-outline-primary btn-sm me-2">
              <i class="pi pi-cog me-1"></i> <!-- icono engranaje -->
              Admin
            </button>

            <router-link v-else to="/login">
              <Button label="Acceso Admin" icon="pi pi-sign-in" iconPos="left" severity="info" variant="outlined"
                size="small" />
            </router-link>

          </div>
        </div>
      </div>
    </nav>



    <!-- Espacio para el navbar fijo -->
    <div class="navbar-spacer"></div>

    <!-- Contenido principal -->
    <div class="main-content">
      <!-- Header con logo y título -->
      <header class="header-title text-center">
        <h1 class="display-5 fw-bold text-primary">SISTEMA INTEGRADO DE GESTIÓN - DGOS</h1>
        <small class="text-muted">DGOS - DIMON - DIEM</small>
      </header>
      <Divider />

      <!-- Alert de novedad -->
      <div class="alert-modern d-flex justify-content-center align-items-center mb-5 mx-auto" role="alert">
        <div class="alert-icon-container me-3">
          <i class="pi pi-megaphone"></i>
        </div>
        <Badge class="text-center" severity="info">
          Novedad: Lanzamiento de la Versión (v2.0) nuevos módulos: (Personal, Tableros)
        </Badge>
      </div>

      <!-- Módulos principales -->
      <section id="modules" class="modules-section mb-5">
        <h2 class="section-title text-center mb-4">
          <span class="title-decoration"></span>
          <i class="pi pi-th-large me-2"></i>Módulos Principales
          <span class="title-decoration"></span>
        </h2>

        <!-- Breadcrumb para navegación entre grupos -->
        <div class="module-breadcrumb mb-4" v-if="currentGroup !== 'main'">
          <button class="btn btn-back-elegant" @click="goBackToMain">
            <i class="pi pi-arrow-left me-1"></i> Volver
          </button>
          <span class="text-muted">Grupo actual: {{ getGroupName(currentGroup) }}</span>
        </div>

        <!-- Vista de módulos principales -->
        <div v-if="currentGroup === 'main'" class="row justify-content-center g-4">
          <div v-for="group in moduleGroups" :key="group.id" class="col-10 col-sm-6 col-md-4 col-lg-3">
            <div class="elegant-group-card p-4 rounded-4 text-center h-100 position-relative"
              @click="selectGroup(group.id)">
              <div class="elegant-icon-container mb-3 mx-auto" :style="{ '--icon-color': group.color }">
                <i :class="group.icon" class="elegant-icon"></i>
              </div>
              <h5 class="fw-bold mb-2 elegant-title">{{ group.name }}</h5>
              <p class="small text-muted mb-3">{{ group.description }}</p>
              <div class="elegant-module-count">
                <Badge severity="info">{{ group.modules.length }} módulos</Badge>
              </div>
              <div class="elegant-hover-indicator">
                <Button icon="pi pi-arrow-right" iconPos="right" severity="info"
                  class="p-button-sm p-button-outlined p-button-rounded" />
              </div>
            </div>
          </div>
        </div>

        <!-- Vista de módulos específicos de un grupo -->
        <div v-else class="row justify-content-center g-4">
          <div v-for="module in getCurrentGroupModules()" :key="module.id" class="col-10 col-sm-6 col-md-4 col-lg-3">
            <div class="elegant-module-card p-4 rounded-4 h-100 position-relative d-flex flex-column"
              :class="{ 'module-enabled': module.enabled, 'module-disabled': !module.enabled }"
              @click="module.enabled ? redirectToModule(module.path) : null">

              <!-- Badge para módulos deshabilitados -->
              <div v-if="!module.enabled" class="position-absolute top-0 end-0 m-2">
                <span class="badge bg-warning text-dark px-2 py-1 coming-soon-badge">
                  <i class="pi pi-clock me-1"></i> Próximamente
                </span>
              </div>

              <div class="elegant-icon-container mb-3 mx-auto" :style="{ '--icon-color': module.color }">
                <i :class="module.icon" class="elegant-icon"></i>
              </div>

              <h5 class="fw-bold mb-2 elegant-title text-center">{{ module.title }}</h5>
              <p class="small text-muted mb-3 text-center">{{ module.description }}</p>

              <div class="elegant-action-btn mt-auto text-center">
                <Button v-if="module.enabled" class="btn btn-primary btn-sm" size="small" severity="info">
                  Acceder <i class="pi pi-arrow-right ms-1"></i>
                </Button>
                <button v-else class="btn btn-outline-secondary btn-sm" disabled>
                  No disponible
                </button>
              </div>

              <div class="elegant-card-decoration"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- Sección de beneficios -->
      <section id="benefits" class="benefits-section mb-5">
        <h2 class="section-title text-center mb-4">
          <span class="title-decoration"></span>
          <i class="bi bi-award me-2"></i>Beneficios Principales
          <span class="title-decoration"></span>
        </h2>

        <div class="row justify-content-center g-4">
          <div class="col-md-6 col-lg-3">
            <div class="benefit-card text-center p-4 rounded-4 h-100">
              <div class="benefit-icon mb-3">
                <i class="bi bi-graph-up-arrow"></i>
              </div>
              <h5>Eficiencia Mejorada</h5>
              <p class="text-muted">Automatiza procesos administrativos y reduces tiempos de ejecución.</p>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="benefit-card text-center p-4 rounded-4 h-100">
              <div class="benefit-icon mb-3">
                <i class="bi bi-shield-check"></i>
              </div>
              <h5>Seguridad de Datos</h5>
              <p class="text-muted">Protección avanzada para toda la información institucional.</p>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="benefit-card text-center p-4 rounded-4 h-100">
              <div class="benefit-icon mb-3">
                <i class="bi bi-lightning-charge"></i>
              </div>
              <h5>Rapidez</h5>
              <p class="text-muted">Acceso rápido a la información y reportes en tiempo real.</p>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="benefit-card text-center p-4 rounded-4 h-100">
              <div class="benefit-icon mb-3">
                <i class="bi bi-bar-chart"></i>
              </div>
              <h5>Toma de Decisiones</h5>
              <p class="text-muted">Dashboards intuitivos para una mejor visualización de datos.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Sección de características -->
      <section id="features" class="features-section mb-5">
        <h2 class="section-title text-center mb-4">
          <span class="title-decoration"></span>
          <i class="bi bi-stars me-2"></i>Características Destacadas
          <span class="title-decoration"></span>
        </h2>

        <div class="row align-items-center">
          <div class="col-lg-6">
            <div class="feature-item d-flex mb-4">
              <div class="feature-icon me-4">
                <i class="bi bi-check2-circle"></i>
              </div>
              <div>
                <h5>Interfaz Intuitiva</h5>
                <p class="text-muted mb-0">Diseño moderno y fácil de usar que requiere mínima capacitación.</p>
              </div>
            </div>

            <div class="feature-item d-flex mb-4">
              <div class="feature-icon me-4">
                <i class="bi bi-check2-circle"></i>
              </div>
              <div>
                <h5>Integración Total</h5>
                <p class="text-muted mb-0">Todos los módulos conectados entre sí para un flujo de trabajo unificado.</p>
              </div>
            </div>

            <div class="feature-item d-flex mb-4">
              <div class="feature-icon me-4">
                <i class="bi bi-check2-circle"></i>
              </div>
              <div>
                <h5>Acceso Móvil</h5>
                <p class="text-muted mb-0">Disponible desde cualquier dispositivo con conexión a internet.</p>
              </div>
            </div>
          </div>

          <div class="col-lg-6 text-center">
            <div class="feature-visual p-4 rounded-4">
              <i class="bi bi-laptop"></i>
              <div class="mt-3">
                <h5>Plataforma Unificada</h5>
                <p class="text-muted">Todas las herramientas en un solo lugar</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Sección Nosotros -->
      <section id="about" class="about-section mb-4">
        <h2 class="section-title text-center mb-4">
          <span class="title-decoration"></span>
          <i class="bi bi-people me-2"></i>Nosotros
          <span class="title-decoration"></span>
        </h2>

        <div class="row justify-content-center">
          <div class="col-lg-8 text-center">
            <p class="lead">
              Somos el área de Tecnologías de la Información de la DGOS, dedicados a desarrollar
              soluciones innovadoras que mejoren la gestión administrativa y optimicen los procesos
              institucionales.
            </p>
          </div>
        </div>
      </section>

      <!-- Sección Contacto -->
      <section id="contact" class="contact-section mb-5">
        <h2 class="section-title text-center mb-4">
          <span class="title-decoration"></span>
          <i class="bi bi-envelope me-2"></i>Contacto
          <span class="title-decoration"></span>
        </h2>

        <div class="row justify-content-center">
          <div class="col-lg-6">
            <div class="contact-card p-4 rounded-4 text-center">
              <i class="bi bi-headset contact-icon mb-3"></i>
              <h5>Soporte Técnico</h5>
              <p class="text-muted">Estamos aquí para ayudarte con cualquier consulta o problema técnico.</p>
              <p class="mb-0">
                <i class="bi bi-envelope me-2"></i>
                <a href="mailto:soporte@dgos.gob.pe">dgos.staff@minsa.gob.pe</a>
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="footer-modern py-4 bg-light">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-lg-5 text-center text-lg-start mb-lg-0">
              <p class="mb-0">
                <span class="text-muted">&copy; {{ currentYear }} - Desarrollado por</span>
                <span class="fw-medium text-primary ms-1">área de TI de la DGOS</span>
              </p>
            </div>

            <div class="col-lg-7 text-center text-lg-end">
              <div
                class="d-inline-flex flex-wrap justify-content-center justify-content-lg-end align-items-center gap-2">
                <small class="text-muted">Tecnologías:</small>
                <span v-for="(tech, index) in technologies" :key="index"
                  class="tech-badge-modern d-flex align-items-center">
                  <img :src="tech.icon" :alt="tech.name" class="tech-icon me-1" />
                  {{ tech.name }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = computed(() => {
  const token = localStorage.getItem('auth_token');
  return !!token;
});

const currentYear = ref(new Date().getFullYear());
const currentGroup = ref('main');

// Array de tecnologías para el footer
const technologies = ref([
  { name: 'Python', icon: '/src/assets/svg/python.svg' },
  { name: 'Vuejs3', icon: '/src/assets/svg/vuejs.svg' },
  { name: 'Sql Server', icon: '/src/assets/svg/sql_server.svg' },
  { name: 'Vite', icon: '/src/assets/svg/vite.svg' },
  { name: 'Pinia', icon: '/src/assets/svg/pinia.svg' },
  { name: 'WebSocket', icon: '/src/assets/svg/websocket.svg' }
]);

// Array de módulos para renderizar dinámicamente
const moduleGroups = ref([
  {
    id: 'hga',
    name: 'HGA - DGOS',
    description: 'Herramientas de Gestión Administrativa',
    icon: 'pi pi-building',
    color: '#6f42c1',
    modules: [
      {
        id: 1,
        title: 'Personal',
        description: 'Gestión de usuarios y permisos del sistema',
        icon: 'pi pi-users',
        color: '#6f42c1',
        path: '/dgos/personal',
        enabled: true
      },
      {
        id: 2,
        title: 'POI',
        description: 'Planeamiento Operativo Institucional',
        icon: 'pi pi-calendar',
        color: '#ffc107',
        path: '/dashboard',
        enabled: false
      },
      {
        id: 3,
        title: 'Informática',
        description: 'Control de equipos y recursos tecnológicos',
        icon: 'pi pi-desktop',
        color: '#28a745',
        path: '/dashboard',
        enabled: false
      }
    ]
  },
  {
    id: 'dimon',
    name: 'DIMON',
    description: 'Herramientas de Monitoreo',
    icon: 'pi pi-chart-line',
    color: '#007bff',
    modules: [
      {
        id: 4,
        title: 'Tableros',
        description: 'Dashboards e indicadores de gestión',
        icon: 'pi pi-chart-line',
        color: '#007bff',
        path: '/dimon/tablero',
        enabled: true
      },
      {
        id: 5,
        title: 'Pool vehicular',
        description: 'Control de vehículos y asignaciones',
        icon: 'pi pi-car',
        color: '#0B5ED7',
        path: '/dashboard',
        enabled: false
      }
    ]
  },
  {
    id: 'diem',
    name: 'DIEM',
    description: 'Herramientas de mantenimiento ',
    icon: 'bi bi-buildings',
    color: '#fd7e14',
    modules: [
      {
        id: 6,
        title: 'Patrimonio',
        description: 'Control de bienes y activos fijos',
        icon: 'pi pi-box',
        color: '#fd7e14',
        path: '/dashboard',
        enabled: false
      },
      {
        id: 7,
        title: 'Gasto',
        description: 'Seguimiento de presupuesto y gastos',
        icon: 'pi pi-money-bill',
        color: '#ffb300',
        path: '/dashboard',
        enabled: false
      },
      {
        id: 8,
        title: 'Reuniones',
        description: 'Agenda y actas de reuniones',
        icon: 'pi pi-clock',
        color: '#28a745',
        path: '/dashboard',
        enabled: false
      }
    ]
  }
]);

// Función para obtener el nombre de un grupo por su ID
const getGroupName = (groupId) => {
  const group = moduleGroups.value.find(g => g.id === groupId);
  return group ? group.name : '';
};

// Función para obtener los módulos del grupo actual
const getCurrentGroupModules = () => {
  const group = moduleGroups.value.find(g => g.id === currentGroup.value);
  return group ? group.modules : [];
};

// Función para seleccionar un grupo
const selectGroup = (groupId) => {
  currentGroup.value = groupId;
  setTimeout(() => {
    scrollToSection('modules');
  }, 100);
};

// Función para volver al grupo principal
const goBackToMain = () => {
  currentGroup.value = 'main';
};

// Resto de funciones
const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};

const redirectToModule = (path) => {
  if (isAuthenticated.value) {
    router.push(path);
  } else {
    localStorage.setItem('redirectAfterLogin', path);
    router.push('/login');
  }
};

const goToDashboard = () => {
  router.push('/dashboard');
};

// Efecto de aparición progresiva para las tarjetas
onMounted(() => {
  const cards = document.querySelectorAll('.elegant-group-card, .elegant-module-card');
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`;
  });
});
// Variables para el reproductor
const audioPlayer = ref(null);
const isPlaying = ref(false);
const currentTrack = ref('');
const trackHistory = ref([]);
const showMusicPanel = ref(false); // Controla la visibilidad del panel
const volume = ref(0.2); // Volumen por defecto

// Lista de pistas
const tracks = ref([
  new URL('/src/assets/playlist/song1.ogg', import.meta.url).href,
  new URL('/src/assets/playlist/song2.ogg', import.meta.url).href,
  new URL('/src/assets/playlist/song3.ogg', import.meta.url).href,
  new URL('/src/assets/playlist/song4.ogg', import.meta.url).href,
  new URL('/src/assets/playlist/song5.ogg', import.meta.url).href,
]);

// Función para mostrar/ocultar el panel de música
const toggleMusicPanel = () => {
  showMusicPanel.value = !showMusicPanel.value;
};

// Función para verificar si una URL de audio es válida
const checkAudioSource = async (url) => {
  try {
    const response = await fetch(url, { method: 'HEAD' });
    return response.ok;
  } catch (error) {
    console.error(`Error verificando ${url}:`, error);
    return false;
  }
};

// Obtener pista aleatoria
const getRandomTrack = () => {
  if (tracks.value.length === 0) return null;
  if (trackHistory.value.length >= tracks.value.length) trackHistory.value = [];

  const availableTracks = tracks.value.filter(track => !trackHistory.value.includes(track));
  if (availableTracks.length === 0) return null;

  const randomIndex = Math.floor(Math.random() * availableTracks.length);
  return availableTracks[randomIndex];
};

// Reproducir siguiente pista
const playNextTrack = async () => {
  const track = getRandomTrack();
  if (!track) return;

  const isValidSource = await checkAudioSource(track);
  if (!isValidSource) {
    console.error(`La fuente de audio no existe: ${track}`);
    setTimeout(playNextTrack, 1000);
    return;
  }

  trackHistory.value.push(track);

  if (audioPlayer.value) {
    currentTrack.value = track;
    audioPlayer.value.src = track;
    try {
      await audioPlayer.value.play();
      isPlaying.value = true;
    } catch (error) {
      console.error("Error al reproducir audio:", error);
      isPlaying.value = false;
      setTimeout(playNextTrack, 1000);
    }
  }
};

// Toggle reproducción manual
const togglePlayback = () => {
  if (!audioPlayer.value) return;

  if (isPlaying.value) {
    audioPlayer.value.pause();
    isPlaying.value = false;
  } else {
    audioPlayer.value.play()
      .then(() => { isPlaying.value = true; })
      .catch(error => { console.error("Error al reanudar audio:", error); });
  }
};

// Ajustar volumen
const adjustVolume = (newVolume) => {
  volume.value = parseFloat(newVolume);
  if (audioPlayer.value) audioPlayer.value.volume = volume.value;
};

// Inicializar reproductor
onMounted(() => {
  audioPlayer.value = new Audio();
  audioPlayer.value.volume = volume.value;
  audioPlayer.value.muted = true; // autoplay permitido
  audioPlayer.value.addEventListener('ended', playNextTrack);

  // Iniciar reproducción automática (silenciosa)
  playNextTrack();

  // Activar música en la primera interacción
  const enableAudio = () => {
    if (audioPlayer.value && audioPlayer.value.muted) {
      audioPlayer.value.muted = false;
    }
    // remover listeners después de la primera interacción
    document.removeEventListener('click', enableAudio);
    document.removeEventListener('scroll', enableAudio);
    document.removeEventListener('touchstart', enableAudio);
    document.removeEventListener('wheel', enableAudio);
  };

  // Agregar listeners
  document.addEventListener('click', enableAudio);
  document.addEventListener('scroll', enableAudio);
  document.addEventListener('touchstart', enableAudio);
  document.addEventListener('wheel', enableAudio);
});

// Limpiar al desmontar
onUnmounted(() => {
  if (audioPlayer.value) {
    audioPlayer.value.pause();
    audioPlayer.value.removeEventListener('ended', playNextTrack);
  }
});
</script>

<style scoped>
/* Estilos generales */
.modern-container {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  padding: 0;
  backdrop-filter: blur(1px);
}

.navbar-spacer {
  height: 76px;
}

/* Efecto mejorado - Expandir desde el centro */
.header-title {
  position: relative;
  padding-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.header-title h1 {
  background: linear-gradient(90deg, #53beef 2%, #0a58ca);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 3px;
  background: linear-gradient(90deg,
      transparent 0%,
      #53beef 30%,
      #0a58ca 70%,
      transparent 100%);
  transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
  transform: translateX(-50%);
  border-radius: 2px;
}

.header-title:hover::after {
  width: 100%;
}

.header-title:hover {
  transform: translateY(-2px);
  text-shadow: 0 2px 12px rgba(13, 110, 253, 0.15);
}

.header-subtitle {
  display: inline-block;
  padding-bottom: 0.3rem;
  position: relative;
  transition: all 0.3s ease;
}

.header-subtitle::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg,
      transparent 0%,
      #6c757d 30%,
      #495057 70%,
      transparent 100%);
  transition: all 0.4s ease;
  transform: translateX(-50%);
}

.header-subtitle:hover::after {
  width: 50%;
}

.main-content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* Navbar styles */
.navbar-modern {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  padding: 0.5rem 0;
}

.navbar-brand-modern {
  font-weight: 700;
  color: var(--bs-primary) !important;
  font-size: 1.5rem;
}

.navbar-modern .nav-link {
  font-weight: 500;
  color: #495057 !important;
  transition: all 0.3s ease;
  position: relative;
}

.navbar-modern .nav-link:hover {
  color: var(--bs-primary) !important;
}

.navbar-modern .nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: var(--bs-primary);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.navbar-modern .nav-link:hover::after {
  width: 80%;
}


/* Alert moderno */
.alert-modern {
  font-size: 0.9rem;
  border: none;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  padding: 1rem 1.5rem;
  align-items: center;
  display: flex;
  margin: 0 auto 30px auto;
  width: 60%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  opacity: 0.7;
  text-align: center;
}

.alert-modern:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 36px rgba(31, 38, 135, 0.15);
}

.alert-icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bs-primary);
  color: white;
}

/* Section title */
.section-title {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 2rem;
}



/* Estilos para tarjetas de grupos */
.elegant-group-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
  position: relative;
  overflow: hidden;
}

.elegant-group-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--icon-color), transparent);
  opacity: 0.7;
}

.elegant-group-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 36px rgba(31, 38, 135, 0.2);
}

.elegant-group-card:hover .elegant-icon-container {
  transform: scale(1.1) translateY(-5px);
}

.elegant-group-card:hover .elegant-hover-indicator {
  opacity: 1;
  transform: translateX(5px);
}

.elegant-icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 70px;
  border-radius: 18px;
  background: linear-gradient(135deg, var(--icon-color) 0%, var(--icon-color) 100%);
  color: white;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.elegant-icon {
  font-size: 1.8rem;
}

.elegant-title {
  color: #2c3e50;
  font-weight: 600;
}

.elegant-module-count {
  margin-top: auto;
}

.elegant-hover-indicator {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  opacity: 0;
  transition: all 0.3s ease;
  color: var(--bs-primary);
}

/* Estilos para tarjetas de módulos individuales */
.elegant-module-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  transition: all 0.3s ease;
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.elegant-module-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--icon-color), transparent);
  opacity: 0.7;
}

.elegant-module-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 36px rgba(31, 38, 135, 0.2);
}

.elegant-module-card:hover .elegant-icon-container {
  transform: scale(1.1);
}

.elegant-module-card:hover .elegant-card-decoration {
  opacity: 1;
}

.module-enabled {
  cursor: pointer;
}

.module-disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.module-disabled:hover {
  transform: none !important;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1) !important;
}

.coming-soon-badge {
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 10;
  /* Añadir esta línea */
  position: relative;
  /* Añadir esta línea si no está ya */
}

.coming-soon-badge {
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 10;
  position: relative;
}

/* Animación para el icono de reloj */
.coming-soon-badge i {
  animation: spin-clockwise 2s infinite linear;
  display: inline-block;
}

@keyframes spin-clockwise {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.elegant-action-btn {
  margin-top: auto;
}

.elegant-card-decoration {
  position: absolute;
  bottom: -20px;
  right: -20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--icon-color) 0%, transparent 70%);
  opacity: 0.1;
  transition: opacity 0.3s ease;
}

/* Breadcrumb para navegación entre grupos */
.module-breadcrumb {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(10px);
}

/* Benefit cards */
.benefit-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  transition: all 0.3s ease;
}

.benefit-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 36px rgba(31, 38, 135, 0.15);
}

.benefit-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: linear-gradient(135deg, var(--bs-primary) 0%, #0a58ca 100%);
  color: white;
  font-size: 1.5rem;
}

/* Feature section */
.feature-item {
  padding: 1rem;
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: rgba(13, 110, 253, 0.1);
  color: var(--bs-primary);
  font-size: 1.2rem;
  flex-shrink: 0;
}

.feature-visual {
  background: linear-gradient(135deg, rgba(13, 110, 253, 0.1) 0%, rgba(13, 110, 253, 0.05) 100%);
  border: 1px solid rgba(13, 110, 253, 0.1);
}

.feature-visual i {
  font-size: 4rem;
  color: var(--bs-primary);
}

/* About section */
.about-section {
  padding: 2rem 0;
}

.contact-section {
  padding: 2rem 0;
}

.contact-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
}

.contact-icon {
  font-size: 3rem;
  color: var(--bs-primary);
}

/* Footer moderno */
.footer-modern {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(1px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.05);
}

.tech-badge-modern {
  padding: 0.4rem 0.8rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  font-size: 0.75rem;
  color: #2c3e50;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  transition: all 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.tech-badge-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.tech-icon {
  width: 16px;
  height: 16px;
  object-fit: contain;
  margin-right: 6px;
}

/* Animaciones */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .modern-container {
    padding: 0;
  }

  .navbar-spacer {
    height: 66px;
  }

  .header-section h1 {
    font-size: 1.8rem;
  }

  .section-title {
    flex-direction: column;
  }

  .title-decoration {
    margin: 10px 0;
    width: 80px;
  }

  .alert-modern {
    width: 90%;
    flex-direction: column;
    text-align: center;
  }

  .elegant-group-card,
  .elegant-module-card {
    margin-bottom: 1.5rem;
  }

  .navbar-brand-modern {
    font-size: 1.2rem;
  }
}

.navbar-logo {
  height: 32px;
  width: auto;
  object-fit: contain;
}

.btn-back-elegant {
  background: linear-gradient(135deg, #6f42c1 0%, #8c68cd 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.5rem 1.2rem;
  font-size: 0.875rem;
  font-weight: 500;
  margin-right: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(111, 66, 193, 0.25);
  position: relative;
  overflow: hidden;
}

.btn-back-elegant::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.7s ease;
}

.btn-back-elegant:hover::before {
  left: 100%;
}

.btn-back-elegant:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(111, 66, 193, 0.4);
  background: linear-gradient(135deg, #8c68cd 0%, #6f42c1 100%);
  color: white;

}

.btn-back-elegant:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(111, 66, 193, 0.3);
}

.btn-back-elegant i {
  transition: transform 0.3s ease;
}

.btn-back-elegant:hover i {
  transform: translateX(-3px);
}

/* Estilos para el panel de música flotante */
.music-floating-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 40px;
  height: 40px;
  background: #54bef0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  z-index: 1000;
  transition: all 0.3s ease;
}

.music-floating-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
}

.music-floating-btn i {
  color: white;
  font-size: 1.1rem;
}

.music-player-panel {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 300px;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  transition: all 0.3s ease;
  border: 1px solid #eaeaea;
}

.volume-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.volume-slider {
  flex: 1;
}

.status-indicator {
  font-size: 0.85rem;
  flex-grow: 1;
  margin: 0 10px;
}

.btn-outline-primary {
  border-width: 2px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>