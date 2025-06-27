import axios from 'axios';
import { logoutUser } from './auth';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // o '/api/' si usas proxy
});

// ➤ Agrega el token de acceso en cada solicitud
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ➤ Si el token está expirado, intenta refrescarlo
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    // Si es 401 y no se ha intentado ya
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post('http://127.0.0.1:8000/api/refresh/', {
            refresh: refreshToken,
          });

          const newAccessToken = response.data.access;
          localStorage.setItem('access_token', newAccessToken);

          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return api(originalRequest);
        } catch (refreshError) {
          logoutUser(); // Si también falla el refresh, cerrar sesión
        }
      } else {
        logoutUser(); // No hay refresh token
      }
    }

    return Promise.reject(error);
  }
);

export default api;
