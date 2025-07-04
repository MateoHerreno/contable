import DataTable from 'react-data-table-component';
import React, { useEffect, useState } from 'react';
import EntityModal from '../../components/EntityModal';
import FormGroup from '../../components/FormGroup';
import AlertAutoHide from '../../components/AlertAutoHide';
import { getEmpresas, createEmpresa, updateEmpresa, deleteEmpresa } from '../../services/empresaService';
import { handleApiError } from '../../utils/handleApiError';
import { limpiarPayload } from '../../utils/limpiarPayload';
import { api } from '../../utils/connection';
import { Button } from 'react-bootstrap';
import { BsPencilFill, BsTrashFill } from 'react-icons/bs';

const Empresa = () => {
  const [empresas, setEmpresas] = useState([]);
  const [perfiles, setPerfiles] = useState([]);
  const [form, setForm] = useState({ nombre: '', nit: '', telefono: '', perfiles: [] });
  const [error, setError] = useState('');

  const columns = [
    { name: 'Nombre', selector: row => row.nombre, sortable: true },
    { name: 'NIT', selector: row => row.nit },
    { name: 'Teléfono', selector: row => row.telefono },
    { name: 'Perfiles', selector: row => (row.perfiles_nombres || []).join(', ') },
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
    fetchEmpresas();
    fetchPerfiles();
  }, []);

  const fetchEmpresas = async () => {
    try {
      const res = await getEmpresas();
      setEmpresas(res.data);
    } catch (err) {
      handleApiError(err, setError);
    }
  };

  const fetchPerfiles = async () => {
    try {
      const res = await api.get('perfiles/');
      setPerfiles(res.data);
    } catch (err) {
      handleApiError(err, setError);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handlePerfilesChange = (e) => {
    const selected = Array.from(e.target.selectedOptions, opt => parseInt(opt.value));
    setForm({ ...form, perfiles: selected });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = limpiarPayload(form);

    setLoading(true);
    try {
      if (editId) {
        await updateEmpresa(editId, payload);
        showSuccess('Empresa actualizada.');
      } else {
        await createEmpresa(payload);
        showSuccess('Empresa creada.');
      }
      fetchEmpresas();
      setShowModal(false);
    } catch (err) {
      handleApiError(err, setError);
    } finally {
      setLoading(false);
    }
  };

  const openModal = (empresa = null) => {
    if (empresa) {
      setForm({
        nombre: empresa.nombre,
        nit: empresa.nit,
        telefono: empresa.telefono,
        perfiles: empresa.perfiles || [],
      });
      setEditId(empresa.id);
    } else {
      setForm({ nombre: '', nit: '', telefono: '', perfiles: [] });
      setEditId(null);
    }
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Eliminar esta empresa?')) return;
    try {
      await deleteEmpresa(id);
      showSuccess('Empresa eliminada.');
      fetchEmpresas();
    } catch (err) {
      handleApiError(err, setError);
    }
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-end align-items-center mb-3">
        <Button variant="primary" onClick={() => openModal(null)}>Crear Empresa</Button>
      </div>

      <AlertAutoHide message={error} />
      <AlertAutoHide message={success} variant="success" />

      <DataTable title="Empresas" columns={columns} data={empresas} pagination striped highlightOnHover />

      <EntityModal
        show={showModal}
        onHide={() => setShowModal(false)}
        onSubmit={handleSubmit}
        title={editId ? 'Editar Empresa' : 'Crear Empresa'}
        loading={loading}
      >
        <FormGroup label="Nombre" name="nombre" value={form.nombre} onChange={handleChange} required />
        <FormGroup label="NIT" name="nit" value={form.nit} onChange={handleChange} type="number" required />
        <FormGroup label="Teléfono" name="telefono" value={form.telefono} onChange={handleChange} required />
        <FormGroup
          label="Perfiles"
          name="perfiles"
          value={form.perfiles}
          onChange={handlePerfilesChange}
          as="select"
          multiple
        >
          {perfiles.map(p => (
            <option key={p.id} value={p.id}>{p.nombre}</option>
          ))}
        </FormGroup>
      </EntityModal>
    </div>
  );
};

export default Empresa;
