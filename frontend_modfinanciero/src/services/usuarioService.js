import {api} from './connection';

export const getUsuarios = () => api.get('usuarios/');
export const getUsuario = (id) => api.get(`usuarios/${id}/`);
export const createUsuario = (data) => api.post('usuarios/', data);
export const updateUsuario = (id, data) => api.patch(`usuarios/${id}/`, data);
export const deleteUsuario = (id) => api.delete(`usuarios/${id}/`);
