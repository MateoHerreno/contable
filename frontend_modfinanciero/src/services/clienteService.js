
import { api } from './connection';

export const getClientes = () => api.get('clientes/');
export const getCliente = (id) => api.get(`clientes/${id}/`);
export const createCliente = (data) => api.post('clientes/', data);
export const updateCliente = (id, data) => api.patch(`clientes/${id}/`, data);
export const deleteCliente = (id) => api.delete(`clientes/${id}/`);
