import { useEffect, useState } from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import {api} from '../services/connection';
import Header from './Header';
import NavBar from './NavBar';
import Footer from './Footer';

export default function ProtectedLayout() {
  const [isValid, setIsValid] = useState(null); // null = validando, true = ok, false = inválido

  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem('access_token');

      if (!token) {
        setIsValid(false);
        return;
      }

      try {
        await api.post('verify/', {
          token: token,
        });
        setIsValid(true);
      } catch (error) {
        console.warn('Token inválido o expirado:', error.response?.data);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setIsValid(false);
      }
    };

    verifyToken();
  }, []);

  if (isValid === null) {
    return <div className="text-center mt-5">Verificando sesión...</div>;
  }

  if (!isValid) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="d-flex flex-column min-vh-100">
      <Header />
      <NavBar />
      <main className="flex-fill container mt-4">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
