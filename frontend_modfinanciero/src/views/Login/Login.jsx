import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import {api} from '../../services/connection';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await api.post('token/', {
                email: email,
                password: password,
            });

            // Guardar tokens
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            localStorage.setItem('access_rol', response.data.rol);
            localStorage.setItem('access_nombre', response.data.nombre);

            setError(null);
            navigate('/dashboard');
        } catch (err) {
            setError('Error al iniciar session; revise los datos de inicio o su coneccion.');
        }
    };

    return (
        <div className="d-flex flex-column min-vh-100">
            <Header />

            <div className="flex-fill d-flex justify-content-center align-items-center bg-white">
                <div className="card shadow p-4" style={{ minWidth: '320px', maxWidth: '400px', width: '100%' }}>
                    <h2 className="text-center mb-4">Iniciar sesión</h2>

                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label className="form-label">Correo</label>
                            <input
                                type="email"
                                className="form-control"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>

                        <div className="mb-3">
                            <label className="form-label">Contraseña</label>
                            <input
                                type="password"
                                className="form-control"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>

                        {error && <div className="alert alert-danger">{error}</div>}

                        <div className="d-grid">
                            <button type="submit" className="btn btn-primary">
                                Entrar
                            </button>
                        </div>
                    </form>
                    <div className="text-center mt-3">
                        <a href="/recuperar" className="text-decoration-none">¿Olvidó su contraseña?</a>
                    </div>
                </div>
            </div>

              <Footer />
        </div>
    );
}
