<template>
  <transition name="slide-down">
    <div v-if="errorStore.message" class="error-message" :class="errorStore.type">
      <div class="error-content">
        <i :class="iconClass"></i>
        <span>{{ errorStore.message }}</span>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'
import { useErrorStore } from '@/store/errorStore'

const errorStore = useErrorStore()

const iconClass = computed(() => {
  return {
    'error': 'fas fa-exclamation-circle',
    'warning': 'fas fa-exclamation-triangle',
    'success': 'fas fa-check-circle'
  }[errorStore.type]
})
</script>

<style scoped>
.error-message {
  width: 100%;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 0 0 20px 0;
  display: flex;
  justify-content: center;
  font-size: 14px;
  animation: fadeIn 0.3s ease-in-out;
}

.error-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.error-message.error {
  background-color: #ffebee;
  color: #c62828;
  border-left: 4px solid #c62828;
}

.error-message.warning {
  background-color: #fff8e1;
  color: #e65100;
  border-left: 4px solid #e65100;
}

.error-message.success {
  background-color: #e8f5e9;
  color: #2e7d32;
  border-left: 4px solid #2e7d32;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>