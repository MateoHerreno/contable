import { api } from './connection';

export const postEstadoResultados = (data) => api.post('estres/', data);