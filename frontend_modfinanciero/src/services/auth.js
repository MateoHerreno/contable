export function logoutUser(redirect = true) {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('access_rol');
  localStorage.removeItem('access_nombre');
  if (redirect) {
    window.location.href = '/login';
  }
}