import { Routes, Route, Navigate } from 'react-router-dom';
import { intentarRenovarToken } from '../utils/refreshToken';
import { useEffect } from 'react';

// Vistas públicas
import Login from '../views/Login/Login';
import RecuperarPassword from '../views/Password/RecuperarPassword';
import RestablecerPassword from '../views/Password/RestablecerPassword';

// Vistas protegidas
import Dashboard from '../views/Dashboards/Dashboard';
import CuentasPorCobrar from '../views/CXC/CuentasPorCobrar';
import CuentasPorPagar from '../views/CXP/CuentasPorPagar';
import Clientes from '../views/Clientes/Clientes';
import Proveedores from '../views/Proveedores/Proveedores';
import Usuarios from '../views/Usuarios/Usuarios';
import Tiendas from '../views/Tiendas/Tiendas';
import Empresa from '../views/Empresa/Empresa';
import EstadoResultados from '../views/EstadoResultados/EstadoResultados';

// Layouts y protecciones
import ProtectedLayout from '../components/ProtectedLayout';
import ProtectedRouteByRole from '../components/ProtectedRouteByRole';

export default function AppRoutes() {
  useEffect(() => {
    const interval = setInterval(() => {
      intentarRenovarToken();
    }, 4 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Routes>
      {/* Redirección por defecto */}
      <Route path="/" element={<Navigate to="/login" />} />

      {/* Rutas públicas  los numeros en el array son los numeros que pueden acceder a esa vista*/}
      <Route path="/login" element={<Login />} />
      <Route path="/recuperar" element={<RecuperarPassword />} />
      <Route path="/restablecer" element={<RestablecerPassword />} />

      {/* Rutas protegidas */}
      <Route element={<ProtectedLayout />}>
        <Route path="/dashboard" element={
          <ProtectedRouteByRole allowedRoles={[1, 2, 3]}>
            <Dashboard />
          </ProtectedRouteByRole>
        } />

        <Route path="/empresa" element={
          <ProtectedRouteByRole allowedRoles={[1, 2, 3]}>
            <Empresa />
          </ProtectedRouteByRole>
        } />

        <Route path="/tiendas" element={
          <ProtectedRouteByRole allowedRoles={[1, 2, 3]}>
            <Tiendas />
          </ProtectedRouteByRole>
        } />

        <Route path="/usuarios" element={
          <ProtectedRouteByRole allowedRoles={[1, 2]}>
            <Usuarios />
          </ProtectedRouteByRole>
        } />

        <Route path="/clientes" element={
          <ProtectedRouteByRole allowedRoles={[1, 2, 3, 4]}>
            <Clientes />
          </ProtectedRouteByRole>
        } />

        <Route path="/proveedores" element={
          <ProtectedRouteByRole allowedRoles={[1, 2, 3, 4]}>
            <Proveedores />
          </ProtectedRouteByRole>
        } />

        <Route path="/CuentasPorCobrar" element={
          <ProtectedRouteByRole allowedRoles={[1, 2, 3, 4]}>
            <CuentasPorCobrar />
          </ProtectedRouteByRole>
        } />

        <Route path="/CuentasPorPagar" element={
          <ProtectedRouteByRole allowedRoles={[1, 2, 3, 4]}>
            <CuentasPorPagar />
          </ProtectedRouteByRole>
        } />

        <Route path="/estadoResultados" element={
          <ProtectedRouteByRole allowedRoles={[1, 2, 3]}>
            <EstadoResultados />
          </ProtectedRouteByRole>
        } />
      </Route>

      {/* Página 404 */}
      <Route path="*" element={<Navigate to="/CuentasPorCobrar" replace />} />
    </Routes>
  );
}
