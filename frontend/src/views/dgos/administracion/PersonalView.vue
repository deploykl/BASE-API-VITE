<template>
    <div class="container-fluid">
        <!-- Modal para crear/editar personal -->
        <ModalBase :visible="showModal" :mode="editing ? 'edit' : 'create'" entityName="personal"
            :confirm-text="isSubmitting ? 'Guardando...' : 'Guardar'" :loading="isSubmitting" @close="closeModal"
            @confirm="handleSubmit">
            <template #content>
                <form @submit.prevent="handleSubmit" class="needs-validation" novalidate>
                    <!-- Pestañas para organizar la información -->
                    <div class="mb-5">
                        <ul class="nav nav-tabs" id="personalTabs" role="tablist">
                            <li class="nav-item" role="presentation">
                                <button class="nav-link active" id="basic-tab" data-bs-toggle="tab"
                                    data-bs-target="#basic" type="button" role="tab" aria-controls="basic"
                                    aria-selected="true">Información General</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="contract-tab" data-bs-toggle="tab"
                                    data-bs-target="#contract" type="button" role="tab" aria-controls="contract"
                                    aria-selected="false">Datos Laborales</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="emergency-tab" data-bs-toggle="tab"
                                    data-bs-target="#emergency" type="button" role="tab" aria-controls="emergency"
                                    aria-selected="false">Emergencia</button>
                            </li>
                        </ul>
                    </div>

                    <div class="tab-content" id="personalTabsContent">
                        <!-- Pestaña de Información Básica -->
                        <div class="tab-pane fade show active" id="basic" role="tabpanel" aria-labelledby="basic-tab">
                            <div class="row g-3">
                                <!-- Columna 1 -->
                                <div class="col-md-3">

                                    <!-- Nombre -->
                                    <div class="mb-3">
                                        <FloatInput id="nombre" label="Nombres" v-model="form.nombre" icon="pi pi-user"
                                            :errors="errors" :invalid="!!errors.nombre" size="small" required />
                                    </div>
                                    <!-- Email -->
                                    <div class="mb-3">
                                        <FloatInput id="email" label="Email Institucional" v-model="form.email"
                                            type="email" icon="pi pi-envelope" :invalid="!!errors.email"
                                            :errors="errors" size="small" />
                                    </div>

                                    <div class="mb-3">
                                        <FloatLabel>
                                            <label for="fecha_nac" class="form-label" style="font-size: 0.8rem;">
                                                <i class="pi pi-calendar me-2"></i>
                                                Fecha de Nacimiento
                                            </label>
                                            <DatePicker v-model="form.fecha_nac" id="fecha_nac"
                                                :showIcon="false" class="w-100" size="small"
                                                :class="{ 'is-invalid': !!errors.fecha_nac }" inputId="fecha_nac"
                                                :showClear="true" />
                                        </FloatLabel>

                                        <div v-if="errors.fecha_nac" class="invalid-feedback d-block">
                                            {{ errors.fecha_nac[0] }}
                                        </div>
                                    </div>
                                </div>
                                <!-- Columna 2 -->
                                <div class="col-md-3">
                                    <!-- Apellido -->
                                    <div class="mb-3">
                                        <FloatInput id="apellido" label="Apellidos" v-model="form.apellido"
                                            icon="pi pi-user" :invalid="!!errors.apellido" :errors="errors" size="small"
                                            required />
                                    </div>

                                    <!-- Email personal -->
                                    <div class="mb-3">
                                        <FloatInput id="email_per" label="Email Personal" v-model="form.email_per"
                                            type="email" icon="pi pi-envelope" :invalid="!!errors.email_per"
                                            :errors="errors" size="small" />
                                    </div>
                                    <!-- Sexo -->
                                    <div class="mb-5">
                                        <Dropdown id="sexo" v-model="form.sexo" :options="sexoOptions"
                                            optionLabel="label" optionValue="value" placeholder="Seleccionar género"
                                            :class="{ 'p-invalid': !!errors.sexo }" class="w-100" size="small"
                                            :showClear="true">
                                            <template #option="slotProps">
                                                <div class="flex align-items-center">
                                                    <i :class="slotProps.option.value === 'M' ? 'pi pi-mars text-primary' : 'pi pi-venus text-danger'"
                                                        style="font-size: 1rem; margin-right: 8px;"></i>
                                                    <span>{{ slotProps.option.label }}</span>
                                                </div>
                                            </template>
                                            <template #value="slotProps">
                                                <div v-if="slotProps.value" class="flex align-items-center">
                                                    <i :class="slotProps.value === 'M' ? 'pi pi-mars text-primary' : 'pi pi-venus text-danger'"
                                                        style="font-size: 1rem; margin-right: 8px;"></i>
                                                    <span>{{ slotProps.value === 'M' ? 'Masculino' : 'Femenino'
                                                    }}</span>
                                                </div>
                                                <span v-else>
                                                    {{ slotProps.placeholder }}
                                                </span>
                                            </template>
                                        </Dropdown>
                                        <small v-if="errors.sexo" class="p-error">
                                            {{ errors.sexo[0] }}
                                        </small>
                                    </div>


                                </div>
                                <!-- Columna 3 -->
                                <div class="col-md-3">
                                    <!-- DNI -->
                                    <div class="mb-3">
                                        <FloatInput id="dni" label="DNI" v-model="form.dni" icon="pi pi-id-card"
                                            :errors="errors" :invalid="!!errors.dni" size="small" type="tel" required
                                            maxlength="8" @input="onlyNumbersDNI" />
                                    </div>

                                    <!-- Celular -->
                                    <div class="mb-1">
                                        <FloatInput id="celular" label="Celular" v-model="form.celular"
                                            icon="pi pi-mobile" :invalid="!!errors.celular" :errors="errors"
                                            size="small" maxlength="9" @input="onlyNumbersCelular" />
                                    </div>

                                    <!-- Es Padre / Madre -->
                                    <div class="mb-2">
                                        <Dropdown id="padre_madre" v-model="form.padre_madre" :options="opcionesSiNo"
                                            optionLabel="label" optionValue="value" placeholder="Es Padre / Madre"
                                            :class="{ 'p-invalid': !!errors.padre_madre }" class="w-100" size="small"
                                            :showClear="true" @change="handlePadreMadreChange">
                                        </Dropdown>
                                        <small v-if="errors.padre_madre" class="p-error">
                                            {{ errors.padre_madre[0] }}
                                        </small>
                                    </div>
                                </div>
                                <!-- Columna 4 -->
                                <div class="col-md-3">

                                    <!-- RUC -->
                                    <div class="mb-3">
                                        <FloatInput id="ruc" label="RUC" v-model="form.ruc"
                                            icon="bi bi-person-badge-fill" :errors="errors" :invalid="!!errors.ruc"
                                            size="small" required maxlength="11" @input="onlyNumbersRUC" />
                                    </div>
                                    <!-- Teléfono -->
                                    <div class="mb-1">
                                        <FloatInput id="telefono" label="Teléfono" v-model="form.telefono"
                                            icon="pi pi-phone" :invalid="!!errors.telefono" :errors="errors"
                                            size="small" maxlength="8" @input="onlyNumbersTelefono"
                                            placeholder="123-4567" />
                                    </div>

                                    <!-- Número de hijos (siempre visible pero desactivado cuando no es padre/madre) -->
                                    <div class="mb-3">
                                        <Dropdown id="n_hijos" v-model="form.n_hijos" :options="hijosOptions"
                                            optionLabel="label" optionValue="value"
                                            :placeholder="form.padre_madre === 'Si' ? 'N° de hijos' : 'N° de hijos'"
                                            :class="{ 'p-invalid': !!errors.n_hijos, 'disabled-field': form.padre_madre !== 'Si' }"
                                            class="w-100" size="small" :disabled="form.padre_madre !== 'Si'"
                                            :showClear="true" />
                                        <small v-if="errors.n_hijos" class="p-error">
                                            {{ errors.n_hijos[0] }}
                                        </small>
                                    </div>
                                </div>
                            </div>

                            <div class="row g-3">
                                <div class="col-md-8">
                                    <!-- Dirección -->
                                    <div class="mb-3">
                                        <FloatInput id="direccion" label="Dirección" v-model="form.direccion"
                                            icon="pi pi-map-marker" :invalid="!!errors.direccion" :errors="errors"
                                            size="small" />
                                    </div>
                                </div>

                                <div class="col-md-4">
                                    <!-- Distrito -->
                                    <div class="mb-3">
                                        <Dropdown id="distrito" v-model="form.distrito" :options="distritosLima"
                                            optionLabel="label" optionValue="value" placeholder="Seleccione distrito"
                                            :class="{ 'p-invalid': !!errors.distrito }" class="w-100" size="small"
                                            :filter="true" filterPlaceholder="Buscar distrito..." :showClear="true" />
                                        <small v-if="errors.distrito" class="p-error">
                                            {{ errors.distrito[0] }}
                                        </small>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Pestaña de Datos Laborales -->
                        <div class="tab-pane fade" id="contract" role="tabpanel" aria-labelledby="contract-tab">
                            <div class="row g-3">
                                <!-- Columna 1 -->
                                <div class="col-md-4">
                                    <!-- Dependencia -->
                                    <div class="mb-5">
                                        <small for="dependencia" class="form-label">
                                            <i class="pi pi-sitemap me-2"></i> <!-- Icono de organización -->
                                            Dependencia
                                        </small>
                                        <Dropdown id="dependencia" v-model="form.dependencia"
                                            :options="dependenciasOptions" optionLabel="nombre" optionValue="id"
                                            placeholder="Seleccionar dependencia"
                                            :class="{ 'p-invalid': !!errors.dependencia }" class="w-100"
                                            :showClear="true" size="small" />
                                        <small v-if="errors.dependencia" class="p-error">
                                            {{ errors.dependencia[0] }}
                                        </small>
                                    </div>
                                    <!-- Fecha de inicio -->
                                    <div class="mb-3">
                                        <FloatLabel>
                                            <label for="fecha_inicio" class="form-label" style="font-size: 0.8rem;">
                                                <i class="pi pi-calendar-plus me-2"></i>
                                                <!-- Icono de calendario con plus -->
                                                Fecha de Inicio
                                            </label>
                                            <DatePicker v-model="form.fecha_inicio" id="fecha_inicio"
                                                dateFormat="dd/mm/yy" :showIcon="false" class="w-100"
                                                :class="{ 'is-invalid': !!errors.fecha_inicio }" inputId="fecha_inicio"
                                                :showClear="true" />
                                        </FloatLabel>

                                        <div v-if="errors.fecha_inicio" class="invalid-feedback d-block">
                                            {{ errors.fecha_inicio[0] }}
                                        </div>
                                    </div>
                                    <!-- Estado -->
                                    <div class="mb-3">
                                        <small for="estado" class="form-label">
                                            <i class="pi pi-info-circle me-2"></i> <!-- Icono de información -->
                                            Estado
                                        </small>
                                        <Dropdown id="estado" v-model="form.estado" :options="estadoOptions"
                                            optionLabel="nombre" optionValue="id" placeholder="Seleccionar estado"
                                            :class="{ 'p-invalid': !!errors.estado }" class="w-100" :showClear="true"
                                            size="small" />
                                        <small v-if="errors.estado" class="p-error">
                                            {{ errors.estado[0] }}
                                        </small>
                                    </div>
                                    <!-- Grupo Ocupacional -->
                                    <div class="mb-3">
                                        <small for="grupo_ocupacional" class="form-label">
                                            <i class="pi pi-briefcase me-2"></i> <!-- Icono de maletín -->
                                            Grupo Ocupacional
                                        </small>
                                        <Dropdown id="grupo_ocupacional" v-model="form.grupo_ocupacional"
                                            :options="grupoOcupacionalOptions" optionLabel="nombre" optionValue="id"
                                            placeholder="Seleccionar grupo ocupacional"
                                            :class="{ 'p-invalid': !!errors.grupo_ocupacional }" class="w-100"
                                            :showClear="true" size="small" />
                                        <small v-if="errors.grupo_ocupacional" class="p-error">
                                            {{ errors.grupo_ocupacional[0] }}
                                        </small>
                                    </div>
                                    <!-- Nivel -->
                                    <div class="mb-3">
                                        <small for="nivel" class="form-label">
                                            <i class="pi pi-sort-alt me-2"></i> <!-- Icono de niveles -->
                                            Nivel
                                        </small>
                                        <Dropdown id="nivel" v-model="form.nivel" :options="nivelOptions"
                                            optionLabel="name" optionValue="id" placeholder="Seleccionar nivel"
                                            :class="{ 'p-invalid': !!errors.nivel }" class="w-100" :showClear="true"
                                            size="small" />
                                        <small v-if="errors.nivel" class="p-error">
                                            {{ errors.nivel[0] }}
                                        </small>
                                    </div>
                                </div>
                                <!-- Columna 2 -->
                                <div class="col-md-4">
                                    <!-- Área (dependiente de la dependencia) -->
                                    <div class="mb-5">
                                        <small for="area" class="form-label">
                                            <i class="pi pi-building me-2"></i> <!-- Icono de edificio -->
                                            Área
                                        </small>
                                        <Dropdown id="area" v-model="form.area" :options="areasOptions"
                                            optionLabel="nombre" optionValue="id" placeholder="Seleccionar área"
                                            :disabled="!form.dependencia || personalStore.loading"
                                            :class="{ 'p-invalid': !!errors.area }" class="w-100 " :showClear="true"
                                            size="small" />
                                        <small v-if="errors.area" class="p-error">
                                            {{ errors.area[0] }}
                                        </small>

                                        <small v-if="personalStore.loading" class="text-info">
                                            <i class="pi pi-spinner pi-spin"></i> Cargando áreas...
                                        </small>
                                    </div>

                                    <!-- Fecha de fin -->
                                    <div class="mb-3">
                                        <FloatLabel>
                                            <label for="fecha_fin" class="form-label" style="font-size: 0.8rem;">
                                                <i class="pi pi-calendar-minus me-2"></i>
                                                <!-- Icono de calendario con menos -->
                                                Fecha de Fin
                                            </label>
                                            <DatePicker v-model="form.fecha_fin" id="fecha_fin" dateFormat="dd/mm/yy"
                                                :showIcon="false" class="w-100"
                                                :class="{ 'is-invalid': !!errors.fecha_fin }" inputId="fecha_fin"
                                                :showClear="true" />
                                        </FloatLabel>

                                        <div v-if="errors.fecha_fin" class="invalid-feedback d-block">
                                            {{ errors.fecha_fin[0] }}
                                        </div>
                                    </div>
                                    <!-- cargo -->
                                    <div class="mb-3">
                                        <small for="cargo" class="form-label">
                                            <i class="pi pi-id-card me-2"></i> <!-- Icono de identificación -->
                                            Cargo
                                        </small>
                                        <Dropdown id="cargo" v-model="form.cargo" :options="cargoOptions"
                                            optionLabel="nombre" optionValue="id" placeholder="Seleccionar cargo"
                                            :class="{ 'p-invalid': !!errors.cargo }" class="w-100" :filter="true"
                                            filterPlaceholder="Buscar cargo..." :showClear="true" size="small" />
                                        <small v-if="errors.cargo" class="p-error">
                                            {{ errors.cargo[0] }}
                                        </small>
                                    </div>
                                    <!-- Genérica -->
                                    <div class="mb-3">
                                        <div class="mb-3">
                                            <small for="generica" class="form-label">
                                                <i class="pi pi-tags me-2"></i> <!-- Icono de etiquetas -->
                                                Genérica
                                            </small>
                                            <Dropdown id="generica" v-model="form.generica" :options="genericaOptions"
                                                optionLabel="nombre" optionValue="id" placeholder="Seleccionar genérica"
                                                :class="{ 'p-invalid': !!errors.generica }" class="w-100"
                                                :showClear="true" />
                                            <small v-if="errors.generica" class="p-error">
                                                {{ errors.generica[0] }}
                                            </small>
                                        </div>
                                    </div>

                                    <!-- Régimen -->
                                    <div class="mb-3">
                                        <small for="regimen" class="form-label">
                                            <i class="pi pi-sliders-h me-2"></i> <!-- Icono de ajustes -->
                                            Régimen
                                        </small>
                                        <Dropdown id="regimen" v-model="form.regimen" :options="regimenOptions"
                                            optionLabel="nombre" optionValue="id" placeholder="Seleccionar régimen"
                                            :class="{ 'p-invalid': !!errors.regimen }" class="w-100" :showClear="true"
                                            size="small" />
                                        <small v-if="errors.regimen" class="p-error">
                                            {{ errors.regimen[0] }}
                                        </small>
                                    </div>
                                </div>
                                <!-- Columna 3 -->
                                <div class="col-md-4">
                                    <!-- Condición -->
                                    <div class="mb-4">
                                        <small for="condicion" class="form-label">
                                            <i class="pi pi-check-circle me-2"></i> <!-- Icono de verificación -->
                                            Condición
                                        </small>
                                        <Dropdown id="condicion" v-model="form.condicion" :options="condicionOptions"
                                            optionLabel="nombre" optionValue="id" placeholder="Seleccionar condicion"
                                            :class="{ 'p-invalid': !!errors.condicion }" class="w-100"
                                            :showClear="true" />
                                        <small v-if="errors.condicion" class="p-error">
                                            {{ errors.condicion[0] }}
                                        </small>
                                    </div>
                                    <!-- Profesión -->
                                    <div class="mb-5">
                                        <small for="profesion" class="form-label">
                                            <i class="pi pi-graduation-cap me-2"></i> <!-- Icono de graduación -->
                                            Profesión
                                        </small>
                                        <Dropdown id="profesion" v-model="form.profesion" :options="profesionOptions"
                                            optionLabel="nombre" optionValue="id" placeholder="Seleccionar profesión"
                                            :class="{ 'p-invalid': !!errors.profesion }" class="w-100" :filter="true"
                                            filterPlaceholder="Buscar profesion..." :showClear="true" size="small" />
                                        <small v-if="errors.profesion" class="p-error">
                                            {{ errors.profesion[0] }}
                                        </small>
                                    </div>
                                    <!-- salario -->
                                    <div class="mb-2">
                                        <FloatInput id="salario" label="Salario" v-model="form.salario"
                                            icon="pi pi-money-bill" :invalid="!!errors.salario" :errors="errors"
                                            size="small" type="text" @input="formatSalario" currency="PEN" />
                                    </div>
                                    <!-- Número de contrato -->
                                    <div class="mb-3">
                                        <FloatInput id="n_contrato" label="Número de Contrato" v-model="form.n_contrato"
                                            icon="pi pi-file-edit" :invalid="!!errors.n_contrato" :errors="errors"
                                            size="small" />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Pestaña de Datos de Emergencia -->
                        <div class="tab-pane fade" id="emergency" role="tabpanel" aria-labelledby="emergency-tab">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <!-- Contacto de emergencia -->
                                    <div class="mb-3">
                                        <FloatInput id="cont_emergencia" label="Contacto de Emergencia"
                                            v-model="form.cont_emergencia" icon="pi pi-user"
                                            :invalid="!!errors.cont_emergencia" :errors="errors" size="small" />
                                    </div>


                                </div>

                                <div class="col-md-6">
                                    <!-- Celular de emergencia -->
                                    <div class="mb-3">
                                        <FloatInput id="cel_emergencia" label="Celular de Emergencia"
                                            v-model="form.cel_emergencia" icon="pi pi-phone"
                                            :invalid="!!errors.cel_emergencia" :errors="errors" size="small" />
                                    </div>


                                </div>
                            </div>
                        </div>
                    </div>
                </form>
            </template>
        </ModalBase>

        <!-- Modal de confirmación para eliminar -->
        <ModalBase :visible="showDeleteModal" mode="delete" entityName="personal"
            confirm-text="Eliminar Permanentemente" confirm-class="p-button-danger" :loading="isDeleting"
            @close="closeDeleteModal" @confirm="proceedDelete">
            <template #content>
                ¿Estás seguro de eliminar permanentemente al personal <strong>{{ personalToDelete?.nombre }} {{
                    personalToDelete?.apellido }}</strong>?
                <div class="alert alert-warning mt-3">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Esta acción no se puede deshacer y eliminará todos los datos asociados.
                </div>
            </template>
        </ModalBase>

        <!-- Modal para habilitar/editar módulos -->
        <ModalBase :visible="showModulosModal" :mode="modalMode === 'habilitar' ? 'create' : 'edit'"
            :entityName="modalMode === 'habilitar' ? 'acceso' : 'módulos'"
            :confirm-text="isProcessingModulos ? 'Procesando...' : (modalMode === 'habilitar' ? 'Habilitar' : 'Actualizar')"
            :loading="isProcessingModulos" @close="closeModulosModal" @confirm="confirmarAccionModulos"
            :width="'600px'">

            <template #content>
                <div class="modulos-selection">
                    <h6>Seleccionar módulos para {{ selectedPerson?.nombre }} {{ selectedPerson?.apellido }}:</h6>
                    <div class="modulos-list" style="max-height: 300px; overflow-y: auto;">
                        <!-- Spinner de carga cuando se están cargando los módulos -->
                        <div v-if="personalStore.loading" class="text-center py-4">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Cargando módulos...</span>
                            </div>
                            <p class="mt-2 text-muted">Cargando módulos...</p>
                        </div>

                        <!-- Lista de módulos cuando ya están cargados -->
                        <div v-else>
                            <div v-for="modulo in personalStore.modulos" :key="modulo.id" class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" :id="'modulo-' + modulo.id"
                                    :value="modulo.id" v-model="selectedModulos" :disabled="isProcessingModulos">
                                <label class="form-check-label" :for="'modulo-' + modulo.id">
                                    <strong>{{ modulo.name || modulo.codename }}</strong> - {{ modulo.description }}
                                </label>
                            </div>

                            <div v-if="personalStore.modulos.length === 0" class="text-center py-3 text-muted">
                                No hay módulos disponibles
                            </div>
                        </div>
                    </div>

                    <div v-if="selectedModulos.length === 0 && !personalStore.loading" class="alert alert-info mt-3">
                        <i class="pi pi-info-circle me-2"></i>
                        Debe seleccionar al menos un módulo
                    </div>
                </div>
            </template>
        </ModalBase>

        <!-- Listado de personal -->
        <DataTableWrapper :data="personalStore.personal" :columns="columns" :loading="personalStore.loading"
            :actions="true" :showCreateButton="true" title="GESTIÓN DE PERSONAL" createButtonLabel="Nuevo Personal"
            createButtonIcon="pi pi-user" :expandable="true" @create="openCreateModal"
            @column-filter-change="handleFilterChange">

            <template #body-dni="{ data }">
                {{ data.dni || '-' }}
            </template>
            <template #body-ruc="{ data }">
                {{ data.ruc || '-' }}
            </template>
            <template #body-full_name="{ data }">
                {{ data.full_name || '-' }}
            </template>
            <template #body-sexo="{ data }">
                <div class="sexo-container">
                    <span v-if="!data.sexo">-</span>
                    <div v-else class="sexo-content">
                        <i v-if="data.sexo === 'M'" class="pi pi-mars"
                            style="color: #007bff;font-size: 0.7rem;margin-right: 5px;" title="Masculino"></i>
                        <i v-else-if="data.sexo === 'F'" class="pi pi-venus"
                            style="color: #e83e8c;font-size: 0.7rem;margin-right: 5px;" title="Femenino"></i>
                        <span class="sexo-text">{{ data.sexo }}</span>
                    </div>
                </div>
            </template>
            <template #body-fecha_nac="{ data }">
                <div>
                    {{ data.fecha_nac || '-' }}
                    <span v-if="data.edad" style="font-size:0.7rem;color: #666; margin-left: 5px;">
                        ({{ data.edad }} años)
                    </span>
                </div>
            </template>
            <template #body-celular="{ data }">
                <div class="celular-container">
                    <a v-if="data.celular" :href="`https://wa.me/51${data.celular}`" target="_blank"
                        class="whatsapp-link" title="Enviar mensaje por WhatsApp">
                        <i class="pi pi-whatsapp" style="color: #25D366; margin-right: 5px;"></i>
                    </a>
                    <span class="numero">{{ data.celular || '-' }}</span>
                </div>
            </template>
            <template #body-email="{ data }">
                {{ data.email }}
            </template>
            <template #body-dependencia_nombre="{ data }">
                {{ data.dependencia_nombre || '-' }}
            </template>
            <template #body-area_nombre="{ data }">
                {{ data.area_nombre || '-' }}
            </template>
            <template #body-condicion_nombre="{ data }">
                {{ data.condicion_nombre || '-' }}
            </template>

            <template v-if="isSuperuser" #body-acceso="{ data }">
                <!-- Habilitado -->
                <Badge v-if="data.acceso === true" severity="success" class="p-2">
                    <i class="pi pi-check-circle"></i>
                </Badge>

                <!-- Deshabilitado -->
                <Badge v-else-if="data.acceso === false" severity="danger" class="p-2">
                    <i class="pi pi-times-circle"></i>
                </Badge>

                <!-- Vacío / nulo -->
                <Badge v-else severity="secondary" class="p-2">
                    <i class="pi pi-minus-circle"></i>
                </Badge>
            </template>

            <template #actions="{ data }">
                <div class="d-flex flex-wrap align-items-center justify-content-center gap-1">
                    <!-- Botón Habilitar/Editar Módulos (solo para superusuarios) -->
                    <Button v-if="isSuperuser && !data.acceso && data.email" icon="pi pi-key"
                        class="p-button-sm p-button-rounded p-button-primary" v-tooltip.top="'Habilitar acceso'"
                        @click="openModalHabilitar(data)" />

                    <Button v-if="isSuperuser && data.acceso" icon="pi pi-cog"
                        class="p-button-sm p-button-outlined p-button-rounded p-button-secondary"
                        v-tooltip.top="'Editar módulos'" @click="openModalEditarModulos(data)" />

                    <!-- Botón Deshabilitar Acceso (solo para superusuarios) -->
                    <Button v-if="isSuperuser && data.acceso" icon="pi pi-times"
                        class="p-button-sm p-button-outlined p-button-rounded p-button-warning"
                        v-tooltip.top="'Deshabilitar acceso'" @click="deshabilitarAcceso(data)" />

                    <!-- Botón Resetear Password (solo para superusuarios) -->
                    <Button v-if="isSuperuser && data.acceso" icon="pi pi-key"
                        class="p-button-sm p-button-outlined p-button-rounded p-button-info"
                        v-tooltip.top="'Resetear contraseña'" @click="resetearPassword(data)" />

                    <!-- Botones para todos los usuarios -->
                    <Button icon="pi pi-pencil" class="p-button-sm p-button-outlined p-button-rounded p-button-warning"
                        v-tooltip.top="'Editar'" @click="openEditModal(data)" />

                    <Button icon="pi pi-trash" class="p-button-sm p-button-outlined p-button-rounded p-button-danger"
                        v-tooltip.top="'Eliminar'" @click="confirmDelete(data)" />
                </div>
            </template>

            <template #expansion="{ data }">
                <div class="expansion-content p-4">
                    <div class="row">
                        <!-- Columna 1:  Información Laboral -->
                        <div class="col-5">
                            <div class="expansion-card p-3 h-100">
                                <div class="d-flex align-items-center mb-3">
                                    <i class="pi pi-user text-primary me-2" style="font-size: 1.35rem;"></i>
                                    <h6 class="m-0 text-900 fw-semibold">Información Laboral</h6>
                                </div>

                                <div class="row">
                                    <!-- Columna 1: Información básica del contrato -->
                                    <div class="col-12 col-md-4">
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">N° Contrato</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.n_contrato || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Fecha Inicio</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.fecha_inicio || '-' }}</p>
                                            <small class="m-0 text-500 fw-medium time-with-underline">
                                                ({{ calculateTimeWorked(data.fecha_inicio) }})
                                            </small>

                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Fecha Fin</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.fecha_fin || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Salario</label>
                                            <p class="m-0 text-900 fw-medium">{{ formatCurrency(data.salario || '-') }}
                                            </p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Anexo</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.anexo_number || '-' }}</p>
                                        </div>
                                    </div>

                                    <!-- Columna 2: Información de puesto y categoría -->
                                    <div class="col-12 col-md-4">
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Cargo</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.cargo_nombre || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Condición</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.condicion_nombre || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Estado</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.estado_nombre || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Régimen</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.regimen_nombre || '-' }}</p>
                                        </div>
                                    </div>

                                    <!-- Columna 3: Información de clasificación laboral -->
                                    <div class="col-12 col-md-4">
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Nivel</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.nivel_name || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Grupo Ocupacional</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.grupoo_cupacional_nombre || '-' }}
                                            </p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Genérica</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.generica_nombre || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Profesión</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.profesion_nombre || '-' }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Columna 2: Información del sistema -->
                        <div class="col-12 col-md-5 col-lg-5">
                            <div class="expansion-card p-3 h-100">
                                <div class="d-flex align-items-center mb-3">
                                    <i class="pi pi-cog text-primary me-2" style="font-size: 1.35rem;"></i>
                                    <h6 class="m-0 text-900 fw-semibold">Información adicional</h6>
                                </div>
                                <div class="row">
                                    <!-- Dirección ocupa toda la primera fila -->
                                    <div class="col-12">
                                        <div class="field mb-3">
                                            <label class="text-600 small fw-medium">Dirección</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.direccion || '-' }}</p>
                                        </div>
                                    </div>

                                    <!-- Campos restantes en 2 columnas -->
                                    <div class="col-12 col-md-6">
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Distrito</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.distrito || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Telefono</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.telefono || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Es Padre / Madre</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.padre_madre || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">N° Hijos</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.n_hijos || '-' }}</p>
                                        </div>
                                    </div>
                                    <div class="col-12 col-md-6">
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Email Personal</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.email_per || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">Contacto Emergencia</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.cont_emergencia || '-' }}</p>
                                        </div>
                                        <div class="field mb-1">
                                            <label class="text-600 small fw-medium">N° Celular</label>
                                            <p class="m-0 text-900 fw-medium">{{ data.cel_emergencia || '-' }}</p>
                                        </div>
                                        <!-- Eliminé los campos duplicados de N° Hijos -->
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Columna 3: Grupos -->
                        <div class="col-12 col-md-2 col-lg-2">
                            <div class="expansion-card p-3 h-100">
                                <div class="d-flex align-items-center mb-3">
                                    <i class="pi pi-users text-primary me-2" style="font-size: 1.35rem;"></i>
                                    <h6 class="m-0 text-900 fw-semibold">Otros</h6>
                                </div>
                                <div class="field mb-1">
                                    <label class="text-600 small fw-medium">Creado por</label>
                                    <p class="m-0 text-900 fw-medium">{{ data.created_by_username || '-' }}</p>
                                </div>
                                <!-- Campos que solo verá el superusuario -->
                                <template v-if="isSuperuser">
                                    <div class="field mb-1">
                                        <label class="text-600 small fw-medium">Habilitado por</label>
                                        <p class="m-0 text-900 fw-medium">{{ data.habilitado_por || '-' }}</p>
                                    </div>
                                    <div class="field mb-1">
                                        <label class="text-600 small fw-medium">Acceso</label>
                                        <p class="m-0 text-900 fw-medium">{{ data.fecha_habilitacion_acceso || '-' }}
                                        </p>
                                    </div>
                                </template>

                            </div>
                        </div>
                    </div>
                </div>
            </template>
        </DataTableWrapper>

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
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import DataTableWrapper from '@/components/ui/DataTableWrapper.vue';
import { usePersonalStore } from '@/stores/dgos/personalStore';
import FloatInput from '@/components/widgets/FloatInput.vue';
import ModalBase from '@/components/ui/ModalBase.vue';
import DatePicker from 'primevue/datepicker';
import { useRouter } from 'vue-router'
import { api } from "@/components/services/Axios"
import { useToast } from 'primevue/usetoast';
import { calculateTimeWorked, formatCurrency, onlyNumbersDNI, onlyNumbersRUC, onlyNumbersCelular, onlyNumbersTelefono, formatDateToISO, parseDateFromISO } from "@/components/utils/format";
import { distritosLima } from "@/components/utils/distritos";

const personalStore = usePersonalStore();
const toast = useToast();
const router = useRouter();

const errors = ref({});
const showModal = ref(false);
const showDeleteModal = ref(false);
const showModulosModal = ref(false);
const editing = ref(false);
const isSubmitting = ref(false);
const personalToDelete = ref(null);
const personalToEdit = ref(null);
const isDeleting = ref(false);
const selectedDependencia = ref(null);
const selectedPerson = ref(null);
const selectedModulos = ref([]);
const modalMode = ref('habilitar');
const message = ref('');
const messageType = ref('info');

const anexoOptions = ref([]); // Array vacío inicial
const condicionOptions = ref([]); // Array vacío inicial
const nivelOptions = ref([]); // Array vacío inicial
const dependenciasOptions = ref([]);
const areasOptions = ref([]);
const profesionOptions = ref([]);
const cargoOptions = ref([]);
const regimenOptions = ref([]);
const grupoOcupacionalOptions = ref([]);
const estadoOptions = ref([]);
const genericaOptions = ref([]);


const dependenciaOptions = computed(() => {
    return [...new Set(personalStore.personal.map(p => p.dependencia_nombre))].filter(Boolean);
});

const isSuperuser = computed(() => {
    return localStorage.getItem('is_superuser') === 'true'
})

const areaOptions = computed(() => {
    if (!selectedDependencia.value) {
        return [...new Set(personalStore.personal.map(p => p.area_nombre))].filter(Boolean);
    }

    return personalStore.personal
        .filter(p => p.dependencia_nombre === selectedDependencia.value)
        .map(p => p.area_nombre)
        .filter((v, i, a) => a.indexOf(v) === i && v !== null);
});

// Definimos la estructura del formulario como constante
const FORM_STATE = {
    dni: '',
    ruc: '',
    nombre: '',
    apellido: '',
    email: '',
    dependencia: '',
    area: '',
    profesion: '',
    cargo: '',
    regimen: '',
    grupo_ocupacional: '',
    estado: '',
    generica: '',
    fecha_nac: '',
    fecha_inicio: '',
    salario: '',
    sexo: '',
    is_active: true,
    padre_madre: '', // Añadido
    n_hijos: ''      // Añadido
};

// Usamos la estructura para el formulario reactivo
const form = ref({ ...FORM_STATE });

// Columnas con filtros dependientes
const columns = ref([
    { field: 'dni', header: 'DNI', bodyTemplate: true, filter: false,sortable: true, },
    { field: 'ruc', header: 'RUC', bodyTemplate: true, filter: false },
    { field: 'full_name', header: 'NOMBRE COMPLETO', sortable: true, bodyTemplate: true, filter: false },
    { field: 'sexo', header: 'GÉNERO', sortable: true, bodyTemplate: true, filter: false },
    { field: 'fecha_nac', header: 'F.NACIMIENTO', sortable: true, bodyTemplate: true, filter: false },
    { field: 'celular', header: 'CELULAR', sortable: false, bodyTemplate: true, filter: false },
    { field: 'email', header: 'EMAIL', sortable: false, bodyTemplate: true, filter: false },
    {
        field: 'dependencia_nombre',
        header: 'DEPENDENCIA',
        sortable: true,
        bodyTemplate: true,
        filter: true,
        filterOptions: dependenciaOptions
    },
    {
        field: 'area_nombre',
        header: 'AREA',
        sortable: true,
        bodyTemplate: true,
        filter: true,
        filterOptions: areaOptions
    },
    {
        field: 'condicion_nombre', header: 'CONDICIÓN', sortable: false, bodyTemplate: true, filter: true, filterOptions: computed(() =>
            personalStore.personal.map(u => u.condicion_nombre).filter((v, i, a) => a.indexOf(v) === i)
        ),
    },
]);

// Opciones para el dropdown de sexo
const sexoOptions = ref([
    { value: 'M', label: 'Masculino' },
    { value: 'F', label: 'Femenino' }
]);
const opcionesSiNo = ref([
    { value: 'Si', label: 'Sí' },
    { value: 'No', label: 'No' }
]);
// Opciones para el dropdown de número de hijos (1-6)
const hijosOptions = ref([
    { value: '1', label: '1 hijo' },
    { value: '2', label: '2 hijos' },
    { value: '3', label: '3 hijos' },
    { value: '4', label: '4 hijos' },
    { value: '5', label: '5 hijos' },
    { value: '6', label: '6 hijos' }
]);

// Función para manejar el cambio en "Es Padre/Madre"
const handlePadreMadreChange = (event) => {
    // Si no es padre/madre, limpiar el número de hijos
    if (form.value.padre_madre !== 'Si') {
        form.value.n_hijos = '';
    }
};
// Manejar cambios de filtro
const handleFilterChange = (event) => {
    if (event.field === 'dependencia_nombre') {
        selectedDependencia.value = event.value;
        personalStore.setSelectedDependencia(event.value);
    }
};
// Función para formatear el salario
const formatSalario = (event) => {
    let input = event.target.value;

    // Eliminar todos los caracteres no numéricos excepto el punto decimal
    let numericValue = input.replace(/[^\d.]/g, '');

    // Eliminar puntos decimales adicionales
    const decimalParts = numericValue.split('.');
    if (decimalParts.length > 2) {
        numericValue = decimalParts[0] + '.' + decimalParts.slice(1).join('');
    }

    // Limitar a dos decimales
    if (decimalParts.length === 2) {
        numericValue = decimalParts[0] + '.' + decimalParts[1].slice(0, 2);
    }

    // Formatear con separadores de miles
    if (numericValue) {
        const parts = numericValue.split('.');
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        numericValue = parts.join('.');
    }

    // Actualizar el valor en el formulario (sin el símbolo de moneda)
    form.value.salario = numericValue;
};

// También necesitamos una función para convertir el valor formateado a número antes de enviarlo
const getUnformattedSalario = () => {
    if (!form.value.salario) return null;
    return parseFloat(form.value.salario.replace(/,/g, ''));
};

// Métodos
const resetForm = () => {
    form.value = { ...FORM_STATE };
    errors.value = {};
};

const openCreateModal = () => {
    resetForm();
    editing.value = false;
    showModal.value = true;
};

const closeModal = () => {
    showModal.value = false;
    resetForm();
};

const confirmDelete = (user) => {
    personalToDelete.value = user;
    showDeleteModal.value = true;
};

const closeDeleteModal = () => {
    showDeleteModal.value = false;
    personalToDelete.value = null;
};

const openEditModal = async (personal) => {
    try {
        editing.value = true;
        personalToEdit.value = personal;

        // Resetear formulario primero
        resetForm();
        // Llenar el formulario con los datos del personal
        form.value = {
            ...personal,

            fecha_nac: parseDateFromISO(personal.fecha_nac),
            fecha_inicio: parseDateFromISO(personal.fecha_inicio),
            fecha_fin: parseDateFromISO(personal.fecha_fin),
            dependencia: personal.dependencia?.id || personal.dependencia,
            area: personal.area?.id || personal.area,
            anexo: personal.anexo?.id || personal.anexo,
            condicion: personal.condicion?.id || personal.condicion,
            nivel: personal.nivel?.id || personal.nivel,
            profesion: personal.profesion?.id || personal.profesion, // Corregí
            cargo: personal.cargo?.id || personal.cargo,             // Corregí
            regimen: personal.regimen?.id || personal.regimen,
            grupo_ocupacional: personal.grupo_ocupacional?.id || personal.grupo_ocupacional,
            estado: personal.estado?.id || personal.estado,
            generica: personal.generica?.id || personal.generica
        };

        console.log('Datos del formulario:', form.value);

        // Si hay dependencia, cargar sus áreas
        if (form.value.dependencia) {
            try {
                console.log('Cargando áreas para dependencia ID:', form.value.dependencia);
                const areasData = await personalStore.ListAreasByDependencia(form.value.dependencia);
                console.log('Áreas cargadas:', areasData);
                areasOptions.value = areasData;

                // Esperar a que el DOM se actualice
                await nextTick();
            } catch (error) {
                console.error('Error loading areas for edit:', error);
                areasOptions.value = [];
            }
        }

        showModal.value = true;

    } catch (error) {
        console.error('Error al abrir modal de edición:', error);
        toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo cargar la información para editar', life: 3000 });
    }
};
const proceedDelete = async () => {
    isDeleting.value = true;
    try {
        const success = await personalStore.DeletePersonal(personalToDelete.value.id);
        if (success) {
            closeDeleteModal();
        }
    } catch (error) {
        console.error('Error al eliminar:', error);
    } finally {
        isDeleting.value = false;
    }
};

const handleSubmit = async () => {
    isSubmitting.value = true;
    errors.value = {};

    try {
        // Crear copia del formulario con el salario sin formato
        const submitData = {
            ...form.value,
            salario: getUnformattedSalario(),
            fecha_nac: formatDateToISO(form.value.fecha_nac),
            fecha_inicio: formatDateToISO(form.value.fecha_inicio),
            fecha_fin: formatDateToISO(form.value.fecha_fin),
// Asegurar que los IDs sean números
            dependencia: form.value.dependencia ? parseInt(form.value.dependencia) : null,
            area: form.value.area ? parseInt(form.value.area) : null,
            condicion: form.value.condicion ? parseInt(form.value.condicion) : null,
            nivel: form.value.nivel ? parseInt(form.value.nivel) : null,
            profesion: form.value.profesion ? parseInt(form.value.profesion) : null,
            cargo: form.value.cargo ? parseInt(form.value.cargo) : null,
            regimen: form.value.regimen ? parseInt(form.value.regimen) : null,
            grupo_ocupacional: form.value.grupo_ocupacional ? parseInt(form.value.grupo_ocupacional) : null,
            estado: form.value.estado ? parseInt(form.value.estado) : null,
            generica: form.value.generica ? parseInt(form.value.generica) : null,
            
            // Campos numéricos
            dni: form.value.dni ? parseInt(form.value.dni.replace(/\D/g, '')) : null,
            ruc: form.value.ruc ? parseInt(form.value.ruc.replace(/\D/g, '')) : null,
            n_hijos: form.value.n_hijos ? parseInt(form.value.n_hijos) : null,
            celular: form.value.celular ? parseInt(form.value.celular.replace(/\D/g, '')) : null,
            telefono: form.value.telefono ? parseInt(form.value.telefono.replace(/\D/g, '')) : null,
            cel_emergencia: form.value.cel_emergencia ? parseInt(form.value.cel_emergencia.replace(/\D/g, '')) : null
        };

        console.log('Datos a enviar:', submitData);

        if (editing.value) {
            await personalStore.UpdatePersonal(personalToEdit.value.id, submitData);
        } else {
            await personalStore.CreatePersonal(submitData);
        }
        closeModal();
    } catch (error) {
        if (error.response?.data) {
            errors.value = error.response.data;
        } else {
            console.error('Error al guardar:', error);
        }
    } finally {
        isSubmitting.value = false;
    }
};

// Métodos para gestión de módulos
const openModalHabilitar = (person) => {
    selectedPerson.value = person;
    selectedModulos.value = [];
    modalMode.value = 'habilitar';
    showModulosModal.value = true;
};

const openModalEditarModulos = (person) => {
    selectedPerson.value = person;
    modalMode.value = 'editar';

    // Pre-seleccionar los módulos actuales del usuario
    if (person.user && person.user.modulos) {
        selectedModulos.value = person.user.modulos.map(modulo => modulo.id);
    } else {
        selectedModulos.value = [];
    }

    showModulosModal.value = true;
};

const closeModulosModal = () => {
    showModulosModal.value = false;
    selectedPerson.value = null;
    selectedModulos.value = [];
};

const confirmarAccionModulos = async () => {
    if (!selectedPerson.value || selectedModulos.value.length === 0) return;

    try {
        await personalStore.gestionarModulos(
            selectedPerson.value.id,
            selectedModulos.value,
            modalMode.value
        );

        closeModulosModal();
    } catch (error) {
        console.error('Error gestionando módulos:', error);
    }
};

const deshabilitarAcceso = async (person) => {
    if (!confirm(`¿Deshabilitar acceso a ${person.nombre} ${person.apellido}?`)) {
        return;
    }

    try {
        await personalStore.deshabilitarAcceso(person);
    } catch (error) {
        console.error('Error al deshabilitar acceso:', error);
    }
};

const resetearPassword = async (person) => {
    if (!confirm(`¿Resetear contraseña de ${person.nombre} ${person.apellido}?`)) {
        return;
    }

    try {
        await personalStore.resetearPassword(person);
    } catch (error) {
        console.error('Error al resetear contraseña:', error);
    }
};

onMounted(async () => {
    try {
        await personalStore.ListPersonal();
        await personalStore.ListModulos();

        // Cargar anexos
        const anexosData = await personalStore.ListAnexos();
        anexoOptions.value = anexosData;

        // Cargar condicion
        const condicionData = await personalStore.ListCondicion();
        condicionOptions.value = condicionData;

        // Cargar nivel
        const nivelData = await personalStore.ListNivel();
        nivelOptions.value = nivelData;

        // Cargar dependencias
        const dependenciasData = await personalStore.ListDependencias();
        dependenciasOptions.value = dependenciasData;

        // Cargar profesion
        const profesionData = await personalStore.ListProfesion();
        profesionOptions.value = profesionData;

        // Cargar cargo
        const cargoData = await personalStore.ListCargo();
        cargoOptions.value = cargoData;

        // Cargar regimen
        const regimenData = await personalStore.ListRegimen();
        regimenOptions.value = regimenData;

        // Cargar regimen
        const grupoOcupacionalData = await personalStore.ListGrupoOcupacional();
        grupoOcupacionalOptions.value = grupoOcupacionalData;

        // Cargar regimen
        const estadoData = await personalStore.ListEstado();
        estadoOptions.value = estadoData;

        // Cargar regimen
        const genericaData = await personalStore.ListGenerica();
        genericaOptions.value = genericaData;
    } catch (error) {
        console.error('Error loading data:', error);
    }
});

watch(() => form.value.dependencia, async (newDependencia) => {
    // Obtener el ID (puede ser un objeto o un ID directo)
    const dependenciaId = newDependencia?.id || newDependencia;

    console.log('Dependencia cambiada:', dependenciaId);

    if (dependenciaId) {
        try {
            // Cargar áreas filtradas por dependencia
            const areasData = await personalStore.ListAreasByDependencia(dependenciaId);
            console.log('Áreas cargadas para dependencia:', areasData);
            areasOptions.value = areasData;

            // Si estamos editando y el área actual pertenece a esta dependencia, mantenerla
            if (editing.value && form.value.area) {
                const areaExists = areasData.some(area =>
                    area.id == form.value.area || area.id.toString() === form.value.area.toString()
                );

                if (!areaExists) {
                    console.log('El área actual no pertenece a la nueva dependencia, limpiando...');
                    form.value.area = '';
                }
            }
        } catch (error) {
            console.error('Error loading areas:', error);
            areasOptions.value = [];
            form.value.area = '';
        }
    } else {
        console.log('No hay dependencia seleccionada, limpiando áreas');
        areasOptions.value = [];
        form.value.area = '';
    }
}, { immediate: false });

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

.modulos-list {
    border: 1px solid #dee2e6;
    border-radius: 5px;
    padding: 10px;
}

.expansion-content {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 12px;
}

.expansion-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border: 1px solid #e5e7eb;
    height: 100%;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.expansion-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3B82F6, #6366F1);
}

.expansion-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.custom-tag {
    border-radius: 20px;
    font-weight: 600;
    padding: 0.35rem 0.75rem;
    font-size: 0.85rem;
}

.custom-chip {
    background: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%);
    color: white;
    border-radius: 20px;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 0.5rem 0.75rem;
}

.field {
    margin-bottom: 1.2rem;
    padding: 0.5rem 0;
}

.field:last-child {
    margin-bottom: 0;
}

.text-xl {
    font-size: 1.35rem;
}

.font-semibold {
    font-weight: 600;
    color: #1f2937;
}

.h-full {
    height: 100%;
    display: flex;
    flex-direction: column;
}

.expansion-card .field label {
    display: block;
    margin-bottom: 0.35rem;
    color: #6b7280;
    font-weight: 500;
    font-size: 0.9rem;
}

.expansion-card .field p {
    color: #374151;
    font-weight: 500;
    font-size: 0.95rem;
    line-height: 1.4;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .expansion-card {
        margin-bottom: 1rem;
    }

    .expansion-card:last-child {
        margin-bottom: 0;
    }
}

.time-with-underline {
    font-size: 0.7rem;
    border-bottom: 1.5px solid #3B82F6;
    padding-bottom: 1px;
    display: inline-block;
    transition: all 0.2s ease;
}

.time-with-underline:hover {
    border-bottom: 2px solid #2563EB;
    /* Azul más oscuro al pasar el mouse */
    color: #2563EB !important;
}

small {
    color: #6B7B90;
}
</style>