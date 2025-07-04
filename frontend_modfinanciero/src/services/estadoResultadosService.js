import { api } from '../utils/connection';

export const postEstadoResultados = (data) => api.post('estres/', data);

export const postPDFEstadoResultados = (data) =>
  api.post('pdfestres/', data, { responseType: 'blob' });

export const postExcelEstadoResultados = (data) =>
  api.post('excelestres/', data, { responseType: 'blob' });
