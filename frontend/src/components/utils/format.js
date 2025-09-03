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
  // Verificar si el valor es null, undefined, vacío o no es un número válido
  if (value === null || value === undefined || value === '' || isNaN(Number(value))) {
    return '-';
  }
  
  return new Intl.NumberFormat('es-PE', {
    style: 'currency',
    currency: currency,
  }).format(value);
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

export const calculateTimeWorked = (startDate) => {
  if (!startDate) return '-';
  
  try {
    const start = new Date(startDate);
    const now = new Date();
    
    if (start > now) return 'Fecha futura';
    
    let years = now.getFullYear() - start.getFullYear();
    let months = now.getMonth() - start.getMonth();
    let days = now.getDate() - start.getDate();
    
    // Ajustar meses negativos
    if (months < 0) {
      years--;
      months += 12;
    }
    
    // Ajustar días negativos
    if (days < 0) {
      months--;
      // Obtener los días del mes anterior
      const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 0);
      days += lastMonth.getDate();
      
      // Si meses se volvió negativo
      if (months < 0) {
        years--;
        months += 12;
      }
    }
    
    let result = '';
    if (years > 0) result += `${years} año${years !== 1 ? 's' : ''} `;
    if (months > 0) result += `${months} mes${months !== 1 ? 'es' : ''} `;
    if (days > 0 || result === '') result += `${days} día${days !== 1 ? 's' : ''}`;
    
    return result.trim();
  } catch (error) {
    return '-';
  }
};

export const onlyNumbersTelefono = (event) => {
    let value = event.target.value;
    
    // Filtrar solo números y remover guiones existentes
    let numbersOnly = value.replace(/[^\d]/g, '');
    
    // Limitar a 7 dígitos (máximo para teléfono fijo)
    numbersOnly = numbersOnly.slice(0, 7);
    
    // Aplicar formato con guión
    let formattedValue = numbersOnly;
    if (numbersOnly.length > 3) {
        formattedValue = numbersOnly.slice(0, 3) + '-' + numbersOnly.slice(3);
    }
    
    // Actualizar el valor del input
    event.target.value = formattedValue;
    
    return formattedValue; // Retorna con guión
};

export const onlyNumbersSpaceHyphen = (event, maxLength = null) => {
    let value = event.target.value;
    
    // Filtrar solo números, espacios y guiones
    value = value.replace(/[^\d\s-]/g, '');
    
    // Limitar longitud si se especifica
    if (maxLength !== null) {
        value = value.slice(0, maxLength);
    }
    
    // Actualizar el valor del input
    event.target.value = value;
    
    return value;
};

export const onlyNumbers = (event, maxLength = null) => {
    let value = event.target.value;
    
    // Filtrar solo números
    value = value.replace(/[^\d]/g, '');
    
    // Limitar longitud si se especifica
    if (maxLength !== null) {
        value = value.slice(0, maxLength);
    }
    
    // Actualizar el valor del input
    event.target.value = value;
    
    return value;
};
export const onlyNumbersSpaceHyphenUnlimited = (event) => onlyNumbersSpaceHyphen(event);

// Para DNI (8 dígitos)
export const onlyNumbersDNI = (event) => onlyNumbers(event, 8);

// Para RUC (11 dígitos)
export const onlyNumbersRUC = (event) => onlyNumbers(event, 11);

// Para Celular (9 dígitos)
export const onlyNumbersCelular = (event) => onlyNumbers(event, 9);

// Para cualquier campo sin límite
export const onlyNumbersUnlimited = (event) => onlyNumbers(event);


// Función para formatear fecha a YYYY-MM-DD (sin problemas de zona horaria)
// En tu archivo de utils/format.js
export const formatDateToISO = (date) => {
    if (!date) return null;
    if (date instanceof Date) {
        return date.toISOString().split('T')[0];
    }
    return date;
};

export const parseDateFromISO = (dateString) => {
    if (!dateString) return null;
    
    // Crear fecha y ajustar por timezone offset
    const date = new Date(dateString);
    const timezoneOffset = date.getTimezoneOffset() * 60000; // minutos a milisegundos
    const adjustedDate = new Date(date.getTime() + timezoneOffset);
    
    return adjustedDate;
};