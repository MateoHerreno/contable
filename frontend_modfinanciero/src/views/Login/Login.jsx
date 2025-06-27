import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://localhost:8000/api/token/', {
                email: email,
                password: password,
            });

            // Guardar tokens
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);

            setError(null);
            navigate('/dashboard');
        } catch (err) {
            setError('Credenciales incorrectas o error de conexión.');
        }
    };

    return (
        <div className="d-flex flex-column min-vh-100">
            <div className="bg-primary py-3"></div>

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

            <div className="bg-primary py-3 mt-auto"></div>
        </div>
    );
}
