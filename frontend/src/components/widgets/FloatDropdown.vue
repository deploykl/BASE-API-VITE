<template>
    <div class="mb-3 position-relative">
        <!-- Label siempre arriba (sin FloatLabel) -->
        <label :for="id" class="form-label d-block mb-2">
            <i v-if="icon" :class="icon" class="me-2"></i>
            {{ label }}
            <span v-if="required" class="text-danger">*</span>
        </label>

        <Dropdown 
            :id="id" 
            v-model="inputValue" 
            :options="options" 
            :optionLabel="optionLabel" 
            :optionValue="optionValue" 
            :placeholder="placeholder" 
            :class="['w-100', { 'p-invalid': showError }]"
            :filter="filter" 
            :filterPlaceholder="filterPlaceholder"
            :disabled="disabled"
            :showClear="showClear"
            @change="handleChange"
            @blur="handleBlur">
            
            <!-- Slots para personalización -->
            <template v-if="$slots.option" #option="slotProps">
                <slot name="option" v-bind="slotProps"></slot>
            </template>
            
            <template v-if="$slots.value" #value="slotProps">
                <slot name="value" v-bind="slotProps"></slot>
            </template>
        </Dropdown>

        <!-- Mensaje de error -->
        <small v-if="showError" class="p-error mt-1 d-block">
            {{ errorText }}
        </small>

        <!-- Hint text -->
        <small v-if="hint && !inputValue" class="p-text-secondary mt-1 d-block">
            {{ hint }}
        </small>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    id: { type: String, required: true },
    label: { type: String, required: true },
    modelValue: { type: [String, Number, Object, Array], default: null },
    options: { type: Array, default: () => [] },
    optionLabel: { type: String, default: 'label' },
    optionValue: { type: String, default: 'value' },
    placeholder: { type: String, default: 'Seleccionar' },
    invalid: { type: Boolean, default: false },
    required: { type: Boolean, default: false },
    icon: { type: String, default: '' },
    errorMessage: { type: String, default: '' },
    errors: { type: Object, default: () => ({}) },
    filter: { type: Boolean, default: false },
    filterPlaceholder: { type: String, default: 'Buscar...' },
    disabled: { type: Boolean, default: false },
    showClear: { type: Boolean, default: false },
    hint: { type: String, default: '' },
    showErrorMessage: { type: Boolean, default: true }
});

const emit = defineEmits(['update:modelValue', 'change', 'blur']);

const inputValue = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
});

const showError = computed(() => {
    return props.invalid || 
           (props.required && !inputValue.value && props.showErrorMessage) ||
           (props.errors && props.errors[props.id]);
});

const errorText = computed(() => {
    if (props.errors && props.errors[props.id]) {
        return Array.isArray(props.errors[props.id])
            ? props.errors[props.id][0]
            : props.errors[props.id];
    }
    return props.errorMessage || 'Este campo es obligatorio';
});

const handleChange = (event) => {
    emit('change', event);
};

const handleBlur = () => {
    emit('blur');
};
</script>

<style scoped>
.position-relative {
    position: relative;
}

.mb-3 {
    margin-bottom: 1rem;
}

.mt-1 {
    margin-top: 0.25rem;
}

.d-block {
    display: block;
}

.form-label {
    font-weight: 500;
    color: #495057;
    font-size: 0.875rem;
}

/* Estilos para mantener consistencia con FloatInput */
:deep(.p-dropdown) {
    border-radius: 6px;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

:deep(.p-dropdown:not(.p-disabled):hover) {
    border-color: #6366f1;
}

:deep(.p-dropdown:not(.p-disabled).p-focus) {
    border-color: #6366f1;
    box-shadow: 0 0 0 0.2rem rgba(99, 102, 241, 0.2);
}

:deep(.p-dropdown.p-invalid) {
    border-color: #e24c4c;
}

:deep(.p-dropdown.p-invalid:not(.p-disabled):hover) {
    border-color: #e24c4c;
}

:deep(.p-dropdown.p-invalid:not(.p-disabled).p-focus) {
    border-color: #e24c4c;
    box-shadow: 0 0 0 0.2rem rgba(226, 76, 76, 0.2);
}
</style>