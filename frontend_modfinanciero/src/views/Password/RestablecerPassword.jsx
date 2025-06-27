import { useEffect, useState } from 'react';
import axios from 'axios';
import { useSearchParams, Link } from 'react-router-dom';

export default function RestablecerPassword() {
    const [searchParams] = useSearchParams();

    const [form, setForm] = useState({
        email: '',
        token_recuperar: '',
        nueva_password: '',
        confirmar_password: '',
    });

    const [mensaje, setMensaje] = useState(null);
    const [exito, setExito] = useState(false); // para mostrar botón si todo salió bien

    useEffect(() => {
        const email = searchParams.get('email');
        const token = searchParams.get('token');
        setForm((prev) => ({
            ...prev,
            email: email || '',
            token_recuperar: token || '',
        }));
    }, [searchParams]);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (form.nueva_password !== form.confirmar_password) {
            setMensaje({ tipo: 'danger', texto: 'Las contraseñas no coinciden.' });
            return;
        }

        try {
            await axios.post('http://127.0.0.1:8000/api/passreset/', form);
            setMensaje({ tipo: 'success', texto: '✅ Contraseña restablecida correctamente.' });
            setExito(true);

            setForm({
                email: '',
                token_recuperar: '',
                nueva_password: '',
                confirmar_password: '',
            });
        } catch {
            setMensaje({ tipo: 'danger', texto: '❌ Error al restablecer la contraseña. Revisa el correo o el token.' });
        }
    };

    return (
        <div className="d-flex flex-column min-vh-100">
            {/* Franja azul superior */}
            <div className="bg-primary py-3"></div>

            {/* Contenido centrado */}
            <div className="flex-fill d-flex justify-content-center align-items-center bg-white">
                <div className="card shadow p-4" style={{ minWidth: '320px', maxWidth: '400px', width: '100%' }}>
                    <h2 className="text-center mb-4">Restablecer contraseña</h2>

                    {!exito && (
                        <form onSubmit={handleSubmit}>
                            <div className="mb-3">
                                <label className="form-label">Correo</label>
                                <input
                                    type="email"
                                    className="form-control"
                                    name="email"
                                    value={form.email}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div className="mb-3">
                                <label className="form-label">Token</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    name="token_recuperar"
                                    value={form.token_recuperar}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div className="mb-3">
                                <label className="form-label">Nueva contraseña</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    name="nueva_password"
                                    value={form.nueva_password}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div className="mb-3">
                                <label className="form-label">Confirmar contraseña</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    name="confirmar_password"
                                    value={form.confirmar_password}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div className="d-grid">
                                <button className="btn btn-primary" type="submit">Cambiar contraseña</button>
                            </div>
                            <div className="d-flex justify-content-between mt-3">
                                <a href="/recuperar" className="text-decoration-none">
                                    No tengo un token
                                </a>
                                <a href="/login" className="text-decoration-none text-end">
                                    Login
                                </a>
                            </div>
                        </form>
                    )}

                    {mensaje && (
                        <div className={`alert alert-${mensaje.tipo} mt-3`} role="alert">
                            {mensaje.texto}
                        </div>
                    )}

                    {exito && (
                        <div className="text-center mt-3">
                            <Link to="/login" className="btn btn-outline-primary">
                                Volver al login
                            </Link>
                        </div>
                    )}
                </div>
            </div>

            {/* Franja azul inferior */}
            <div className="bg-primary py-3 mt-auto"></div>
        </div>
    );
}
