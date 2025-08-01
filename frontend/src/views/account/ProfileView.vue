<template>
  <div class="container">
    <div class="profile-card">
      <div class="profile-header">
        <h2 class="profile-title">Editar Perfil</h2>
        <p class="profile-subtitle">Actualiza tu información personal</p>
      </div>

      <div class="profile-content">
        <form @submit.prevent="updateProfile" class="profile-form">
          <div class="avatar-section">
            <div class="avatar-wrapper" @click="openImageModal(userImage)">
              <img :src="userImage" alt="Foto de perfil" class="avatar-image" @error="userStore.setImageError(true)">
              <div class="avatar-overlay">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path
                    d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z">
                  </path>
                </svg>
              </div>
            </div>

            <div class="avatar-actions">
              <input type="file" ref="fileInput" @change="handleImageChange" accept="image/*" class="d-none">
              <button type="button" @click="$refs.fileInput.click()" class="btn-change-image">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7"></path>
                  <line x1="16" y1="5" x2="22" y2="5"></line>
                  <line x1="19" y1="2" x2="19" y2="8"></line>
                  <circle cx="9" cy="9" r="2"></circle>
                  <path d="M21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
                </svg>
                Cambiar imagen
              </button>

              <div v-if="selectedImage" class="image-selected-notice">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                Nueva imagen seleccionada
              </div>
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 col-lg-4 mb-3">
              <!-- Tu contenido para la primera columna -->
              <FloatInput id="username" label="Nombre de usuario" v-model="userStore.userData.username"
                icon="fas fa-user" required />
            </div>

            <div class="col-md-6 col-lg-4 mb-3">
              <!-- Tu contenido para la segunda columna -->
              <FloatInput id="firstname" label="Nombres" v-model="userStore.userData.first_name" icon="fas fa-signature"
                required />
            </div>

            <div class="col-md-6 col-lg-4 mb-3">
              <!-- Tu contenido para la tercera columna -->
              <FloatInput id="lastname" label="Apellidos" v-model="userStore.userData.last_name" icon="fas fa-users" />
            </div>

            <div class="col-md-6 col-lg-4 mb-3">
              <FloatInput id="dni" label="DNI" v-model="userStore.userData.dni" icon="fas fa-id-card" validationType="dni" maxlength="8"
                />
            </div>

            <div class="col-md-6 col-lg-4 mb-3">
              <FloatInput id="phone" label="N° Celular" v-model="userStore.userData.celular" icon="fas fa-mobile-alt" validationType="phone" maxlength="9"/>
            </div>

            <div class="col-md-6 col-lg-4 mb-3">
              <FloatInput id="email" label="Correo electrónico" v-model="userStore.userData.email"
                icon="fas fa-envelope" type="email" />
            </div>
          </div>
          <div class="form-actions">
            <router-link to="/change-password" class="btn-secondary">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"></circle>
                <path
                  d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z">
                </path>
              </svg>
              Cambiar Contraseña
            </router-link>

            <button type="submit" class="btn-primary" :disabled="userStore.loading">
              <span v-if="userStore.loading" class="spinner"></span>
              <span v-else>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                  <polyline points="17 21 17 13 7 13 7 21"></polyline>
                  <polyline points="7 3 7 8 15 8"></polyline>
                </svg>
              </span>
              Guardar Cambios
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal para imagen en tamaño completo -->
    <div v-if="showImageModal" class="image-modal" @click.self="closeImageModal">
      <div class="modal-content">
        <button class="close-btn" @click="closeImageModal">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <img :src="modalImageSrc" alt="Imagen de perfil ampliada" class="full-size-image">
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/store/user'
import { toast } from 'vue-sonner'
import FloatInput from '@/components/widgets/FloatInput.vue';


const userStore = useUserStore()
const fileInput = ref(null)
const selectedImage = ref(null)
const imagePreview = ref(null)
const showImageModal = ref(false)
const modalImageSrc = ref('')

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
    toast.error('Por favor selecciona un archivo de imagen válido');
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
      toast.error('Error al procesar la imagen');
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
.container {
  max-width: 800px;
  padding: 0 1.5rem;
}

.profile-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
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

.profile-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  position: relative;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.profile-subtitle {
  font-size: 0.95rem;
  opacity: 0.9;
  margin-bottom: 0;
  position: relative;
}


.profile-content {
  padding: 2rem;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}

.input-wrapper i.fas {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #364257;
  opacity: 0.7;
  font-size: 1rem;
}

/* Avatar mejorado */
.avatar-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  cursor: pointer;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
  border: 4px solid white;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(0, 0, 0, 0.05);
}

.avatar-wrapper:hover {
  transform: scale(1.05);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  border: 4px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.avatar-overlay svg {
  color: white;
  width: 30px;
  height: 30px;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.btn-change-image {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f5f7ff;
  color: #5a67d8;
  border: none;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-change-image:hover {
  background: #e0e7ff;
  transform: translateY(-1px);
}

.btn-change-image svg {
  width: 14px;
  height: 14px;
}

.image-selected-notice {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  margin-left: 1rem;
  font-size: 0.8rem;
  color: #48bb78;
}

.image-selected-notice svg {
  width: 14px;
  height: 14px;
}


.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: #364257;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background-color: #f8fafc;
}

.form-input:focus {
  outline: none;
  border-color: #364257;
  box-shadow: 0 0 0 3px rgba(167, 119, 227, 0.2);
  background-color: white;
}

.input-wrapper svg {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #a777e3;
  opacity: 0.7;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #edf2f7;
}

.btn-primary,
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #364257;
  color: white;
  border: none;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(106, 123, 251, 0.3);
}

.btn-primary:disabled {
  background: #cbd5e0;
  transform: none;
  box-shadow: none;
  cursor: not-allowed;
}

.btn-secondary {
  background: white;
  color: #6e8efb;
  border: 1px solid #e2e8f0;
}

.btn-secondary:hover {
  background: #f5f7ff;
  transform: translateY(-2px);
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Modal styles */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  backdrop-filter: blur(5px);
}

.modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
}

.full-size-image {
  max-width: 100%;
  max-height: 40vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.close-btn {
  position: absolute;
  top: -50px;
  right: 0;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.close-btn:hover {
  opacity: 1;
}

.close-btn svg {
  width: 24px;
  height: 24px;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 0 1rem;
  }

  .profile-header {
    padding: 1.5rem 1rem;
  }

  .profile-content {
    padding: 1.5rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column-reverse;
    gap: 1rem;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }

  .avatar-wrapper {
    width: 100px;
    height: 100px;
  }
}
</style>