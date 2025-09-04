import { api } from "@/components/services/Axios";
import { ref } from 'vue';

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
  
  // Obtener la extensión del archivo
  const extension = baseName.includes('.') ? baseName.split('.').pop() : '';
  const baseWithoutExtension = baseName.replace('.' + extension, '');
  
  // Formato: nombre_YYYYMMDD_HHMMSS.extensión
  const year = limaDate.getFullYear();
  const month = String(limaDate.getMonth() + 1).padStart(2, '0');
  const day = String(limaDate.getDate()).padStart(2, '0');
  const hours = String(limaDate.getHours()).padStart(2, '0');
  const minutes = String(limaDate.getMinutes()).padStart(2, '0');
  const seconds = String(limaDate.getSeconds()).padStart(2, '0');
  
  return `${baseWithoutExtension}_${year}${month}${day}_${hours}${minutes}${seconds}.${extension}`;
};

/**
 * Función reusable para exportar archivos (Excel, CSV, PDF)
 */
export const exportFile = async (endpoint, defaultFileName, successMessage, errorMessage) => {
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
 * Composable para exportar con loading state (CSV, PDF, Excel)
 */
export const useExportWithLoading = () => {
  const exporting = ref(false);

  const executeExport = async (endpoint, defaultFileName, successMessage, errorMessage) => {
    exporting.value = true;
    try {
      const result = await exportFile(endpoint, defaultFileName, successMessage, errorMessage);
      return result;
    } finally {
      exporting.value = false;
    }
  };

  return { exporting, executeExport };
};

// Ejemplo de uso en un componente Vue (esto sería parte de tu componente)
export const usePersonalExports = () => {
  const { exporting, executeExport } = useExportWithLoading();
  
  const exportExcel = async () => {
    const result = await executeExport(
      'componentes/personal/excel/',
      'personal.xlsx',
      'Personal exportado correctamente en Excel',
      'No se pudo exportar el personal en Excel'
    );

    if (result.toast) {
      // Asumiendo que tienes un sistema de toast disponible
      // toast.add(result.toast);
      console.log('Toast:', result.toast);
    }

    if (result.success) {
      console.log('Archivo descargado:', result.fileName);
    }
    
    return result;
  };

  const exportCSV = async () => {
    const result = await executeExport(
      'componentes/personal/csv/',
      'personal.csv',
      'Personal exportado correctamente en CSV',
      'No se pudo exportar el personal en CSV'
    );

    if (result.toast) {
      // toast.add(result.toast);
      console.log('Toast:', result.toast);
    }
    
    return result;
  };

  const exportPDF = async () => {
    const result = await executeExport(
      'componentes/personal/pdf/',
      'personal.pdf',
      'Personal exportado correctamente en PDF',
      'No se pudo exportar el personal en PDF'
    );

    if (result.toast) {
      // toast.add(result.toast);
      console.log('Toast:', result.toast);
    }
    
    return result;
  };

  return {
    exporting,
    exportExcel,
    exportCSV,
    exportPDF
  };
};

// Exportar todas las funciones por si se necesitan individualmente
export default {
  exportFile,
  useExportWithLoading,
  usePersonalExports,
  generateFileNameWithLimaTime
};