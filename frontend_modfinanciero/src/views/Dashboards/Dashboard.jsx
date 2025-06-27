
export default function Dashboard() {
  return (
    <div className="d-flex flex-column min-vh-100">
      <main className="flex-fill container mt-4">
        <h2>Bienvenido al Dashboard</h2>
        <p className="lead">Aquí puedes acceder a las secciones del sistema contable.</p>
        <ul>
          <li>Consultar cuentas por cobrar y pagar</li>
          <li>Administrar clientes y proveedores</li>
          <li>Generar estado de resultados</li>
        </ul>
      </main>
    </div>
  );
}
