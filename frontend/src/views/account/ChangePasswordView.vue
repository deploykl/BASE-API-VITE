<template>
  <div class="change-password-container">
    <div class="card">
      <div class="card-header">
        <h3>Cambiar Contraseña</h3>
      </div>
      <div class="card-body">
        <form @submit.prevent="changePassword">
          <div class="mb-3">
            <label class="form-label">Contraseña Actual</label>
            <div class="input-group">
              <input 
                :type="showCurrentPassword ? 'text' : 'password'" 
                class="form-control" 
                v-model="passwords.current_password" 
                :class="{ 'is-invalid': errors.current_password }"
                required
              >
              <button 
                class="btn btn-outline-secondary" 
                type="button" 
                @click="showCurrentPassword = !showCurrentPassword"
              >
                <i :class="showCurrentPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
              </button>
            </div>
            <div v-if="errors.current_password" class="invalid-feedback d-block">
              {{ errors.current_password }}
            </div>
          </div>
          
          <div class="mb-3">
            <label class="form-label">Nueva Contraseña</label>
            <div class="input-group">
              <input 
                :type="showNewPassword ? 'text' : 'password'" 
                class="form-control" 
                v-model="passwords.new_password" 
                :class="{ 'is-invalid': errors.new_password }"
                required
              >
              <button 
                class="btn btn-outline-secondary" 
                type="button" 
                @click="showNewPassword = !showNewPassword"
              >
                <i :class="showNewPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
              </button>
            </div>
            <small class="form-text text-muted">Mínimo 8 caracteres</small>
            <div v-if="errors.new_password" class="invalid-feedback d-block">
              {{ errors.new_password }}
            </div>
          </div>
          
          <div class="mb-3">
            <label class="form-label">Confirmar Nueva Contraseña</label>
            <div class="input-group">
              <input 
                :type="showConfirmPassword ? 'text' : 'password'" 
                class="form-control" 
                v-model="passwords.confirm_password" 
                :class="{ 'is-invalid': errors.confirm_password }"
                required
              >
              <button 
                class="btn btn-outline-secondary" 
                type="button" 
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
              </button>
            </div>
            <div v-if="errors.confirm_password" class="invalid-feedback d-block">
              {{ errors.confirm_password }}
            </div>
          </div>
          
          <div class="d-flex justify-content-between mt-4">
            <router-link to="/perfil" class="btn btn-outline-secondary">
              Volver al Perfil
            </router-link>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm"></span>
              Cambiar Contraseña
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/components/services/Axios'
import { toast } from 'vue-sonner'

const router = useRouter()

const passwords = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const errors = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const loading = ref(false)
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const resetErrors = () => {
  errors.value = {
    current_password: '',
    new_password: '',
    confirm_password: ''
  }
}

const changePassword = async () => {
  resetErrors()
  let hasErrors = false

  // Validación de frontend
  if (!passwords.value.current_password) {
    errors.value.current_password = 'La contraseña actual es requerida'
    hasErrors = true
  }

  if (passwords.value.new_password.length < 8) {
    errors.value.new_password = 'La contraseña debe tener al menos 8 caracteres'
    hasErrors = true
  }

  if (passwords.value.new_password !== passwords.value.confirm_password) {
    errors.value.confirm_password = 'Las contraseñas no coinciden'
    hasErrors = true
  }

  if (passwords.value.new_password === passwords.value.current_password) {
    errors.value.new_password = 'La nueva contraseña no puede ser igual a la actual'
    hasErrors = true
  }

  if (hasErrors) {
    return
  }

  loading.value = true

  try {
    const response = await api.post('user/change-password/', {
      current_password: passwords.value.current_password,
      new_password: passwords.value.new_password,
      confirm_password: passwords.value.confirm_password
    })

    toast.success('Contraseña cambiada exitosamente')
    
    // Limpiar formulario
    passwords.value = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
    
    // Redirigir al perfil
    router.push('/perfil')
    
  } catch (err) {
    console.error('Error al cambiar contraseña:', err)
    
    // Manejo de errores del backend
    if (err.response?.data) {
      // Asignar errores a los campos correspondientes
      for (const [field, messages] of Object.entries(err.response.data)) {
        if (errors.value.hasOwnProperty(field)) {
          errors.value[field] = Array.isArray(messages) ? messages[0] : messages
        } else {
          toast.error(Array.isArray(messages) ? messages[0] : messages)
        }
      }
    } else {
      toast.error('Error al cambiar la contraseña')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.change-password-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.card {
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-header {
  background: linear-gradient(135deg, #364257 0%, #2b3548 100%);
  padding: 1.5rem 2rem;
  color: white;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.card-header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  transform: rotate(30deg);
}

.card-body {
  padding: 2rem;
}

.form-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.input-group button {
  border-radius: 0 0.375rem 0.375rem 0;
}
</style>