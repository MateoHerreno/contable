export function handleApiError(err, setError) {
  const msg = err?.response?.data?.detail || 'Error al procesar la solicitud.';
  setError(msg);
  setTimeout(() => setError(''), 6000);
}
