<template>
    <div class="container">
        <ModalBase :visible="showUserModal" :mode="editing ? 'edit' : 'create'" entityName="usuario"
            :confirm-text="isSubmitting ? 'Guardando...' : 'Guardar'" :loading="isSubmitting" @close="closeUserModal"
            @confirm="handleSubmit">
            <template #content>
                <form @submit.prevent="handleSubmit">
                    <div class="row">
                        <div class="col-md-6">
                            <!-- Username -->
                            <FloatInput id="username" label="Nombre de usuario" v-model="form.username"
                                icon="pi pi-user-edit" :errors="errors" :invalid="!!errors.username" size="small" />

                            <!-- Email -->
                            <FloatInput id="email" label="Email" v-model="form.email" type="email" icon="pi pi-envelope"
                                :invalid="!!errors.email" :errors="errors" size="small" />

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
                            <FloatInput id="celular" label="Celular" v-model="form.celular" icon="pi pi-phone"
                                maxlength="9" :invalid="!!errors.celular" :errors="errors"
                                placeholder="Ingrese 9 dígitos" size="small" />
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-check form-switch mb-3">
                                <input v-model="form.is_active" class="form-check-input" type="checkbox"
                                    id="isActiveCheck">
                                <label class="form-check-label" for="isActiveCheck">Activo</label>
                            </div>
                        </div>
                       
                    </div>
                </form>
            </template>
        </ModalBase>

        <!-- Listado de usuarios -->
        <DataTableWrapper :data="tableroStore.tableros" :columns="columns" :loading="tableroStore.loading" :actions="true"
            :showCreateButton="true" title="GESTIÓN DE TABLEROS" createButtonLabel="Nuevo Usuario"
            createButtonIcon="pi pi-user-plus" @create="openCreateModal">
            <!-- sortField="is_active" :sortOrder="-1" para poner estado activo -->

            <!-- Template para full_name -->
            <template #body-full_name="{ data }">
                {{ data.name || '-' }}
            </template>

            <!-- Template para is_active -->
            <template #body-is_active="{ data }">
                <div class="d-flex flex-column align-items-center">
                    <ToggleSwitch v-model="data.is_active" @change="tableroStore.toggleUserStatus(data.id, data.is_active)"
                        class="mb-1" />
                    <span class="badge custom-badge" :class="data.is_active ? 'bg-success' : 'bg-danger'">
                        {{ data.is_active ? 'Activo' : 'Inactivo' }}
                    </span>
                </div>
            </template>

            <!-- Template para is_staff -->
            <template #body-is_staff="{ data }">
                <div class="d-flex flex-column align-items-center">
                    <ToggleSwitch v-model="data.is_staff" @change="tableroStore.toggleStaffStatus(data.id, data.is_staff)"
                        class="mb-1" />
                    <span class="badge custom-badge" :class="data.is_staff ? 'bg-info' : 'bg-secondary'">
                        {{ data.is_staff ? 'Staff' : 'Normal' }}
                    </span>
                </div>
            </template>

            <!-- Template para roles -->
            <template #body-roles="{ data }">
                <div class="d-flex gap-2">
                    <span v-if="data.is_superuser" class="badge bg-danger"
                        v-tooltip.top="'Usuario con todos los permisos'">
                        <i class="fas fa-crown me-1"></i>
                        SuperUser
                    </span>
                    <span v-if="data.is_staff" class="badge bg-info text-dark"
                        v-tooltip.top="'Usuario con permisos de staff'">
                        <i class="fas fa-user-tie me-1"></i>
                        Staff
                    </span>
                    <span v-if="!data.is_superuser && !data.is_staff" class="badge bg-secondary"
                        v-tooltip.top="'Usuario normal'">
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

                    <Button icon="pi pi-times" class="p-button-sm p-button-outlined p-button-rounded p-button-danger"
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
                            <Tag :value="data.is_active ? 'Activo' : 'Inactivo'"
                                :severity="data.is_active ? 'success' : 'danger'" />
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

import ModalBase from '@/components/ui/ModalBase.vue';
import DataTableWrapper from '@/components/ui/DataTableWrapper.vue';
import { useTableroStore } from '@/stores/dimon/tableroStore';
import FloatInput from '@/components/widgets/FloatInput.vue';

const tableroStore = useTableroStore();
const errors = ref({});

const showUserModal = ref(false);
const showDeleteModal = ref(false);
const editing = ref(false);
const isSubmitting = ref(false);
const resetPassword = ref(false);
const userToDelete = ref(null);
const userToEdit = ref(null);
const isDeleting = ref(false);

// Definimos la estructura del formulario como constante
const FORM_STATE = {
  name: '',
  url: '',
  description: '',
  source: '',
  last_updated: '',
  update_frequency: '',
  created_by: '',
  created_at: '',
  updated_at: '',
};
// Usamos la estructura para el formulario reactivo
const form = ref({ ...FORM_STATE });

const columns = ref([
  {
    field: 'name',
    header: 'Nombre',
    sortable: true,
    filter: true,
    filterOptions: computed(() =>
      tableroStore.tableros.map(u => u.name).filter((v, i, a) => a.indexOf(v) === i)
    ),
  },

]);
// Métodos
const resetForm = () => {
  form.value = { ...FORM_STATE };
  resetPassword.value = false;
  errors.value = {};
};

const openCreateModal = () => {
  resetForm();
  editing.value = false;
  showUserModal.value = true;
};
const closeUserModal = () => {
  showUserModal.value = false;
  resetForm();
};

const confirmDelete = (user) => {
  userToDelete.value = user;
  showDeleteModal.value = true;
};
const proceedDelete = async () => {
  isDeleting.value = true;
  try {
    const success = await tableroStore.deleteUser(userToDelete.value.id);
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
      await tableroStore.updateUser(userToEdit.value.id, userData);
    } else {
      await tableroStore.createUser(userData);
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
    tableroStore.loading = true;
    await tableroStore.listUsers();
  } catch (error) {
  } finally {
    tableroStore.loading = false;
  }
});
</script>

<style scoped></style>