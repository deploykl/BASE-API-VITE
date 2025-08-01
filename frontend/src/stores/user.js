import { defineStore } from "pinia";
import { ref, computed } from "vue";
import defaultAvatar from "@/assets/img/header/default-avatar.png";
import { api } from "@/components/services/Axios";
import { toast } from 'vue-sonner';

export const useUserStore = defineStore("user", () => {
  const userData = ref({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    dni: "",
    celular: "",
    image: "",
  });

  const imageError = ref(false);
  const loading = ref(false);

  const effectiveUserImage = computed(() => {
    if (imageError.value || !userData.value.image) return defaultAvatar;
    if (userData.value.image.startsWith("data:")) return userData.value.image;
    
    const cacheBuster = `?t=${Date.now()}`;
    
    if (userData.value.image.startsWith("http")) {
      return `${userData.value.image}${cacheBuster}`;
    }
    
    if (!userData.value.image.startsWith("/media/")) {
      return `${process.env.VUE_APP_IMG_SERVER}media/${userData.value.image}${cacheBuster}`;
    }
    
    return `${process.env.VUE_APP_IMG_SERVER}${userData.value.image.replace(/^\/+/, "")}${cacheBuster}`;
  });
  
  const fullName = computed(() => `${userData.value.first_name} ${userData.value.last_name}`.trim());

  // Función logout dentro del store
  function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('refreshToken');
    window.location.href = '/login';
  }

  async function fetchUserProfile() {
    loading.value = true;
    try {
      const response = await api.get("user/profile/");
      updateUserData(response.data);
      imageError.value = false;
      return response.data;
    } catch (error) {
      if (error.response?.status === 401) {
        // El interceptor ya maneja el 401, solo necesitamos limpiar si falla el refresh
        if (error.config.url.includes('token/refresh')) {
          logout(); // Ahora está definida
        }
      }
      console.error("Error al obtener perfil:", error);
      imageError.value = true;
      throw error;
    } finally {
      loading.value = false;
    }
  }

  function updateUserData(newData) {
    userData.value = {
      ...userData.value,
      ...newData,
      image: newData.image 
        ? newData.image.startsWith("data:") 
          ? newData.image 
          : `${newData.image}?${Date.now()}`
        : ""
    };
  }

  function setImageError(value) {
    imageError.value = value;
  }

  async function updateUserProfile(selectedImage) {
    loading.value = true;

    try {
      const formData = new FormData();
      formData.append('username', userData.value.username);
      formData.append('email', userData.value.email);
      formData.append('first_name', userData.value.first_name);
      formData.append('last_name', userData.value.last_name);
      formData.append('dni', userData.value.dni);
      formData.append('celular', userData.value.celular);

      if (selectedImage) {
        formData.append('image', selectedImage);
      }

      const response = await toast.promise(
        api.put('user/profile/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        }),
        {
          loading: 'Actualizando perfil...',
          success: (data) => {
            updateUserData({
              ...data.data,
              image: data.data.image ? `${data.data.image}?t=${Date.now()}` : ''
            });
            return 'Perfil actualizado correctamente';
          },
          error: (error) => {
            const errorData = error.response?.data || {};
            let errorMessage = 'Error al actualizar el perfil';
            
            if (typeof errorData === 'string') {
              errorMessage = errorData;
            } else if (Array.isArray(errorData)) {
              errorMessage = errorData.join(' ');
            } else if (typeof errorData === 'object') {
              if (errorData.dni && errorData.dni.length > 0) {
                errorMessage = typeof errorData.dni === 'string' 
                  ? errorData.dni 
                  : errorData.dni.join(' ');
              } else if (errorData.celular && errorData.celular.length > 0) {
                errorMessage = typeof errorData.celular === 'string' 
                  ? errorData.celular 
                  : errorData.celular.join(' ');
              } else if (errorData.username) {
                errorMessage = Array.isArray(errorData.username) 
                  ? errorData.username.join(' ') 
                  : errorData.username;
              } else if (errorData.email) {
                errorMessage = Array.isArray(errorData.email) 
                  ? errorData.email.join(' ') 
                  : errorData.email;
              } else if (errorData.detail) {
                errorMessage = errorData.detail;
              } else if (errorData.non_field_errors) {
                errorMessage = Array.isArray(errorData.non_field_errors) 
                  ? errorData.non_field_errors.join(' ') 
                  : errorData.non_field_errors;
              } else {
                const firstErrorKey = Object.keys(errorData)[0];
                const firstErrorValue = errorData[firstErrorKey];
                errorMessage = Array.isArray(firstErrorValue) 
                  ? firstErrorValue.join(' ') 
                  : firstErrorValue;
              }
            }
            return errorMessage || 'Error desconocido al actualizar el perfil';
          }
        }
      );

      return true;
    } catch (error) {
      console.error('Error en updateProfile:', error);
      return false;
    } finally {
      loading.value = false;
    }
  }

  return {
    userData,
    imageError,
    loading,
    effectiveUserImage,
    fullName,
    fetchUserProfile,
    updateUserData,
    setImageError,
    updateUserProfile,
    logout // Exporta la función si necesitas usarla desde otros componentes
  };
});