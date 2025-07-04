import { API_BASE_URL } from "./connection";
export const intentarRenovarToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  if (refreshToken) {
    try {
      const res = await fetch(`${API_BASE_URL}refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken }),
      });
      const data = await res.json();
      if (data.access) {
        localStorage.setItem('access_token', data.access);
        return true;
      }
    } catch (err) {
      console.error('Error actualizando token:', err);
    }
  }

  localStorage.clear();
  window.location.href = '/login';
  return false;
};
