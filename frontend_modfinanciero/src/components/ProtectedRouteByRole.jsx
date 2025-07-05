// ProtectedRouteByRole.jsx
import { Navigate } from 'react-router-dom';

export default function ProtectedRouteByRole({ children, allowedRoles }) {
  const userRol = parseInt(localStorage.getItem('access_rol'), 10);

  if (!allowedRoles.includes(userRol)) {
    return <Navigate to="/CuentasPorCobrar" replace />
  }

  return children;
}
