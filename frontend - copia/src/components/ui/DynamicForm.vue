<template>
  <form @submit.prevent="$emit('submit')">
    <div class="row">
      <template v-for="(field, index) in fields" :key="index">
        <!-- Campo estándar -->
        <div v-if="!field.customComponent" :class="field.colClass">
          <!-- Campos de texto/email/password -->
          <FloatInput v-if="isInputField(field)" 
            :id="field.name"
            :label="field.label"
            v-model="formData[field.name]"
            :type="field.type"
            :icon="field.icon"
            :errors="errors"
            :invalid="!!errors[field.name]"
            size="small"
          />
          
          <!-- Selector -->
          <Dropdown v-else-if="field.type === 'select'"
            v-model="formData[field.name]"
            :options="field.options"
            optionLabel="label"
            optionValue="value"
            :placeholder="field.placeholder"
            class="w-full"
          />
          
          <!-- Switch -->
          <div v-else-if="field.type === 'switch'" class="form-check form-switch">
            <input v-model="formData[field.name]" type="checkbox" class="form-check-input" :id="field.name+'-switch'">
            <label class="form-check-label" :for="field.name+'-switch'">{{ field.label }}</label>
          </div>
        </div>
        
        <!-- Componente personalizado -->
        <div v-else :class="field.colClass">
          <ResetPasswordField 
            v-if="field.customComponent === 'ResetPassword'"
            v-model="resetPassword"
            @update:modelValue="val => resetPassword = val"
          />
        </div>
      </template>
    </div>
  </form>
</template>

<script setup>
defineProps({
  modelValue: Boolean
});

defineEmits(['update:modelValue']);
</script>