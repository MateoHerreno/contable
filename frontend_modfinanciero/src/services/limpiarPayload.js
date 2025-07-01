export function limpiarPayload(obj) {
  const cleaned = {};

  for (const key in obj) {
    const value = obj[key];

    const isNotEmpty =
      value !== '' &&
      value !== null &&
      !(Array.isArray(value) && value.length === 0);

    if (isNotEmpty) {
      cleaned[key] = value;
    }
  }

  return cleaned;
}
