import { useState } from 'react';
import axios from 'axios';

export default function RecuperarPassword() {
    const [email, setEmail] = useState('');
    const [mensaje, setMensaje] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://127.0.0.1:8000/api/passrequest/', { email });
            setMensaje({ tipo: 'success', texto: 'Revisa tu correo para continuar con la recuperación.' });
        } catch {
            setMensaje({ tipo: 'danger', texto: 'No se pudo procesar la solicitud.' });
        }
    };

    return (
        <div className="d-flex flex-column min-vh-100">
            {/* Franja azul superior */}
            <div className="bg-primary py-3"></div>

            {/* Contenido centrado */}
            <div className="flex-fill d-flex justify-content-center align-items-center bg-white">
                <div className="card shadow p-4" style={{ minWidth: '320px', maxWidth: '400px', width: '100%' }}>
                    <h2 className="text-center mb-4">Recuperar contraseña</h2>

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

                        <div className="d-grid">
                            <button type="submit" className="btn btn-primary">Enviar</button>
                        </div>
                        <div className="d-flex justify-content-between mt-3">
                            <a href="/login" className="text-decoration-none text-end">
                                Login
                            </a>
                            <a href="/restablecer" className="text-decoration-none">
                                Ya tengo un token
                            </a>
                        </div>



                    </form>

                    {mensaje && (
                        <div className={`alert alert-${mensaje.tipo} mt-3`} role="alert">
                            {mensaje.texto}
                        </div>
                    )}
                </div>
            </div>

            {/* Franja azul inferior */}
            <div className="bg-primary py-3 mt-auto"></div>
        </div>
    );
}
