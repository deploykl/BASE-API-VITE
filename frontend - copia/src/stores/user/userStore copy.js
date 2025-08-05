import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from '@/components/services/Axios';
import { toast } from 'vue-sonner';

export const useUserStore = defineStore('userStore', () => {
  // Estado
  const loading = ref(false);
  const users = ref([]);
  const error = ref(null);

  // Métodos
const listUsers = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await api.get('user/users/');
    // Agregar fullName a cada usuario
    users.value = response.data.map(user => ({
      ...user,
      fullName: `${user.first_name || ''} ${user.last_name || ''}`.trim() || '-'
    }));
    return users.value;
  } catch (err) {
    error.value = err;
    const message = err.response?.data?.detail || 
                   err.response?.data?.message || 
                   'Error al obtener usuarios';
    toast.error(message);
    throw err;
  } finally {
    loading.value = false;
  }
};

const createUser = async (userData) => {
  try {
    const { password2, ...dataToSend } = userData;
    const response = await api.post('user/users/', dataToSend);
    
    users.value.unshift(response.data);
    toast.success('Usuario creado correctamente');
    return response.data;
  } catch (err) {
    error.value = err;
    
    // Manejo mejorado de errores
    if (err.response?.data) {
      // Mostrar todos los errores de campo
      for (const [field, messages] of Object.entries(err.response.data)) {
        const errorMsg = Array.isArray(messages) ? messages[0] : messages;
        toast.error(`${field}: ${errorMsg}`);
      }
    } else {
      toast.error(err.message || 'Error al crear usuario');
    }
    
    throw err;
  } finally {
  }
};

const updateUser = async (id, userData) => {
  try {
    const { password2, ...dataToSend } = userData;
    const response = await api.patch(`user/users/${id}/`, dataToSend);
    
    // Actualizar el usuario en la lista con fullName
    const updatedUser = {
      ...response.data,
      fullName: `${response.data.first_name || ''} ${response.data.last_name || ''}`.trim() || '-'
    };
    
    const index = users.value.findIndex(u => u.id === id);
    if (index !== -1) {
      users.value[index] = updatedUser;
    }
    
    return updatedUser;
  } catch (err) {
    error.value = err;
    
    if (err.response?.data?.username) {
      toast.error(err.response.data.username[0]);
    } else if (err.response?.data?.email) {
      toast.error(err.response.data.email[0]);
    } else {
      const message = err.response?.data?.detail || 
                     'Error al actualizar usuario';
      toast.error(message);
    }
    
    throw err; // Esto es importante para que el componente sepa que hubo un error
  } finally {
  }
};

  const deleteUser = async (id) => {
    try {
      await api.delete(`user/users/${id}/`);
      
      users.value = users.value.filter(u => u.id !== id);
      toast.success('Usuario eliminado correctamente');
      return true;
    } catch (err) {
      error.value = err;
      const message = err.response?.data?.detail || 
                     err.response?.data?.message || 
                     'Error al eliminar usuario';
      toast.error(message);
      throw err;
    } finally {
    }
  };

  const toggleUserStatus = async (id, newStatus) => {
    try {
      const endpoint = newStatus ? 'activate' : 'deactivate';
      await api.post(`user/users/${id}/${endpoint}/`);
      
      const user = users.value.find(u => u.id === id);
      if (user) {
        user.is_active = newStatus;
      }
      toast.success(`Usuario ${newStatus ? 'activado' : 'desactivado'} correctamente`);
      return true;
    } catch (err) {
      error.value = err;
      const message = err.response?.data?.detail || 
                     err.response?.data?.message || 
                     `Error al ${newStatus ? 'activar' : 'desactivar'} usuario`;
      toast.error(message);
      throw err;
    } finally {
    }
  };

  const toggleStaffStatus = async (id, newStatus) => {
    try {
      const endpoint = newStatus ? 'make_staff' : 'remove_staff';
      await api.post(`user/users/${id}/${endpoint}/`);
      
      const user = users.value.find(u => u.id === id);
      if (user) {
        user.is_staff = newStatus;
      }
      toast.success(`Usuario ${newStatus ? 'promovido a staff' : 'removido de staff'} correctamente`);
      return true;
    } catch (err) {
      error.value = err;
      const message = err.response?.data?.detail || 
                     err.response?.data?.message || 
                     `Error al ${newStatus ? 'promover' : 'remover'} staff`;
      toast.error(message);
      throw err;
    } finally {
    }
  };

  return {
    // Estado
    loading,
    users,
    error,
    
    // Métodos
    listUsers,
    createUser,
    updateUser,
    deleteUser,
    toggleUserStatus,
    toggleStaffStatus
  };
});