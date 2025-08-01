<template>
  <div class="container-fluid mt-4">
    <!-- Modal para crear/editar usuario -->
    <ModalBase :visible="showUserModal" :mode="editing ? 'edit' : 'create'" entityName="usuario"
      :confirm-text="isSubmitting ? 'Guardando...' : 'Guardar'" :loading="isSubmitting" @close="closeUserModal"
      @confirm="handleSubmit">
      <template #content>
        <form @submit.prevent="handleSubmit">
          <div class="row">
            <div class="col-md-6">
              <!-- Username -->
              <FloatInput id="username" label="Nombre de usuario" v-model="form.username" icon="pi pi-user-edit"
                :errors="errors" :invalid="!!errors.username" />

              <!-- Email -->
              <FloatInput id="email" label="Email" v-model="form.email" type="email" icon="pi pi-envelope"
                :invalid="!!errors.email" :errors="errors" />

              <!-- Contraseña (solo creación) -->
              <template v-if="!editing">
                <FloatInput id="password" label="Contraseña" v-model="form.password" type="password" icon="pi pi-lock"
                  :invalid="!!errors.password" :errors="errors" />
                <FloatInput id="password2" label="Confirmar Contraseña" v-model="form.password2" type="password"
                  icon="pi pi-lock-open" :invalid="!!errors.password2" :errors="errors" />
              </template>

              <!-- Reset password (edición) -->
              <div v-if="editing" class="mb-3">
                <div class="alert alert-info">
                  <div class="form-check form-switch">
                    <input v-model="resetPassword" class="form-check-input" type="checkbox" id="resetPasswordCheck">
                    <label class="form-check-label" for="resetPasswordCheck">
                      <i class="pi pi-key me-2"></i>
                      <strong>Resetear contraseña</strong>
                    </label>
                  </div>
                  <small class="text-muted">
                    <i class="pi pi-info-circle me-1"></i>
                    Marque esta opción si desea establecer una nueva contraseña
                  </small>
                </div>

                <div v-if="resetPassword" class="mt-3">
                  <FloatInput id="new_password" label="Nueva Contraseña" v-model="form.password" type="password"
                    icon="pi pi-key" :invalid="!!errors.password" :errors="errors" />
                  <FloatInput id="confirm_new_password" label="Confirmar Nueva Contraseña" v-model="form.password2"
                    type="password" icon="pi pi-key" :invalid="!!errors.password2" :errors="errors" />
                </div>
              </div>
            </div>

            <div class="col-md-6">
              <!-- Nombres -->
              <FloatInput id="first_name" label="Nombres" v-model="form.first_name" icon="pi pi-user"
                :invalid="!!errors.first_name" :errors="errors" />

              <!-- Apellidos -->
              <FloatInput id="last_name" label="Apellidos" v-model="form.last_name" icon="pi pi-users"
                :invalid="!!errors.last_name" :errors="errors" />

              <!-- DNI -->
              <FloatInput id="dni" label="DNI" v-model="form.dni" icon="pi pi-id-card" maxlength="8"
                :invalid="!!errors.dni" :errors="errors" placeholder="Ingrese 8 dígitos" />

              <!-- Celular -->
              <FloatInput id="celular" label="Celular" v-model="form.celular" icon="pi pi-phone" maxlength="9"
                :invalid="!!errors.celular" :errors="errors" placeholder="Ingrese 9 dígitos" />
            </div>
          </div>

          <div class="row">
            <div class="col-md-4">
              <div class="form-check form-switch mb-3">
                <input v-model="form.is_active" class="form-check-input" type="checkbox" id="isActiveCheck">
                <label class="form-check-label" for="isActiveCheck">Activo</label>
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-check form-switch mb-3">
                <input v-model="form.is_staff" class="form-check-input" type="checkbox" id="isStaffCheck">
                <label class="form-check-label" for="isStaffCheck">Staff</label>
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-check form-switch mb-3">
                <input v-model="form.is_superuser" class="form-check-input" type="checkbox" id="isSuperuserCheck">
                <label class="form-check-label" for="isSuperuserCheck">Superusuario</label>
              </div>
            </div>
          </div>
        </form>
      </template>
    </ModalBase>

    <!-- Modal de confirmación para eliminar -->
    <ModalBase :visible="showDeleteModal" mode="delete" entityName="usuario" confirm-text="Eliminar Permanentemente"
      confirm-class="p-button-danger" :loading="isDeleting" @close="closeDeleteModal" @confirm="proceedDelete">
      <template #content>
        ¿Estás seguro de eliminar permanentemente al usuario <strong>{{ userToDelete?.username }}</strong>?
        <div class="alert alert-warning mt-3">
          <i class="fas fa-exclamation-triangle me-2"></i>
          Esta acción no se puede deshacer y eliminará todos los datos asociados al usuario.
        </div>
      </template>
    </ModalBase>

    <!-- Listado de usuarios -->
    <DataTableWrapper :data="userStore.users" :columns="columns" :loading="userStore.loading" :actions="true">
      <template #header>
        <div class="flex justify-content-between align-items-center">
          <h2 class="m-0">Gestión de Usuarios</h2>
          <Button icon="pi pi-plus" label="Nuevo Usuario" @click="openCreateModal" class="p-button-sm" />
        </div>
      </template>

      <template #body-full_name="{ data }"> <!-- Cambiado de body-fullName -->
        {{ data.full_name || '-' }}
      </template>

      <template #body-is_active="{ data }">
        <div class="d-flex flex-column align-items-center">
          <ToggleSwitch v-model="data.is_active" @change="userStore.toggleUserStatus(data.id, data.is_active)"
            class="mb-1" />
          <span class="badge custom-badge" :class="data.is_active ? 'bg-success' : 'bg-danger'">
            {{ data.is_active ? 'Activo' : 'Inactivo' }}
          </span>
        </div>
      </template>

      <template #body-is_staff="{ data }">
        <div class="d-flex flex-column align-items-center">
          <ToggleSwitch v-model="data.is_staff" @change="userStore.toggleStaffStatus(data.id, data.is_staff)"
            class="mb-1" />
          <span class="badge custom-badge" :class="data.is_staff ? 'bg-info' : 'bg-secondary'">
            {{ data.is_staff ? 'Staff' : 'Normal' }}
          </span>
        </div>
      </template>

      <template #body-roles="{ data }">
        <div class="d-flex gap-2">
          <span v-if="data.is_superuser" class="badge bg-danger" v-tooltip.top="'Usuario con todos los permisos'">
            <i class="fas fa-crown me-1"></i>
            SuperUser
          </span>
          <span v-if="data.is_staff" class="badge bg-info text-dark" v-tooltip.top="'Usuario con permisos de staff'">
            <i class="fas fa-user-tie me-1"></i>
            Staff
          </span>
          <span v-if="!data.is_superuser && !data.is_staff" class="badge bg-secondary" v-tooltip.top="'Usuario normal'">
            <i class="fas fa-user me-1"></i>
            Usuario
          </span>
        </div>
      </template>

      <template #body-created_by="{ data }">
        {{ data.created_by ? data.created_by.username : 'Sistema' }}
      </template>

      <template #actions="{ data }">
        <Button icon="pi pi-pencil" class="p-button-warning p-button-sm mr-2" @click="openEditModal(data)" />
        <Button icon="pi pi-trash" class="p-button-danger p-button-sm" @click="confirmDelete(data)" />
      </template>
    </DataTableWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { toast } from 'vue-sonner';
import DataTableWrapper from '@/components/ui/DataTableWrapper.vue';
import Button from 'primevue/button';
import { useUserStore } from '@/store/gore/userStore';
import ToggleSwitch from 'primevue/toggleswitch';
import ModalBase from '@/components/ui/ModalBase.vue';
import FloatInput from '@/components/widgets/FloatInput.vue';

const userStore = useUserStore();
const errors = ref({});

// Definimos la estructura del formulario como constante
const FORM_STATE = {
  username: '',
  email: '',
  password: '',
  password2: '',
  first_name: '',
  last_name: '',
  full_name: '',
  dni: '',
  celular: '',
  is_active: true,
  is_staff: false,
  is_superuser: false
};

const showUserModal = ref(false);
const showDeleteModal = ref(false);
const editing = ref(false);
const isSubmitting = ref(false);
const resetPassword = ref(false);
const userToDelete = ref(null);
const userToEdit = ref(null);
const isDeleting = ref(false);

// Usamos la estructura para el formulario reactivo
const form = ref({ ...FORM_STATE });

// Configuración de columnas para la tabla
const columns = ref([
  { field: 'username', header: 'Usuario', sortable: true },
  { field: 'full_name', header: 'Nombre', sortable: true, bodyTemplate: true },
  { field: 'email', header: 'Email', sortable: true },
  { field: 'is_active', header: 'Estado', sortable: true, bodyTemplate: true },
  { field: 'is_staff', header: 'Staff', sortable: true, bodyTemplate: true },
  { field: 'roles', header: 'Roles', bodyTemplate: true },
  { field: 'created_by', header: 'Creado por', bodyTemplate: true }
]);

// Métodos
const openCreateModal = () => {
  resetForm();
  editing.value = false;
  showUserModal.value = true;
};

const openEditModal = (user) => {
  editing.value = true;
  resetPassword.value = false;
  userToEdit.value = user;

  // Copia los datos del usuario al formulario
  form.value = {
    ...FORM_STATE, // Valores por defecto
    ...user,      // Sobreescribe con los datos del usuario
    password: '',  // Resetear contraseñas
    password2: ''
  };

  showUserModal.value = true;
};

const resetForm = () => {
  form.value = { ...FORM_STATE };
  resetPassword.value = false;
  errors.value = {};
};

const closeUserModal = () => {
  showUserModal.value = false;
  resetForm();
};

const confirmDelete = (user) => {
  userToDelete.value = user;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  try {
    showDeleteModal.value = false;
    // Pequeño delay para la animación antes de resetear
    setTimeout(() => {
      userToDelete.value = null;
    }, 300);
  } catch (error) {
    console.error("Error al cerrar modal:", error);
  }
};

const proceedDelete = async () => {
  isDeleting.value = true;
  try {
    const success = await userStore.deleteUser(userToDelete.value.id);
    if (success) {
      closeDeleteModal();
    }
  } catch (error) {
  } finally {
    isDeleting.value = false;
  }
};

const handleSubmit = async () => {
  if ((!editing.value || resetPassword.value) && form.value.password !== form.value.password2) {
    toast.error('Las contraseñas no coinciden');
    return;
  }

  isSubmitting.value = true;
  errors.value = {}; // Limpiar errores anteriores

  try {
    const { password2, ...userData } = form.value;

    if (editing.value && !resetPassword.value) {
      delete userData.password;
    }

    if (editing.value) {
      await userStore.updateUser(userToEdit.value.id, userData);
    } else {
      await userStore.createUser(userData);
    }

    closeUserModal();
  } catch (error) {
    if (error.response?.data) {
      // Asignar errores al objeto errors para mostrarlos en los campos
      errors.value = error.response.data;

      // Mostrar errores generales en toast solo si no son errores de campo específicos
      if (error.response.data.non_field_errors) {
        toast.error(error.response.data.non_field_errors.join(', '));
      }
    } else {
      toast.error('Error al guardar: ' + error.message);
    }
  } finally {
    isSubmitting.value = false;
  }
};

// Inicialización
onMounted(async () => {
  try {
    userStore.loading = true;
    await userStore.listUsers();
  } catch (error) {
  } finally {
    userStore.loading = false;
  }
});
</script>

<style scoped></style>