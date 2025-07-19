import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { api } from '../../utils/connection';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye } from '@fortawesome/free-solid-svg-icons';
import { faEyeSlash } from '@fortawesome/free-solid-svg-icons';

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

            const rol = parseInt(response.data.rol, 10);
            setError(null);
            navigate(rol === 4 ? '/CuentasPorCobrar' : '/dashboard');
        } catch (err) {
            setError('Error al iniciar sesión; revise los datos de inicio o su conexión.');
        }
    };

    //mostrar password escrito en el input
    
    const [showPassword, setShowPassword] = useState(false);
    const passwordRef = useRef(null);

    const togglePassword = () => {
        setShowPassword(!showPassword);
    };

    return (
        <div className="d-flex flex-column min-vh-100">
            <Header />

            <div className="flex-fill d-flex justify-content-center align-items-center form">
                <div className='logo'> <img src="/logo1.jpg" alt="Logo" /> </div>
                <div className="card shadow p-4" style={{ minWidth: '320px', maxWidth: '400px', width: '100%' }}>
                    <h2 className="text-center text-light mb-5">Iniciar sesión</h2>

                    <form className='fr' onSubmit={handleSubmit}>
                        <div className="mb-5">
                            
                            <input
                                type="email"
                                placeholder=' '
                                className=""
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                            <label className="form-label">Correo</label>
                        </div>

                        <div className="mb-5">
                            
                            <input
                                ref={passwordRef}
                                id='password'
                                type={showPassword ? 'text' : 'password'}
                                placeholder=' '
                                className=""
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                            <label className="form-label">Contraseña</label>
                            <span ><FontAwesomeIcon 
                                icon={showPassword ? faEyeSlash : faEye}
                                onClick={togglePassword}
                            /></span>
                        </div>

                        {error && <div className="alert alert-danger">{error}</div>}

                        <div className="d-grid">
                            <button type="submit" className="btn bg-white rounded-pill">
                                Entrar
                            </button>
                        </div>
                    </form>
                    <div className="text-center mt-3">
                        <a href="/recuperar" className="text-decoration-none text-light">¿Olvidó su contraseña?</a>
                    </div>
                </div>
            </div>

            <Footer />
        </div>
    );
}
