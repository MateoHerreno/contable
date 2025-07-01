import {api} from './connection'

export const getEmpresas = () => api.get('empresas/');
export const createEmpresa = (data) => api.post('empresas/', data);
export const updateEmpresa = (id, data) => api.patch(`empresas/${id}/`, data);
export const deleteEmpresa = (id) => api.delete(`empresas/${id}/`);
