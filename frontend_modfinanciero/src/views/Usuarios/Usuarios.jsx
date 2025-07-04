import DataTable from 'react-data-table-component';
import React, { useEffect, useState } from 'react';
import { getUsuarios, createUsuario, updateUsuario, deleteUsuario } from '../../services/usuarioService';
import { getTiendas } from '../../services/tiendaService';
import { limpiarPayload } from '../../utils/limpiarPayload';
import { handleApiError } from '../../utils/handleApiError';
import EntityModal from '../../components/EntityModal';
import FormGroup from '../../components/FormGroup';
import AlertAutoHide from '../../components/AlertAutoHide';
import { Button } from 'react-bootstrap';
import { BsPencilFill, BsTrashFill } from 'react-icons/bs';

const Usuarios = () => {
    const [usuarios, setUsuarios] = useState([]);
    const [tiendas, setTiendas] = useState([]);
    const [form, setForm] = useState({
        nombre: '',
        email: '',
        password: '',
        password2: '',
        telefono: '',
        tienda: '',
        rol: '',
        is_active: true
    });
    const [error, setError] = useState('');

    const ROLES_LABELS = {
        1: 'Admin',
        2: 'Gerente',
        3: 'Súper Empleado',
        4: 'Empleado'
    };

    const columns = [
        {
    name: 'Activo',
    selector: row => row.is_active ? 'Sí' : 'No',
    sortable: true,
  },
  { name: 'Nombre', selector: row => row.nombre, sortable: true },
        { name: 'Email', selector: row => row.email },
        { name: 'Teléfono', selector: row => row.telefono },
        { name: 'Rol', selector: row => ROLES_LABELS[row.rol] || row.rol },
        { name: 'Tienda', selector: row => tiendas.find(t => t.id === row.tienda)?.nombre || '—' },
        { name: 'Estado', selector: row => row.is_active ? 'Activo' : 'Inactivo' },
        {
            name: 'Acciones',
            cell: row => (
                <>
                    <Button size="sm" variant="warning" className="me-2 d-flex align-items-center" onClick={() => openModal(row)}>
                        <BsPencilFill className="me-1" />
                    </Button>
                    <Button size="sm" variant="danger" onClick={() => handleDelete(row.id)}>
                        <BsTrashFill className="me-2 d-flex align-items-center" />
                    </Button>
                </>
            )
        }
    ];

    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [editId, setEditId] = useState(null);

    const showSuccess = (message) => {
        setSuccess(message);
        setTimeout(() => setSuccess(''), 5000);
    };

    const myRol = parseInt(localStorage.getItem('access_rol')) || 0;

    useEffect(() => {
        if (myRol === 4) return;
        fetchUsuarios();
        fetchTiendas();
    }, [myRol]);

    const fetchUsuarios = async () => {
        try {
            const res = await getUsuarios();
            setUsuarios(res.data);
        } catch (err) {
            handleApiError(err, setError);
        }
    };

    const fetchTiendas = async () => {
        try {
            const res = await getTiendas();
            setTiendas(res.data);
        } catch (err) {
            handleApiError(err, setError);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm({ ...form, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (form.password !== form.password2) {
            setError('Las contraseñas no coinciden.');
            return;
        }

        let payload = limpiarPayload(form);
        payload.is_active = true;
        if (!form.tienda) {
            payload.tienda = null;
        }

        setLoading(true);
        try {
            if (editId) {
                await updateUsuario(editId, payload);
                showSuccess('Usuario actualizado.');
            } else {
                await createUsuario(payload);
                showSuccess('Usuario creado.');
            }
            fetchUsuarios();
            setShowModal(false);
        } catch (err) {
            handleApiError(err, setError);
        } finally {
            setLoading(false);
        }
    };

    const openModal = (usuario = null) => {
        if (usuario) {
            setForm({
                nombre: usuario.nombre,
                email: usuario.email,
                password: '',
                password2: '',
                telefono: usuario.telefono,
                tienda: usuario.tienda || '',
                rol: usuario.rol,
                is_active: usuario.is_active
            });
            setEditId(usuario.id);
        } else {
            setForm({
                nombre: '',
                email: '',
                password: '',
                password2: '',
                telefono: '',
                tienda: '',
                rol: '',
                is_active: true
            });
            setEditId(null);
        }
        setShowModal(true);
    };

    const handleDelete = async (id) => {
        if (!window.confirm('¿Eliminar este usuario?')) return;
        try {
            await deleteUsuario(id);
            showSuccess('Usuario eliminado.');
            fetchUsuarios();
        } catch (err) {
            handleApiError(err, setError);
        }
    };

    const rolOptions = [
        { value: 1, label: 'Admin' },
        { value: 2, label: 'Gerente' },
        { value: 3, label: 'Súper Empleado' },
        { value: 4, label: 'Empleado' }
    ].filter(opt => opt.value > myRol); // solo puede crear roles menores


    return (
        <div className="container mt-4">
            <div className="d-flex justify-content-end align-items-center mb-3">
                <Button variant="primary" onClick={() => openModal(null)}>Crear Usuario</Button>
            </div>

            <AlertAutoHide message={error} />
            <AlertAutoHide message={success} variant="success" />
            <DataTable title="Usuarios" columns={columns} data={usuarios} pagination striped highlightOnHover />
            <EntityModal
                show={showModal}
                onHide={() => setShowModal(false)}
                onSubmit={handleSubmit}
                title={editId ? 'Editar Usuario' : 'Crear Usuario'}
                loading={loading}
            >
                <FormGroup label="Nombre" name="nombre" value={form.nombre} onChange={handleChange} required />
                <FormGroup label="Email" name="email" value={form.email} onChange={handleChange} type="email" required />
                <FormGroup label="Teléfono" name="telefono" value={form.telefono} onChange={handleChange} required />
                <FormGroup label="Contraseña" name="password" value={form.password} onChange={handleChange} type="password" />
                <FormGroup label="Confirmar contraseña" name="password2" value={form.password2} onChange={handleChange} type="password" />
                <FormGroup label="Tienda (opcional)" name="tienda" value={form.tienda} onChange={handleChange} as="select">
                    <option value="">— Ninguna —</option>
                    {tiendas.map((t) => (
                        <option key={t.id} value={t.id}>{t.nombre}</option>
                    ))}
                </FormGroup>
                
<FormGroup label="Rol" name="rol" value={form.rol} onChange={handleChange} as="select" required>
  <option value="">— Seleccionar rol —</option>
  {rolOptions.map((r) => (
    <option key={r.value} value={r.value}>{r.label}</option>
  ))}
</FormGroup>

{/* ✅ Switch para activar o desactivar */}
<div className="mb-3 form-check form-switch">
  <input
    className="form-check-input"
    type="checkbox"
    id="is_active"
    checked={form.is_active}
    onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
  />
  <label className="form-check-label" htmlFor="is_active">
    Usuario activo
  </label>
</div>

            </EntityModal>
        </div>
    );
};

export default Usuarios;
