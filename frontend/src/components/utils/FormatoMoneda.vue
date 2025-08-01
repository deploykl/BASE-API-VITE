<template>
    <span>{{ formattedValue }}</span>
</template>

<script setup>
import { computed } from 'vue';
import { defineProps } from 'vue';

const props = defineProps({
    value: {
        type: Number,
        required: true,
    },
    currency: {
        type: String,
        default: 'PEN',
    },
});

// Formateo del valor para visualización
const formattedValue = computed(() => {
    return new Intl.NumberFormat('es-PE', {
        style: 'currency',
        currency: props.currency,
    }).format(props.value || 0);
});

// Formatea el valor de acuerdo al formato de moneda
const parseValue = (value) => {
    const numberValue = parseFloat(value.replace(/[^0-9.-]+/g, ""));
    return isNaN(numberValue) ? 0 : numberValue;
};

</script>

<style scoped>
/* Estilos opcionales para el componente */
</style>