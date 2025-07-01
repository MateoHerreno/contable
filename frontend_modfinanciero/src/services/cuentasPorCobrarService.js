import { api } from './connection';

// CRUD de Cuentas por Cobrar
export const getCuentasPorCobrar = () => api.get('cxc/');
export const getCuentaPorCobrar = (id) => api.get(`cxc/${id}/`);
export const createCuentaPorCobrar = (data) => api.post('cxc/', data);
export const updateCuentaPorCobrar = (id, data) => api.patch(`cxc/${id}/`, data);
export const deleteCuentaPorCobrar = (id) => api.delete(`cxc/${id}/`);

// Conceptos (para select)
export const getConceptosCXC = () => api.get('conceptoscxc/');

// Nota de Crédito
export const crearNotaCredito = (data) => api.post('notacredito/', data);
export const getNotaCredito = (data) => api.get('notacredito/', data);
