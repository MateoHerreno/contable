import { Routes, Route, Navigate } from 'react-router-dom';

// Vistas
import Login from '../views/Login/Login';
import RecuperarPassword from '../views/Password/RecuperarPassword';
import RestablecerPassword from '../views/Password/RestablecerPassword';

// Rutas protegidas
import Dashboard from '../views/Dashboards/Dashboard';
import CuentasPorCobrar from '../views/CXC/CuentasPorCobrar';
import CuentasPorPagar from '../views/CXP/CuentasPorPagar';
import Clientes from '../views/Clientes/Clientes';
import Proveedores from '../views/Proveedores/Proveedores';
import Usuarios from '../views/Usuarios/Usuarios';
import Tiendas from '../views/Tiendas/Tiendas';
import EstadoResultados from '../views/EstadoResultados/EstadoResultados';

// Layout protegido
import ProtectedLayout from '../components/ProtectedLayout';

export default function AppRoutes() {
  return (
    <Routes>
      {/* Redirección por defecto */}
      <Route path="/" element={<Navigate to="/login" />} />

      {/* Rutas públicas */}
      <Route path="/login" element={<Login />} />
      <Route path="/recuperar" element={<RecuperarPassword />} />
      <Route path="/restablecer" element={<RestablecerPassword />} />

      {/* Rutas protegidas (dentro del layout) */}
      <Route element={<ProtectedLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/cxc" element={<CuentasPorCobrar />} />
        <Route path="/cxp" element={<CuentasPorPagar />} />
        <Route path="/clientes" element={<Clientes />} />
        <Route path="/proveedores" element={<Proveedores />} />
        <Route path="/usuarios" element={<Usuarios />} />
        <Route path="/empresa-tiendas" element={<Tiendas />} />
        <Route path="/estado-resultados" element={<EstadoResultados />} />
      </Route>

      {/* Página 404 */}
      <Route path="*" element={<h1 className="text-center mt-5">Página no encontrada</h1>} />
    </Routes>
  );
}
