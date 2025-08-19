import { useCustomToast } from "@/components/utils/toast";
import { watch } from 'vue';


export const copyToClipboard = async (text, showToast = true, toast = null) => {
  try {
    await navigator.clipboard.writeText(text);
    if (showToast && toast) {
      toast.showInfo('URL copiada al portapapeles', 'Copiado exitoso');
    }
    return true;
  } catch (err) {
    if (showToast && toast) {
      toast.showError('Error al copiar la URL');
    }
    return false;
  }
};

/**
 * Formatea una fecha según configuración
 * @param {string|Date} dateString - Fecha a formatear
 * @param {Object} options - Opciones adicionales para Intl.DateTimeFormat
 * @returns {string} - Fecha formateada o '-' si no válida
 */
export const formatDateTime = (dateString, options = {}) => {
  if (!dateString) return '-';
  try {
    const date = new Date(dateString);
    const defaultOptions = {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Intl.DateTimeFormat('es-PE', { ...defaultOptions, ...options }).format(date);
  } catch {
    return dateString;
  }
};
// Nueva función para formatear fechas para input datetime-local
export const formatDateTimeForInput = (dateString) => {
  if (!dateString) return '';
  try {
    const date = new Date(dateString);
    // Ajustar para el huso horario local
    const offset = date.getTimezoneOffset() * 60000;
    const localISOTime = new Date(date - offset).toISOString().slice(0, 16);
    return localISOTime;
  } catch {
    return dateString;
  }
};
/**
/**
 * Formatea un valor como moneda
 * @param {number} value - Valor numérico
 * @param {string} currency - Código de moneda (default: 'PEN')
 * @returns {string} - Valor formateado como moneda
 */
export const formatCurrency = (value, currency = 'PEN') => {
  return new Intl.NumberFormat('es-PE', {
    style: 'currency',
    currency: currency,
  }).format(value || 0);
};

/**
 * Parsea un string de moneda a número
 * @param {string} value - String con formato de moneda
 * @returns {number} - Valor numérico
 */
export const parseCurrency = (value) => {
  const numberValue = parseFloat(value.replace(/[^0-9.-]+/g, ""));
  return isNaN(numberValue) ? 0 : numberValue;
};