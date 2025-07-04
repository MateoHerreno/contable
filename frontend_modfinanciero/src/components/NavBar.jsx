import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { logoutUser } from '../utils/connection';

const Nav = () => {
  const rol = parseInt(localStorage.getItem('access_rol'), 10); // 1: admin, 2: gerente, 3: sprempleado, 4: empleado
  const [expanded, setExpanded] = useState(false);

  const isAdminOrGerenteOrSP = rol === 1 || rol === 2 || rol === 3;
  const isEmpleado = rol === 4;

  const toggleNavbar = () => setExpanded(!expanded);
  const closeNavbar = () => setExpanded(false);

  return (
    <nav className="navbar navbar-expand-md navbar-light bg-light border-bottom px-3">
      <div className="container-fluid">
        <Link to="/dashboard" className="navbar-brand" onClick={closeNavbar}>Inicio</Link>

        <button
          className="navbar-toggler"
          type="button"
          onClick={toggleNavbar}
        >
          <span className="navbar-toggler-icon" />
        </button>

        <div className={`collapse navbar-collapse ${expanded ? 'show' : ''}`}>
          <ul className="navbar-nav me-auto mb-2 mb-md-0">

            {isAdminOrGerenteOrSP && (
              <>
                <li className="nav-item"><Link to="/empresa" className="nav-link" onClick={closeNavbar}>Empresa</Link></li>
                <li className="nav-item"><Link to="/tiendas" className="nav-link" onClick={closeNavbar}>Tiendas</Link></li>
                <li className="nav-item"><Link to="/usuarios" className="nav-link" onClick={closeNavbar}>Usuarios</Link></li>
                <li className="nav-item"><Link to="/estadoResultados" className="nav-link" onClick={closeNavbar}>Est. Resultados</Link></li>
              </>
            )}

            {(isAdminOrGerenteOrSP || isEmpleado) && (
              <>
                <li className="nav-item"><Link to="/clientes" className="nav-link" onClick={closeNavbar}>Clientes</Link></li>
                <li className="nav-item"><Link to="/proveedores" className="nav-link" onClick={closeNavbar}>Proveedores</Link></li>
                <li className="nav-item"><Link to="/CuentasPorCobrar" className="nav-link" onClick={closeNavbar}>Cuent. Cobrar</Link></li>
                <li className="nav-item"><Link to="/CuentasPorPagar" className="nav-link" onClick={closeNavbar}>Cuent. Pagar</Link></li>
              </>
            )}
          </ul>

          <div className="d-flex ms-auto">
            <button onClick={logoutUser} className="btn btn-sm btn-outline-danger">
              Cerrar sesión
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Nav;
