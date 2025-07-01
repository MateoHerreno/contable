import DataTable from 'react-data-table-component';
import React, { useEffect, useState } from 'react';
import EntityModal from '../../components/EntityModal';
import FormGroup from '../../components/FormGroup';
import AlertAutoHide from '../../components/AlertAutoHide';
import { getTiendas, createTienda, updateTienda, deleteTienda } from '../../services/tiendaService';
import { getEmpresas } from '../../services/empresaService';
import { handleApiError } from '../../services/handleApiError';
import { limpiarPayload } from '../../services/limpiarPayload';
import { Button } from 'react-bootstrap';
import { BsPencilFill, BsTrashFill } from 'react-icons/bs';

const Tienda = () => {
  const [tiendas, setTiendas] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [form, setForm] = useState({
    nombre: '',
    direccion: '',
    ciudad: '',
    empresa: '',
  });
  const [error, setError] = useState('');

  const columns = [
    { name: 'Nombre', selector: row => row.nombre, sortable: true },
    { name: 'Dirección', selector: row => row.direccion },
    { name: 'Ciudad', selector: row => row.ciudad },
    { name: 'Empresa', selector: row => empresas.find(e => e.id === row.empresa)?.nombre || '—' },
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

  useEffect(() => {
    fetchTiendas();
    fetchEmpresas();
  }, []);

  const fetchTiendas = async () => {
    try {
      const res = await getTiendas();
      setTiendas(res.data);
    } catch (err) {
      handleApiError(err, setError);
    }
  };

  const fetchEmpresas = async () => {
    try {
      const res = await getEmpresas();
      setEmpresas(res.data);
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
    const payload = limpiarPayload(form);

    setLoading(true);
    try {
      if (editId) {
        await updateTienda(editId, payload);
        showSuccess('Tienda actualizada.');
      } else {
        await createTienda(payload);
        showSuccess('Tienda creada.');
      }
      fetchTiendas();
      setShowModal(false);
    } catch (err) {
      handleApiError(err, setError);
    } finally {
      setLoading(false);
    }
  };

  const openModal = (tienda = null) => {
    if (tienda) {
      setForm({
        nombre: tienda.nombre,
        direccion: tienda.direccion,
        ciudad: tienda.ciudad,
        empresa: tienda.empresa,
      });
      setEditId(tienda.id);
    } else {
      setForm({ nombre: '', direccion: '', ciudad: '', empresa: '' });
      setEditId(null);
    }
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Eliminar esta tienda?')) return;
    try {
      await deleteTienda(id);
      showSuccess('Tienda eliminada.');
      fetchTiendas();
    } catch (err) {
      handleApiError(err, setError);
    }
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-end align-items-center mb-3">

        <Button variant="primary" onClick={() => openModal(null)}>Crear Tienda</Button>
      </div>

      <AlertAutoHide message={error} />
      <AlertAutoHide message={success} variant="success" />

      <DataTable title="Tiendas" columns={columns} data={tiendas} pagination striped highlightOnHover />

      <EntityModal
        show={showModal}
        onHide={() => setShowModal(false)}
        onSubmit={handleSubmit}
        title={editId ? 'Editar Tienda' : 'Crear Tienda'}
        loading={loading}
      >
        <FormGroup label="Nombre" name="nombre" value={form.nombre} onChange={handleChange} required />
        <FormGroup label="Dirección" name="direccion" value={form.direccion} onChange={handleChange} />
        <FormGroup label="Ciudad" name="ciudad" value={form.ciudad} onChange={handleChange} />
        <FormGroup label="Empresa" name="empresa" value={form.empresa} onChange={handleChange} as="select" required>
          <option value="">Seleccione una empresa</option>
          {empresas.map((e) => (
            <option key={e.id} value={e.id}>{e.nombre}</option>
          ))}
        </FormGroup>
      </EntityModal>
    </div>
  );
};

export default Tienda;
