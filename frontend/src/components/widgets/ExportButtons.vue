<template>
  <div class="d-flex justify-content-start mt-3">
    <button @click="exportToPDF" class="btn btn-danger me-2 mb-2">
      <i class="fas fa-file-pdf"></i> PDF
    </button>
    <button @click="exportToExcel" class="btn btn-success me-2 mb-2">
      <i class="fas fa-file-excel"></i> Excel
    </button>
    <button @click="exportToCSV" class="btn btn-warning mb-2">
      <i class="fas fa-file-csv"></i> CSV
    </button>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import * as XLSX from 'xlsx';  // Importa la biblioteca xlsx

const props = defineProps({
  pdfTitle: {
    type: String,
    default: 'Reporte'
  }
});

const exportToPDF = async () => {
  const input = document.querySelector('.table2');
  if (!input) return;

  try {
    const canvas = await html2canvas(input);
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF();
    const imgWidth = 190;
    const pageHeight = 295;
    const imgHeight = canvas.height * imgWidth / canvas.width;
    let heightLeft = imgHeight;

    pdf.text(props.pdfTitle, 10, 10);
    pdf.addImage(imgData, 'PNG', 10, 20, imgWidth, imgHeight);
    heightLeft -= pageHeight;

    while (heightLeft >= 0) {
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 10, -heightLeft + 20, imgWidth, imgHeight);
      heightLeft -= pageHeight;
    }

    pdf.save('reporte.pdf');
  } catch (error) {
    console.error('Error al exportar a PDF:', error);
  }
};

const exportToExcel = () => {
  const table = document.querySelector('.table');
  if (!table) return;

  try {
    // Convertir la tabla a un libro de trabajo
    const workbook = XLSX.utils.table_to_book(table, { sheet: 'Sheet1' });

    // Obtener la hoja de trabajo
    const worksheet = workbook.Sheets['Sheet1'];

    // Ajustar el rango para omitir la primera columna
    const range = XLSX.utils.decode_range(worksheet['!ref']);
    const newRange = {
      s: { c: range.s.c + 1, r: range.s.r },
      e: { c: range.e.c, r: range.e.r }
    };
    worksheet['!ref'] = XLSX.utils.encode_range(newRange);

    // Guardar el libro de trabajo como un archivo Excel
    XLSX.writeFile(workbook, 'reporte.xlsx');
  } catch (error) {
    console.error('Error al exportar a Excel:', error);
  }
};

const exportToCSV = () => {
  const table = document.querySelector('.table');
  if (!table) return;

  try {
    // Convertir la tabla a un libro de trabajo
    const workbook = XLSX.utils.table_to_book(table, { sheet: 'Sheet1' });

    // Obtener la hoja de trabajo
    const worksheet = workbook.Sheets['Sheet1'];

    // Convertir la hoja de trabajo a CSV
    const csv = XLSX.utils.sheet_to_csv(worksheet);

    // Crear un enlace de descarga
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    if (link.download !== undefined) { // Solo si la propiedad download es compatible
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', 'reporte.csv');
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  } catch (error) {
    console.error('Error al exportar a CSV:', error);
  }
};
</script>

