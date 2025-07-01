import DataTable from 'react-data-table-component';
import React, { useEffect, useState } from 'react';
import { getClientes, createCliente, updateCliente, deleteCliente } from '../../services/clienteService';
import { limpiarPayload } from '../../services/limpiarPayload';
import { handleApiError } from '../../services/handleApiError';
import EntityModal from '../../components/EntityModal';
import FormGroup from '../../components/FormGroup';
import AlertAutoHide from '../../components/AlertAutoHide';
import { Button } from 'react-bootstrap';
import { BsPencilFill, BsTrashFill } from 'react-icons/bs';

const Clientes = () => {
  const [clientes, setClientes] = useState([]);
  const [form, setForm] = useState({ nombre: '', nit: '', telefono: '' });
  const [error, setError] = useState('');

  const columns = [
    { name: 'Nombre', selector: row => row.nombre, sortable: true },
    { name: 'NIT', selector: row => row.nit },
    { name: 'Teléfono', selector: row => row.telefono },
    { name: 'Saldo', selector: row => row.saldo, sortable: true },
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
    fetchClientes();
  }, []);

  const fetchClientes = async () => {
    try {
      const res = await getClientes();
      setClientes(res.data);
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
        await updateCliente(editId, payload);
        showSuccess('Cliente actualizado.');
      } else {
        await createCliente(payload);
        showSuccess('Cliente creado.');
      }
      fetchClientes();
      setShowModal(false);
    } catch (err) {
      handleApiError(err, setError);
    } finally {
      setLoading(false);
    }
  };

  const openModal = (cliente = null) => {
    if (cliente) {
      setForm({
        nombre: cliente.nombre,
        nit: cliente.nit,
        telefono: cliente.telefono
      });
      setEditId(cliente.id);
    } else {
      setForm({ nombre: '', nit: '', telefono: '' });
      setEditId(null);
    }
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Eliminar este cliente?')) return;
    try {
      await deleteCliente(id);
      showSuccess('Cliente eliminado.');
      fetchClientes();
    } catch (err) {
      handleApiError(err, setError);
    }
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-end align-items-center mb-3">

        <Button variant="primary" onClick={() => openModal(null)}>Crear Cliente</Button>
      </div>

      <AlertAutoHide message={error} />
      <AlertAutoHide message={success} variant="success" />


      <DataTable title="Clientes" columns={columns} data={clientes} pagination striped highlightOnHover />


      <EntityModal
        show={showModal}
        onHide={() => setShowModal(false)}
        onSubmit={handleSubmit}
        title={editId ? 'Editar Cliente' : 'Crear Cliente'}
        loading={loading}
      >
        <FormGroup label="Nombre" name="nombre" value={form.nombre} onChange={handleChange} required />
        <FormGroup label="NIT" name="nit" value={form.nit} onChange={handleChange} type="number" required />
        <FormGroup label="Teléfono" name="telefono" value={form.telefono} onChange={handleChange} required />
      </EntityModal>
    </div>
  );
};

export default Clientes;
