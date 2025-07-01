import {api} from '../services/connection';

export const getTiendas = () => api.get('tiendas/');
export const createTienda = (data) => api.post('tiendas/', data);
export const updateTienda = (id, data) => api.patch(`tiendas/${id}/`, data);
export const deleteTienda = (id) => api.delete(`tiendas/${id}/`);
