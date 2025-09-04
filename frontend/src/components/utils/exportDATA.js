import { api } from "@/components/services/Axios";
import { ref } from 'vue';

/**
 * Función reusable para exportar archivos Excel con fecha y hora de Lima
 */
export const exportToExcel = async (endpoint, defaultFileName = 'data.xlsx', successMessage = 'Archivo exportado correctamente', errorMessage = 'Error al exportar el archivo') => {
  try {
    const API_BASE_URL = import.meta.env.VITE_API_URL;
    const response = await api.get(`${API_BASE_URL}${endpoint}`, {
      responseType: 'blob',
    });

    // Crear objeto URL a partir del blob
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;

    // Obtener nombre del archivo desde el header o generar uno con fecha/hora Lima
    let fileName = defaultFileName;
    
    try {
      const disposition = response.headers['content-disposition'];
      if (disposition && disposition.includes('filename=')) {
        fileName = disposition.split('filename=')[1].split(';')[0].replace(/"/g, '');
      } else {
        // Generar nombre con fecha y hora de Lima si no viene en el header
        fileName = generateFileNameWithLimaTime(defaultFileName);
      }
    } catch (error) {
      console.warn('No se pudo obtener filename del header, generando nombre con fecha Lima');
      fileName = generateFileNameWithLimaTime(defaultFileName);
    }

    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);

    return { 
      success: true, 
      fileName,
      toast: {
        severity: 'success',
        summary: 'Éxito',
        detail: successMessage,
        life: 3000
      }
    };

  } catch (error) {
    console.error('Error en exportación:', error);
    
    return { 
      success: false, 
      error,
      toast: {
        severity: 'error',
        summary: 'Error',
        detail: errorMessage,
        life: 3000
      }
    };
  }
};

/**
 * Genera un nombre de archivo con timestamp de Lima
 */
const generateFileNameWithLimaTime = (baseName) => {
  const now = new Date();
  
  // Convertir a hora de Lima (UTC-5)
  const limaOffset = -5 * 60; // Lima está en UTC-5
  const localTime = now.getTime();
  const localOffset = now.getTimezoneOffset() * 60000;
  const utcTime = localTime + localOffset;
  const limaTime = utcTime + (limaOffset * 60000);
  
  const limaDate = new Date(limaTime);
  
  // Formato: nombre_YYYYMMDD_HHMMSS.xlsx
  const year = limaDate.getFullYear();
  const month = String(limaDate.getMonth() + 1).padStart(2, '0');
  const day = String(limaDate.getDate()).padStart(2, '0');
  const hours = String(limaDate.getHours()).padStart(2, '0');
  const minutes = String(limaDate.getMinutes()).padStart(2, '0');
  const seconds = String(limaDate.getSeconds()).padStart(2, '0');
  
  const base = baseName.replace('.xlsx', '');
  return `${base}_${year}${month}${day}_${hours}${minutes}${seconds}.xlsx`;
};

/**
 * Composable para exportar con loading state
 */
export const useExportWithLoading = () => {
  const exporting = ref(false);

  const executeExport = async (endpoint, defaultFileName, successMessage, errorMessage) => {
    exporting.value = true;
    try {
      const result = await exportToExcel(endpoint, defaultFileName, successMessage, errorMessage);
      return result;
    } finally {
      exporting.value = false;
    }
  };

  return { exporting, executeExport };
};