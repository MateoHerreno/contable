import axios from 'axios';

//  Centralizar la URL base de la API
export const API_BASE_URL = 'http://localhost:8000/api/';

//  Función para cerrar sesión local
export const logoutUser = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('access_nombre');
  localStorage.removeItem('access_rol');
  window.location.href = '/logout';
};

//  Instancia principal con token de acceso
export const api = axios.create({
  baseURL: API_BASE_URL,
});

//  Interceptor para agregar token en cada solicitud
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

//  Instancia separada sin interceptores para el refresh
const refreshInstance = axios.create({ baseURL: API_BASE_URL });

// 🧩 Interceptor de respuesta para manejar expiración del access_token
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await refreshInstance.post('refresh/', {
            refresh: refreshToken,
          });

          const newAccessToken = response.data.access;
          localStorage.setItem('access_token', newAccessToken);

          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return api(originalRequest); // reintenta con nuevo token
        } catch (refreshError) {
          logoutUser(); // refresh también falló
        }
      } else {
        logoutUser(); // sin refresh disponible
      }
    }

    return Promise.reject(error);
  }
);
