<template>
  <div class="container-fluid mt-2">

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
                :errors="errors" :invalid="!!errors.username" size="small" />

              <!-- Email -->
              <FloatInput id="email" label="Email" v-model="form.email" type="email" icon="pi pi-envelope"
                :invalid="!!errors.email" :errors="errors" size="small" />

              <!-- Contraseña (solo creación) -->
              <template v-if="!editing">
                <FloatInput id="password" label="Contraseña" v-model="form.password" type="password" icon="pi pi-lock"
                  :invalid="!!errors.password" :errors="errors" size="small" />
                <FloatInput id="password2" label="Confirmar Contraseña" v-model="form.password2" type="password"
                  icon="pi pi-lock-open" :invalid="!!errors.password2" :errors="errors" size="small" />
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
                    icon="pi pi-key" :invalid="!!errors.password" :errors="errors" size="small" />
                  <FloatInput id="confirm_new_password" label="Confirmar Nueva Contraseña" v-model="form.password2"
                    type="password" icon="pi pi-key" :invalid="!!errors.password2" :errors="errors" size="small" />
                </div>
              </div>
            </div>

            <div class="col-md-6">
              <!-- Nombres -->
              <FloatInput id="first_name" label="Nombres" v-model="form.first_name" icon="pi pi-user"
                :invalid="!!errors.first_name" :errors="errors" size="small" />

              <!-- Apellidos -->
              <FloatInput id="last_name" label="Apellidos" v-model="form.last_name" icon="pi pi-users"
                :invalid="!!errors.last_name" :errors="errors" size="small" />

              <!-- DNI -->
              <FloatInput id="dni" label="DNI" v-model="form.dni" icon="pi pi-id-card" maxlength="8"
                :invalid="!!errors.dni" :errors="errors" placeholder="Ingrese 8 dígitos" size="small" />

              <!-- Celular -->
              <FloatInput id="celular" label="Celular" v-model="form.celular" icon="pi pi-phone" maxlength="9"
                :invalid="!!errors.celular" :errors="errors" placeholder="Ingrese 9 dígitos" size="small" />
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
    <DataTableWrapper :data="userStore.users" :columns="columns" :loading="userStore.loading" :actions="true"
      :showCreateButton="true" title="GESTIÓN DE USUARIOS" createButtonLabel="Nuevo Usuario"
      createButtonIcon="pi pi-user-plus" :expandable="true" @create="openCreateModal">
      <!-- sortField="is_active" :sortOrder="-1" para poner estado activo -->

      <!-- Template para full_name -->
      <template #body-full_name="{ data }">
        {{ data.full_name || '-' }}
      </template>

      <!-- Template para is_active -->
      <template #body-is_active="{ data }">
        <div class="d-flex flex-column align-items-center">
          <ToggleSwitch v-model="data.is_active" @change="userStore.toggleUserStatus(data.id, data.is_active)"
            class="mb-1" />
          <span class="badge custom-badge" :class="data.is_active ? 'bg-success' : 'bg-danger'">
            {{ data.is_active ? 'Activo' : 'Inactivo' }}
          </span>
        </div>
      </template>

      <!-- Template para is_staff -->
      <template #body-is_staff="{ data }">
        <div class="d-flex flex-column align-items-center">
          <ToggleSwitch v-model="data.is_staff" @change="userStore.toggleStaffStatus(data.id, data.is_staff)"
            class="mb-1" />
          <span class="badge custom-badge" :class="data.is_staff ? 'bg-info' : 'bg-secondary'">
            {{ data.is_staff ? 'Staff' : 'Normal' }}
          </span>
        </div>
      </template>

      <!-- Template para roles -->
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

      <!-- Template para created_by -->
      <template #body-created_by="{ data }">
        {{ data.created_by ? data.created_by.username : 'Sistema' }}
      </template>


      <template #actions="{ data }">
        <div class="d-flex gap-1">
          <!-- Botón Editar -->
          <Button icon="pi pi-pencil" class="p-button-sm p-button-outlined p-button-rounded p-button-warning"
            v-tooltip.top="'Editar'" @click="openEditModal(data)" />

          <Button icon="pi pi-trash" class="p-button-sm p-button-outlined p-button-rounded p-button-danger"
            v-tooltip.top="'Eliminar'" @click="confirmDelete(data)" />
        </div>
      </template>


      <!-- Template de expansión personalizado -->
      <template #expansion="{ data }">
        <div class="row">
          <div class="col-md-6">
            <p><strong>Nombre completo:</strong> {{ data.full_name || '-' }}</p>
            <p><strong>Email:</strong> {{ data.email }}</p>
            <p><strong>DNI:</strong> {{ data.dni || '-' }}</p>
          </div>
          <div class="col-md-6">
            <p><strong>Celular:</strong> {{ data.celular || '-' }}</p>
            <p><strong>Creado por:</strong> {{ data.created_by?.username || 'Sistema' }}</p>
            <p><strong>Estado:</strong>
              <Tag :value="data.is_active ? 'Activo' : 'Inactivo'" :severity="data.is_active ? 'success' : 'danger'" />
            </p>
            <p><strong>is_superuser:</strong> {{ data.is_superuser || '-' }}</p>

          </div>
        </div>

        <div class="mt-3" v-if="data.groups?.length">
          <h6>Grupos asignados:</h6>
          <div class="d-flex flex-wrap gap-2">
            <Tag v-for="group in data.groups" :key="group.id" :value="group.name" severity="info" />
          </div>
        </div>
      </template>


    </DataTableWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { toast } from 'vue-sonner';
import DataTableWrapper from '@/components/ui/DataTableWrapper.vue';
import { useUserStore } from '@/stores/user/userStore';
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
// Usamos la estructura para el formulario reactivo
const form = ref({ ...FORM_STATE });


const showUserModal = ref(false);
const showDeleteModal = ref(false);
const editing = ref(false);
const isSubmitting = ref(false);
const resetPassword = ref(false);
const userToDelete = ref(null);
const userToEdit = ref(null);
const isDeleting = ref(false);


// Configuración de columnas para la tabla
const columns = ref([

  {
    field: 'username',
    header: 'Usuario',
    sortable: true,
    filter: true,
    filterOptions: computed(() =>
      userStore.users.map(u => u.username).filter((v, i, a) => a.indexOf(v) === i)
    ),
  },
  { field: 'full_name', header: 'Nombre', sortable: true, bodyTemplate: true, filter: false },
  { field: 'email', header: 'Email', sortable: true, filter: false },
  {
    field: 'is_active',
    header: 'Estado',
    sortable: true,
    bodyTemplate: true,
    filter: true,
    dataType: 'boolean',
    filterOptions: [
      { label: 'Activo', value: true },
      { label: 'Inactivo', value: false }
    ],
    filterMatchMode: 'equals'
  },
  { field: 'is_staff', 
  header: 'Staff', 
  sortable: true, 
  bodyTemplate: true, 
  filter: true ,
  dataType: 'boolean',
    filterOptions: [
      { label: 'Staff', value: true },
      { label: 'Normal', value: false }
    ],
    filterMatchMode: 'equals'
  },
  { field: 'roles', header: 'Roles', bodyTemplate: true, filter: false },
  {
    field: 'created_by', header: 'Creado por', bodyTemplate: true, filter: true, filterType: 'select',
    filterOptions: computed(() =>
      userStore.users.map(u => u.created_by).filter((v, i, a) => a.indexOf(v) === i)
    ),
  }
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
const validateForm = () => {
  errors.value = {};
  let isValid = true;

  if (!form.value.username) {
    errors.value.username = ["El nombre de usuario es requerido"];
    isValid = false;
  }

  if (!editing.value && !form.value.password) {
    errors.value.password = ["La contraseña es requerida"];
    isValid = false;
  }

  if ((!editing.value || resetPassword.value) && form.value.password !== form.value.password2) {
    errors.value.password2 = ["Las contraseñas no coinciden"];
    isValid = false;
  }

  return isValid;
};
const handleSubmit = async () => {
  // Validar formulario
  if (!validateForm()) {
    toast.error('Por favor complete todos los campos requeridos');
    return;
  }

  isSubmitting.value = true;

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
    toast.success(editing.value ? 'Usuario actualizado' : 'Usuario creado');
    
  } catch (error) {
    console.error('Error:', error);
    
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors;
      toast.error('Error en el formulario');
    } else {
      toast.error('Error inesperado: ' + error.message);
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