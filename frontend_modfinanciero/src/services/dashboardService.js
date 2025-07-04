import { api } from "../utils/connection";

// Resumen financiero del mes actual
export const getResumenDashboard = () => api.get('resumen/');

// Totales por concepto
export const getCXCConceptos = () => api.get('cxcconcepto/');
export const getCXPConceptos = () => api.get('cxpconcepto/');

// Evolución mensual CxC vs CxP
export const getEvolucionMensual = () => api.get('evolucionmensual/');

// Resumen de pagos
export const getCXCResumen = () => api.get('cxcresumen/');
export const getCXPResumen = () => api.get('cxpresumen/');