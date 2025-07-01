import { api } from './connection';

// CRUD de Cuentas por Pagar
export const getCuentasPorPagar = () => api.get('cxp/');
export const getCuentaPorPagar = (id) => api.get(`cxp/${id}/`);
export const createCuentaPorPagar = (data) => api.post('cxp/', data);
export const updateCuentaPorPagar = (id, data) => api.patch(`cxp/${id}/`, data);
export const deleteCuentaPorPagar = (id) => api.delete(`cxp/${id}/`);

// Conceptos (para select)
export const getConceptosCXP = () => api.get('conceptoscxp/');
