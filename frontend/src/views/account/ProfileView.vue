<template>
  <div class="container py-4">
    <div class="card shadow-sm">
      <div class="profile-header text-center">
        <h2>Editar Perfil</h2>
        <p class="mb-0">Actualiza tu información personal</p>
      </div>

      <div class="card-body">
        <form @submit.prevent="updateProfile">
          <div class="text-center mb-4">
            <div class="position-relative d-inline-block" @click="openImageModal(userImage)" style="cursor:pointer">
              <img :src="userImage" class="rounded-circle border border-white shadow" width="120" height="120" style="object-fit: cover" @error="userStore.setImageError(true)" />
              <div class="position-absolute top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center bg-dark bg-opacity-50 rounded-circle opacity-0 hover-opacity-100">
                <i class="pi pi-cog text-white fs-4"></i>
              </div>
            </div>
            <div class="mt-2">
              <input type="file" ref="fileInput" @change="handleImageChange" accept="image/*" hidden>
              <button type="button" class="btn btn-outline-primary btn-sm" @click="$refs.fileInput.click()">
                <i class="pi pi-image me-1"></i>Cambiar imagen
              </button>
              <div v-if="selectedImage" class="text-success small mt-1">
                <i class="pi pi-check-circle me-1"></i>Nueva imagen seleccionada
              </div>
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 col-lg-4 mb-3">
              <FloatInput id="username" label="Nombre de usuario" v-model="userStore.userData.username" icon="fas fa-user" required />
            </div>
            <div class="col-md-6 col-lg-4 mb-3">
              <FloatInput id="firstname" label="Nombres" v-model="userStore.userData.first_name" icon="fas fa-signature" required />
            </div>
            <div class="col-md-6 col-lg-4 mb-3">
              <FloatInput id="lastname" label="Apellidos" v-model="userStore.userData.last_name" icon="fas fa-users" />
            </div>
            <div class="col-md-6 col-lg-4 mb-3">
              <FloatInput id="dni" label="DNI" v-model="userStore.userData.dni" icon="fas fa-id-card" validationType="dni" maxlength="8" />
            </div>
            <div class="col-md-6 col-lg-4 mb-3">
              <FloatInput id="phone" label="N° Celular" v-model="userStore.userData.celular" icon="fas fa-mobile-alt" validationType="phone" maxlength="9" />
            </div>
            <div class="col-md-6 col-lg-4 mb-3">
              <FloatInput id="email" label="Correo electrónico" v-model="userStore.userData.email" icon="fas fa-envelope" type="email" />
            </div>
          </div>

          <div class="d-flex justify-content-between border-top pt-3">
            <router-link to="/change-password" class="btn btn-outline-secondary">
              <i class="pi pi-key me-1"></i>Cambiar Contraseña
            </router-link>
            <button type="submit" class="btn btn-primary" :disabled="userStore.loading">
              <span v-if="userStore.loading" class="spinner-border spinner-border-sm"></span>
              <span v-else>
                <i class="pi pi-save me-1"></i>Guardar
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal para imagen en tamaño completo -->
    <div v-if="showImageModal" class="modal fade show d-block bg-dark bg-opacity-90" tabindex="-1" @click.self="closeImageModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 bg-transparent">
          <button class="btn btn-link position-absolute top-0 end-0 p-2 text-white opacity-75 hover-opacity-100" @click="closeImageModal">
            <i class="pi pi-times fs-5"></i>
          </button>
          <img :src="modalImageSrc" alt="Imagen de perfil ampliada" class="img-fluid rounded shadow-lg" style="max-height: 70vh;">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useCustomToast } from '@/components/utils/toast'
import FloatInput from '@/components/widgets/FloatInput.vue';

const userStore = useUserStore()
const fileInput = ref(null)
const selectedImage = ref(null)
const imagePreview = ref(null)
const showImageModal = ref(false)
const modalImageSrc = ref('')
const { showError, showSuccess } = useCustomToast()

// Obtener datos del perfil al cargar el componente
onMounted(async () => {
  await userStore.fetchUserProfile()
})

const userImage = computed(() => imagePreview.value || userStore.effectiveUserImage)

const openImageModal = (src) => {
  modalImageSrc.value = src
  showImageModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeImageModal = () => {
  showImageModal.value = false
  document.body.style.overflow = 'auto'
}

const handleImageChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  event.target.value = '';

  // Verificar tipo y tamaño
  if (!file.type.match('image.*')) {
    showError.error('Por favor selecciona un archivo de imagen válido');
    return;
  }

  // Comprimir imagen si es mayor a 1MB
  if (file.size > 1024 * 1024) {
    try {
      const compressedFile = await imageCompression(file, {
        maxSizeMB: 1,
        maxWidthOrHeight: 1920,
        useWebWorker: true
      });

      selectedImage.value = compressedFile;
      userStore.setImageError(false);

      // Vista previa
      const reader = new FileReader();
      reader.onload = (e) => imagePreview.value = e.target.result;
      reader.readAsDataURL(compressedFile);

    } catch (error) {
      console.error('Error al comprimir:', error);
      showError.error('Error al procesar la imagen');
    }
  } else {
    // Usar imagen original si es pequeña
    selectedImage.value = file;
    userStore.setImageError(false);

    // Vista previa
    const reader = new FileReader();
    reader.onload = (e) => imagePreview.value = e.target.result;
    reader.readAsDataURL(file);
  }
};

const updateProfile = async () => {
  const success = await userStore.updateUserProfile(selectedImage.value)
  if (success) {
    imagePreview.value = null
    selectedImage.value = null
  }
}
</script>

<style scoped>
/* Tus estilos existentes se mantienen igual */
.container {
  max-width: 800px;
  padding: 0 1.5rem;
}

.profile-header {
  background: linear-gradient(135deg, #364257 0%, #2b3548 100%);
  padding: 1.5rem 2rem;
  color: white;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.profile-header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  transform: rotate(30deg);
}


</style>