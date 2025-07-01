import React, { useEffect, useState } from 'react';

const Dashboard = () => {
  const [visible, setVisible] = useState(true);
  const nombre = localStorage.getItem('access_nombre') || 'Usuario';

  useEffect(() => {
    // Ocultar automáticamente después de 5 segundos
    const timer = setTimeout(() => setVisible(false), 15000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="container mt-4">
      {visible && (
        <div className="alert alert-info alert-dismissible fade show" role="alert">
          ¡Bienvenido, <strong>{nombre}</strong>! 👋
          <button
            type="button"
            className="btn-close"
            onClick={() => setVisible(false)}
            aria-label="Cerrar"
          ></button>
        </div>
      )}
      <p className="text-muted">Este es tu panel de control general.</p>
    </div>
  );
};

export default Dashboard;
