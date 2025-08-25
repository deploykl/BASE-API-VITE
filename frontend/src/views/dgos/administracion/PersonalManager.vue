<template>
    <div class="personal-manager">
        <div class="header">
            <h2>Gestión de Personal</h2>
            <button @click="fetchPersonal" class="btn btn-primary">
                <i class="fas fa-sync-alt"></i> Actualizar
            </button>
        </div>

        <!-- Filtros -->
        <div class="filters row mb-3">
            <div class="col-md-8">
                <input v-model="searchTerm" placeholder="Buscar por DNI, nombre, apellido..." class="form-control">
            </div>
            <div class="col-md-4">
                <select v-model="filterAcceso" class="form-select">
                    <option value="all">Todos</option>
                    <option value="true">Con acceso</option>
                    <option value="false">Sin acceso</option>
                </select>
            </div>
        </div>

        <!-- Tabla de personal -->
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>DNI</th>
                        <th>Nombre</th>
                        <th>Apellido</th>
                        <th>Email</th>
                        <th>Acceso</th>
                        <th>Módulos</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="person in filteredPersonal" :key="person.id" :class="{ 'table-success': person.acceso }">
                        <td>{{ person.dni }}</td>
                        <td>{{ person.nombre }}</td>
                        <td>{{ person.apellido }}</td>
                        <td>{{ person.email || 'Sin email' }}</td>
                        <td>
                            <span :class="['badge', person.acceso ? 'bg-success' : 'bg-danger']">
                                {{ person.acceso ? 'HABILITADO' : 'DESHABILITADO' }}
                            </span>
                        </td>
                        <td>
                            <span v-if="person.user && person.user.modulos && person.user.modulos.length">
                                {{ getModulosNames(person.user.modulos) }}
                            </span>
                            <span v-else class="text-muted">Sin módulos</span>
                        </td>
                        <td>
                            <div class="btn-group" role="group">
                                <button v-if="!person.acceso && person.email" @click="openModalHabilitar(person)"
                                    class="btn btn-success btn-sm" :disabled="loading">
                                    Habilitar
                                </button>

                                <button v-if="person.acceso" @click="openModalEditarModulos(person)"
                                    class="btn btn-secondary btn-sm" :disabled="loading" title="Editar módulos">
                                    <i class="fas fa-edit"></i> Editar
                                </button>

                                <button v-if="person.acceso" @click="deshabilitarAcceso(person)"
                                    class="btn btn-warning btn-sm" :disabled="loading">
                                    Deshabilitar
                                </button>

                                <button v-if="person.acceso" @click="resetearPassword(person)"
                                    class="btn btn-info btn-sm" :disabled="loading">
                                    Resetear Password
                                </button>
                            </div>

                            <span v-if="!person.email" class="text-danger ms-2">
                                <i class="fas fa-exclamation-circle"></i> Sin email
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Modal para habilitar/editar módulos -->
        <div class="modal fade" id="modulosModal" tabindex="-1" aria-labelledby="modulosModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modulosModalLabel">
                            {{ modalMode === 'habilitar' ? 'Habilitar acceso' : 'Editar módulos' }} 
                            para {{ selectedPerson?.nombre }} {{ selectedPerson?.apellido }}
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="modulos-selection">
                            <h6>Seleccionar módulos:</h6>
                            <div v-for="modulo in modulos" :key="modulo.id" class="form-check">
                                <input 
                                    class="form-check-input" 
                                    type="checkbox" 
                                    :id="'modulo-' + modulo.id" 
                                    :value="modulo.id" 
                                    v-model="selectedModulos"
                                >
                                <label class="form-check-label" :for="'modulo-' + modulo.id">
                                    {{ modulo.name || modulo.codename }} - {{ modulo.description }}
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button 
                            type="button" 
                            class="btn btn-primary" 
                            @click="confirmarAccionModulos" 
                            :disabled="loading || selectedModulos.length === 0"
                        >
                            <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                            {{ modalMode === 'habilitar' ? 'Habilitar' : 'Actualizar' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="d-flex justify-content-center align-items-center my-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
            <span class="ms-2">Cargando...</span>
        </div>

        <!-- Toast para mensajes de estado -->
        <div class="toast-container position-fixed top-0 end-0 p-3">
            <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header"
                    :class="{ 'bg-success': messageType === 'success', 'bg-danger': messageType === 'error', 'bg-info': messageType === 'info' }">
                    <strong class="me-auto text-white">{{ messageType === 'success' ? 'Éxito' : messageType === 'error'
                        ? 'Error' : 'Información' }}</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    {{ message }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { api } from "@/components/services/Axios"
import { Modal, Toast } from 'bootstrap'

const router = useRouter()

// Estados reactivos
const personal = ref([])
const modulos = ref([])
const loading = ref(false)
const searchTerm = ref('')
const filterAcceso = ref('all')
const message = ref('')
const messageType = ref('info')
const selectedPerson = ref(null)
const selectedModulos = ref([])
const modalMode = ref('habilitar') // 'habilitar' o 'editar'

// Computed
const filteredPersonal = computed(() => {
    let filtered = personal.value

    // Filtrar por búsqueda
    if (searchTerm.value) {
        const term = searchTerm.value.toLowerCase()
        filtered = filtered.filter(person =>
            person.dni?.toLowerCase().includes(term) ||
            person.nombre?.toLowerCase().includes(term) ||
            person.apellido?.toLowerCase().includes(term) ||
            (person.email && person.email.toLowerCase().includes(term))
        )
    }

    // Filtrar por estado de acceso
    if (filterAcceso.value !== 'all') {
        const accesoFilter = filterAcceso.value === 'true'
        filtered = filtered.filter(person => person.acceso === accesoFilter)
    }

    return filtered
})

// Métodos
const showMessage = (text, type = 'info') => {
    message.value = text
    messageType.value = type

    const toastEl = document.getElementById('liveToast')
    const toast = new Toast(toastEl)
    toast.show()

    setTimeout(() => {
        if (message.value === text) {
            message.value = ''
        }
    }, 5000)
}

const getModulosNames = (modulosArray) => {
    return modulosArray.map(m => m.name || m.codename).join(', ')
}

const fetchPersonal = async () => {
    loading.value = true
    try {
        const response = await api.get('/dgos/administracion/personal/')
        personal.value = response.data.map(person => ({
            ...person,
            // Asegurar que user.modulos siempre sea un array
            user: person.user ? {
                ...person.user,
                modulos: person.user.modulos || []
            } : null
        }))
        showMessage('Datos cargados correctamente', 'success')
    } catch (error) {
        console.error('Error fetching personal:', error)
        if (error.response?.status === 401) {
            showMessage('No autorizado. Por favor inicie sesión.', 'error')
            router.push('/login')
        } else {
            showMessage('Error al cargar los datos', 'error')
        }
    } finally {
        loading.value = false
    }
}

const fetchModulos = async () => {
    try {
        const response = await api.get('/user/modulo/')
        modulos.value = response.data
    } catch (error) {
        console.error('Error fetching módulos:', error)
        showMessage('Error al cargar los módulos', 'error')
    }
}

const openModalHabilitar = (person) => {
    selectedPerson.value = person
    selectedModulos.value = []
    modalMode.value = 'habilitar'
    
    nextTick(() => {
        const modalElement = document.getElementById('modulosModal')
        const modal = new Modal(modalElement)
        modal.show()
    })
}

const openModalEditarModulos = (person) => {
    selectedPerson.value = person
    modalMode.value = 'editar'
    
    // Pre-seleccionar los módulos actuales del usuario
    if (person.user && person.user.modulos) {
        selectedModulos.value = person.user.modulos.map(modulo => modulo.id)
    } else {
        selectedModulos.value = []
    }
    
    nextTick(() => {
        const modalElement = document.getElementById('modulosModal')
        const modal = new Modal(modalElement)
        modal.show()
    })
}

const confirmarAccionModulos = async () => {
    if (!selectedPerson.value) return

    loading.value = true
    try {
        let response
        if (modalMode.value === 'habilitar') {
            // Habilitar acceso con módulos seleccionados
            response = await api.post(
                `/dgos/administracion/personal/${selectedPerson.value.id}/habilitar_acceso/`,
                { modulos: selectedModulos.value }
            )
        } else {
            // Editar módulos existentes
            response = await api.put(
                `/dgos/administracion/personal/${selectedPerson.value.id}/modulos/`,
                { modulos: selectedModulos.value }
            )
        }
        
        if (response.data.success) {
            showMessage(response.data.message, 'success')
            await fetchPersonal() // Recargar datos
            
            // Cerrar el modal
            const modalElement = document.getElementById('modulosModal')
            const modal = Modal.getInstance(modalElement)
            modal.hide()
        } else {
            showMessage(response.data.message, 'error')
        }
    } catch (error) {
        console.error('Error gestionando módulos:', error)
        showMessage('Error al gestionar módulos', 'error')
    } finally {
        loading.value = false
    }
}

const deshabilitarAcceso = async (person) => {
    if (!confirm(`¿Deshabilitar acceso a ${person.nombre} ${person.apellido}?`)) {
        return
    }

    loading.value = true
    try {
        const response = await api.post(`/dgos/administracion/personal/${person.id}/deshabilitar_acceso/`)

        if (response.data.success) {
            showMessage(response.data.message, 'success')
            await fetchPersonal() // Recargar datos
        } else {
            showMessage(response.data.message, 'error')
        }
    } catch (error) {
        console.error('Error deshabilitando acceso:', error)
        showMessage('Error al deshabilitar acceso', 'error')
    } finally {
        loading.value = false
    }
}

const resetearPassword = async (person) => {
    if (!confirm(`¿Resetear contraseña de ${person.nombre} ${person.apellido}?`)) {
        return
    }

    loading.value = true
    try {
        const response = await api.post(`/dgos/administracion/personal/${person.id}/resetear_password/`)

        if (response.data.success) {
            showMessage(response.data.message, 'success')
        } else {
            showMessage(response.data.message, 'error')
        }
    } catch (error) {
        console.error('Error reseteando password:', error)
        showMessage('Error al resetear contraseña', 'error')
    } finally {
        loading.value = false
    }
}

// Lifecycle
onMounted(() => {
    fetchPersonal()
    fetchModulos()
})
</script>

<style scoped>
.personal-manager {
    padding: 20px;
}

.modal-body {
    max-height: 60vh;
    overflow-y: auto;
}

.btn-group {
    flex-wrap: wrap;
    gap: 5px;
}

.form-check {
    margin-bottom: 8px;
}

.form-check-label {
    margin-left: 5px;
}
</style>