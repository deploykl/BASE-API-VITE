// En tu archivo src/utils/notifications.js
import { toast } from 'vue-sonner'

export const notify = {
  success: (message, options = {}) => toast.success(message, { duration: 3000, ...options }),
  error: (message, options = {}) => toast.error(message, { duration: 5000, ...options }),
  warning: (message, options = {}) => toast.warning(message, { duration: 4000, ...options }),
  info: (message, options = {}) => toast(message, { duration: 3000, ...options }),
  promise: (promiseFn, messages) => {
    return toast.promise(promiseFn, {
      loading: messages.loading || 'Loading...',
      success: (data) => messages.success(data) || 'Success!',
      error: (data) => messages.error(data) || 'Error occurred',
    });
  },
  confirm: (message, confirmAction, cancelAction, options = {}) => {
    const toastId = toast(
      `<div class="sonner-confirm">
        <h3 class="confirm-title">${message}</h3>
        <div class="confirm-buttons">
          <button class="confirm-button confirm-button-yes">Confirmar</button>
          <button class="confirm-button confirm-button-no">Cancelar</button>
        </div>
      </div>`,
      {
        duration: Infinity,
        ...options
      }
    )

    setTimeout(() => {
      const yesBtn = document.querySelector(`.confirm-button-yes[data-toast-id="${toastId}"]`)
      const noBtn = document.querySelector(`.confirm-button-no[data-toast-id="${toastId}"]`)
      
      if (yesBtn) yesBtn.onclick = () => { confirmAction?.(); toast.dismiss(toastId) }
      if (noBtn) noBtn.onclick = () => { cancelAction?.(); toast.dismiss(toastId) }
    }, 100)
  }
}