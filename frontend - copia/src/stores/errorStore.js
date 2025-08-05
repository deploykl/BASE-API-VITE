import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useErrorStore = defineStore('error', () => {
  const message = ref('')
  const type = ref('error')
  const timeout = ref(2500)
  const timer = ref(null)

  const showMessage = (msg, msgType = 'error', msgTimeout = 2500) => {
    clearTimeout(timer.value)
    message.value = msg
    type.value = msgType
    timeout.value = msgTimeout
    
    timer.value = setTimeout(() => {
      message.value = ''
    }, timeout.value)
  }

  const clearMessage = () => {
    clearTimeout(timer.value)
    message.value = ''
  }

  return { message, type, showMessage, clearMessage }
})