<template>
    <div class="mb-5 position-relative">
        <FloatLabel :variant="variant">
            <InputText 
                :id="id" 
                v-model="inputValue" 
                :placeholder="placeholder"
                :class="['form-control', inputClass, { 'is-invalid': invalid || (required && !inputValue && showErrorMessage) || (errors && errors[id]) }]"
                :autocomplete="autocomplete"
                v-bind="$attrs" 
                @keypress="handleKeyPress" 
                @input="handleInput" 
            />
            <label :for="id" class="form-label">
                <i v-if="icon" :class="icon" class="me-2"></i>
                {{ label }}
                <span v-if="required" class="text-danger">*</span>
            </label>
        </FloatLabel>

        <div v-if="hint && !inputValue" class="form-text text-muted">
            {{ hint }}
        </div>

        <!-- Mostrar error del backend si existe, sino mostrar validación frontend -->
        <div v-if="(errors && errors[id]) || ((invalid || (required && !inputValue)) && showErrorMessage)" class="invalid-feedback">
            {{ (errors && errors[id]) || errorMessage || 'Este campo es obligatorio' }}
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    id: { type: String, required: true },
    label: { type: String, required: true },
    modelValue: { type: [String, Number], default: '' },
    variant: {
        type: String,
        default: 'outlined',
        validator: (value) => ['outlined', 'filled', 'standard'].includes(value)
    },
    invalid: { type: Boolean, default: false },
    required: { type: Boolean, default: false },
    autocomplete: { type: String, default: 'off' },
    inputClass: { type: [String, Array, Object], default: '' },
    icon: { type: String, default: '' },
    hint: { type: String, default: '' },
    placeholder: { type: String, default: '' },
    errorMessage: { type: String, default: '' }, // Añadido prop para mensaje de error
    validationType: {
        type: String,
        default: '',
        validator: (value) => ['', 'dni', 'phone', 'password'].includes(value)
    },
    showErrorMessage: {
        type: Boolean,
        default: true
    },
    errors: { type: Object, default: () => ({}) } // Asegurar que siempre es un objeto
});

const emit = defineEmits(['update:modelValue', 'blur']);

const inputValue = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
});

const handleKeyPress = (event) => {
    if (props.validationType === 'dni' || props.validationType === 'phone') {
        const keyCode = event.keyCode || event.which;
        const keyValue = String.fromCharCode(keyCode);
        const isValid = /^[0-9]*$/.test(keyValue);

        if (!isValid) {
            event.preventDefault();
        }
    }
};

const handleInput = (event) => {
    // Solo actualizamos el valor si no excede los límites
    if (props.validationType === 'dni' && event.target.value.length > 8) {
        inputValue.value = event.target.value.slice(0, 8);
    } else if (props.validationType === 'phone' && event.target.value.length > 9) {
        inputValue.value = event.target.value.slice(0, 9);
    } else {
        inputValue.value = event.target.value;
    }
};
</script>