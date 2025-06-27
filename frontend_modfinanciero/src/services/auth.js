export function logoutUser(redirect = true) {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');

  if (redirect) {
    window.location.href = '/login';
  }
}