import { Link } from 'react-router-dom';
import { logoutUser } from '../services/auth';

export default function NavBar() {
  const handleLogout = () => {
    logoutUser(); // limpia tokens y redirige a login
  };

  return (
    <nav className="bg-light border-bottom py-2 px-3">
      <div className="d-flex flex-wrap gap-3 w-100 align-items-center">
        <Link to="/dashboard" className="nav-link">Inicio</Link>
        <Link to="/empresa" className="nav-link">Empresa</Link>
        <Link to="/tienda" className="nav-link"> Tiendas</Link>
        <Link to="/clientes" className="nav-link">Clientes</Link>
        <Link to="/proveedores" className="nav-link">Proveedores</Link>
        <Link to="/cxc" className="nav-link">Cuent. cobrar</Link>
        <Link to="/cxp" className="nav-link">Cuent. pagar</Link>
        <Link to="/estado-resultados" className="nav-link">Est. Resultados</Link>

        {/* Botón de logout alineado a la derecha */}
        <div className="ms-auto">
          <button onClick={handleLogout} className="btn btn-sm btn-outline-danger">
            Cerrar sesión
          </button>
        </div>
      </div>
    </nav>
  );
}
