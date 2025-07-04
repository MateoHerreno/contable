import React, { useEffect, useState } from 'react';
import DataTable from 'react-data-table-component';
import {
  getCuentasPorPagar,
  createCuentaPorPagar,
  updateCuentaPorPagar,
  deleteCuentaPorPagar,
  getConceptosCXP,
  postExportarCXPpdf,
  postExportarCXPexcel,
} from '../../services/cuentasPorPagarService';
import { getProveedores } from '../../services/proveedorService';
import { limpiarPayload } from '../../utils/limpiarPayload';
import { handleApiError } from '../../utils/handleApiError';
import EntityModal from '../../components/EntityModal';
import FormGroup from '../../components/FormGroup';
import AlertAutoHide from '../../components/AlertAutoHide';
import { Button, Modal, Form } from 'react-bootstrap';
import { BsPencilFill, BsTrashFill } from 'react-icons/bs';

const CuentasPorPagar = () => {
  const [registros, setRegistros] = useState([]);
  const [proveedores, setProveedores] = useState([]);
  const [conceptos, setConceptos] = useState([]);
  const [form, setForm] = useState({
    proveedor: '',
    conceptoFijo: '',
    conceptoDetalle: '',
    val_bruto: '',
    abonos: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editId, setEditId] = useState(null);
  const [showExportModal, setShowExportModal] = useState(false);
  const [exportData, setExportData] = useState({ proveedor: '', fecha_inicio: '', fecha_fin: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = limpiarPayload(form);
    payload.val_bruto = parseFloat(form.val_bruto.replace(/\./g, '').replace(',', '.'));
    payload.abonos = parseFloat(form.abonos.replace(/\./g, '').replace(',', '.'));

    if (payload.val_bruto < 0) {
      setError('El valor bruto no puede ser negativo.');
      return;
    }

    delete payload.saldo_anterior;

    setLoading(true);
    try {
      if (editId) {
        await updateCuentaPorPagar(editId, payload);
        showSuccess('Cuenta actualizada.');
      } else {
        await createCuentaPorPagar(payload);
        showSuccess('Cuenta creada.');
      }
      fetchData();
      setShowModal(false);
    } catch (err) {
      handleApiError(err, setError);
    } finally {
      setLoading(false);
    }
  };

  const openModal = (item = null) => {
    if (item) {
      setForm({
        proveedor: item.proveedor,
        conceptoFijo: item.conceptoFijo,
        conceptoDetalle: item.conceptoDetalle,
        val_bruto: item.val_bruto.toString().replace('.', ','),
        abonos: item.abonos.toString().replace('.', ',')
      });
      setEditId(item.n_cxp);
    } else {
      setForm({
        proveedor: '',
        conceptoFijo: '',
        conceptoDetalle: '',
        val_bruto: '',
        abonos: ''
      });
      setEditId(null);
    }
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Eliminar esta cuenta por pagar?')) return;
    try {
      await deleteCuentaPorPagar(id);
      showSuccess('Cuenta eliminada.');
      fetchData();
    } catch (err) {
      handleApiError(err, setError);
    }
  };

  const showSuccess = (msg) => {
    setSuccess(msg);
    setTimeout(() => setSuccess(''), 4000);
  };

  const fetchData = async () => {
    try {
      const [res1, res2, res3] = await Promise.all([
        getCuentasPorPagar(),
        getProveedores(),
        getConceptosCXP()
      ]);
      setRegistros(res1.data);
      setProveedores(res2.data);
      setConceptos(res3.data);
    } catch (err) {
      handleApiError(err, setError);
    }
  };

  const columns = [
    { name: 'Proveedor', selector: row => proveedores.find(p => p.id === row.proveedor)?.nombre || '—' },
    { name: 'Concepto', selector: row => conceptos.find(c => c.id === row.conceptoFijo)?.nombre || row.conceptoFijo },
    { name: 'Detalle', selector: row => row.conceptoDetalle || '—' },
    { name: 'Valor Bruto', selector: row => row.val_bruto },
    { name: 'Abonos', selector: row => row.abonos },
    { name: 'Saldo Anterior', selector: row => row.saldo_anterior },
    { name: 'Pendiente', selector: row => row.pendiente_por_pagar },
    { name: 'Fecha', selector: row => (row.fecha || '').split(' ')[0] },
    {
      name: 'Acciones',
      cell: row => (
        <div className="d-flex">
          <Button size="sm" variant="warning" className="me-2 d-flex align-items-center" onClick={() => openModal(row)}>
            <BsPencilFill className="me-1" />
          </Button>
          <Button size="sm" variant="danger" onClick={() => handleDelete(row.n_cxp)}>
            <BsTrashFill className="me-2 d-flex align-items-center" />
          </Button>
        </div>
      )
    }
  ];

  const handleExportChange = (e) => {
    const { name, value } = e.target;
    setExportData(prev => ({ ...prev, [name]: value }));
  };

  const exportar = async (tipo) => {
  // ✅ Validar fechas no vacías
  if (!exportData.fecha_inicio || !exportData.fecha_fin) {
    setError('Debes seleccionar una fecha de inicio y fin para exportar.');
    return;
  }

  // ✅ Validar formato YYYY-MM-DD
  const isValidDate = (str) => /^\d{4}-\d{2}-\d{2}$/.test(str);
  if (!isValidDate(exportData.fecha_inicio) || !isValidDate(exportData.fecha_fin)) {
    setError('Formato de fecha inválido. Usa YYYY-MM-DD.');
    return;
  }

  // ✅ Validar orden lógico
  const inicio = new Date(exportData.fecha_inicio);
  const fin = new Date(exportData.fecha_fin);
  if (inicio > fin) {
    setError('La fecha de inicio no puede ser posterior a la fecha de fin.');
    return;
  }

  const payload = {
    fecha_inicio: exportData.fecha_inicio,
    fecha_fin: exportData.fecha_fin,
  };
  if (exportData.proveedor) {
    payload.proveedor = exportData.proveedor;
  }

  try {
    const res = await (tipo === 'pdf'
      ? postExportarCXPpdf(payload)
      : postExportarCXPexcel(payload));
    const blob = new Blob([res.data]);
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `cuentas_pagar_export.${tipo === 'pdf' ? 'pdf' : 'xlsx'}`);
    document.body.appendChild(link);
    link.click();
    setShowExportModal(false);
  } catch (err) {
    handleApiError(err, setError);
  }
};

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-end mb-3">
        <Button variant="primary" onClick={() => openModal()}>Crear Cuenta</Button>
        <Button variant="success" className="me-2" onClick={() => setShowExportModal(true)}>Exportar PDF/Excel</Button>
      </div>

      <AlertAutoHide message={error} />
      <AlertAutoHide message={success} variant="success" />

      <DataTable title="Cuentas por Pagar" columns={columns} data={registros} pagination striped highlightOnHover />

      <EntityModal
        show={showModal}
        onHide={() => setShowModal(false)}
        onSubmit={handleSubmit}
        title={editId ? 'Editar Cuenta' : 'Crear Cuenta'}
        loading={loading}
      >
        <FormGroup label="Proveedor" name="proveedor" value={form.proveedor} onChange={handleChange} as="select" required>
          <option value="">Seleccione...</option>
          {proveedores.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
        </FormGroup>
        <FormGroup label="Concepto Fijo" name="conceptoFijo" value={form.conceptoFijo} onChange={handleChange} as="select" required>
          <option value="">Seleccione...</option>
          {conceptos.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </FormGroup>
        <FormGroup label="Detalle (opcional)" name="conceptoDetalle" value={form.conceptoDetalle} onChange={handleChange} />
        <FormGroup label="Valor Bruto" name="val_bruto" value={form.val_bruto} onChange={handleChange} required />
        <FormGroup label="Abonos" name="abonos" value={form.abonos} onChange={handleChange} />
      </EntityModal>

      <Modal show={showExportModal} onHide={() => setShowExportModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Exportar Cuentas por Pagar</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group className="mb-3">
            <Form.Label>Proveedor (opcional)</Form.Label>
            <Form.Select name="proveedor" value={exportData.proveedor} onChange={handleExportChange}>
              <option value="">Todos</option>
              {proveedores.map(p => (
                <option key={p.id} value={p.id}>{p.nombre}</option>
              ))}
            </Form.Select>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Fecha Inicio</Form.Label>
            <Form.Control type="date" name="fecha_inicio" value={exportData.fecha_inicio} onChange={handleExportChange} required />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Fecha Fin</Form.Label>
            <Form.Control type="date" name="fecha_fin" value={exportData.fecha_fin} onChange={handleExportChange} required />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowExportModal(false)}>Cancelar</Button>
          <Button variant="success" onClick={() => exportar('excel')}>Exportar Excel</Button>
          <Button variant="danger" onClick={() => exportar('pdf')}>Exportar PDF</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default CuentasPorPagar;
