import React, { useEffect, useState } from 'react';
import DataTable from 'react-data-table-component';
import { getCuentasPorCobrar, createCuentaPorCobrar, updateCuentaPorCobrar,
        deleteCuentaPorCobrar, getConceptosCXC, postExportarCXCpdf, postExportarCXCexcel 
      } from '../../services/cuentasPorCobrarService';
import { getClientes } from '../../services/clienteService';
import { limpiarPayload } from '../../utils/limpiarPayload';
import { handleApiError } from '../../utils/handleApiError';
import EntityModal from '../../components/EntityModal';
import FormGroup from '../../components/FormGroup';
import AlertAutoHide from '../../components/AlertAutoHide';
import { Button, Modal } from 'react-bootstrap';
import { BsPencilFill, BsTrashFill } from 'react-icons/bs';
import { Form } from 'react-bootstrap';

const CuentasPorCobrar = () => {
  const [registros, setRegistros] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [conceptos, setConceptos] = useState([]);
  const [form, setForm] = useState({
    cliente: '',
    conceptoFijo: '',
    conceptoDetalle: '',
    val_bruto: '',
    iva: '0',
    retenciones: '0',
    abonos: '',
    descripcion_nota_credito: ''
  });
  const [totales, setTotales] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editId, setEditId] = useState(null);
  const [showNotaModal, setShowNotaModal] = useState(false);
  const [notaSeleccionada, setNotaSeleccionada] = useState(null);

  const formatMiles = (str) => {
    const clean = str.replace(/[^0-9\\-]/g, '');
    return clean.replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'val_bruto') {
      const raw = value.replace(/[^0-9\\-]/g, '');
      setForm(prev => ({ ...prev, [name]: raw }));
    } else {
      setForm(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = limpiarPayload(form);
    payload.val_bruto = parseInt(form.val_bruto.replace(/\\./g, ''), 10);

    if (payload.val_bruto < 0 && !payload.descripcion_nota_credito) {
      setError('Debes incluir descripción si el valor bruto es negativo.');
      return;
    }

    setLoading(true);
    try {
      if (editId) {
        await updateCuentaPorCobrar(editId, payload);
        showSuccess('Cuenta actualizada.');
      } else {
        await createCuentaPorCobrar(payload);
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
      const bruto = parseFloat(item.val_bruto);
      const iva = parseFloat(item.iva);
      const ret = parseFloat(item.retenciones);
      let iva_pct = '0';
      let ret_pct = '0';

      if (bruto !== 0) {
        iva_pct = Math.round((iva / bruto) * 100).toString();
        ret_pct = Math.round((ret / bruto) * 100).toString();
      }

      setForm({
        cliente: item.cliente,
        conceptoFijo: item.conceptoFijo,
        conceptoDetalle: item.conceptoDetalle,
        val_bruto: bruto.toString(),
        iva: iva_pct,
        retenciones: ret_pct,
        abonos: item.abonos,
        descripcion_nota_credito: item?.nota_credito?.descripcion || ''
      });
      setEditId(item.n_cxc);
      setTotales(null);
    } else {
      setForm({
        cliente: '',
        conceptoFijo: '',
        conceptoDetalle: '',
        val_bruto: '',
        iva: '0',
        retenciones: '0',
        abonos: '',
        descripcion_nota_credito: ''
      });
      setEditId(null);
      setTotales(null);
    }
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Eliminar esta cuenta por cobrar?')) return;
    try {
      await deleteCuentaPorCobrar(id);
      showSuccess('Cuenta eliminada.');
      fetchData();
    } catch (err) {
      handleApiError(err, setError);
    }
  };

  const handleCalcularTotales = () => {
    const bruto = parseInt(form.val_bruto.replace(/\\./g, ''), 10);
    const ivaPct = parseFloat(form.iva || 0);
    const retPct = parseFloat(form.retenciones || 0);

    if (isNaN(bruto)) {
      setError('Debes ingresar un valor bruto válido.');
      return;
    }

    const iva = Math.round((bruto * ivaPct) / 100);
    const ret = Math.round((bruto * retPct) / 100);
    const neto = bruto + iva - ret;

    setTotales({
      iva: formatMiles(iva.toString()),
      retenciones: formatMiles(ret.toString()),
      neto: formatMiles(neto.toString())
    });
  };

  const showSuccess = (msg) => {
    setSuccess(msg);
    setTimeout(() => setSuccess(''), 4000);
  };

  const fetchData = async () => {
    try {
      const [res1, res2, res3] = await Promise.all([
        getCuentasPorCobrar(),
        getClientes(),
        getConceptosCXC()
      ]);
      setRegistros(res1.data);
      setClientes(res2.data);
      setConceptos(res3.data);
    } catch (err) {
      handleApiError(err, setError);
    }
  };

  const columns = [
    { name: 'Cliente', selector: row => clientes.find(c => c.id === row.cliente)?.nombre || '—' },
    { name: 'Concepto', selector: row => conceptos.find(c => c.id === row.conceptoFijo)?.nombre || row.conceptoFijo },
    { name: 'Detalle', selector: row => row.conceptoDetalle || '—' },
    { name: 'Valor Bruto', selector: row => row.val_bruto },
    { name: 'IVA', selector: row => row.iva },
    { name: 'Retenciones', selector: row => row.retenciones },
    { name: 'Neto', selector: row => row.neto_facturado },
    { name: 'Abonos', selector: row => row.abonos },
    { name: 'Pendiente', selector: row => row.pendiente_por_pagar },
    {
      name: 'Nota Crédito',
      selector: row =>
        row?.nota_credito ? (
          <Button
            variant="link"
            className="p-0 text-decoration-underline"
            onClick={() => {
              setNotaSeleccionada(row.nota_credito);
              setShowNotaModal(true);
            }}
          >
            #{row.nota_credito.id}
          </Button>
        ) : '—'
    },
    { name: 'Fecha', selector: row => (row.fecha || '').split(' ')[0] },
    {
      name: 'Acciones',
      cell: row => (
        <div className="d-flex">
          <Button size="sm" variant="warning" className="me-2 d-flex align-items-center" onClick={() => openModal(row)}>
            <BsPencilFill className="me-1" />
          </Button>
          <Button size="sm" variant="danger" onClick={() => handleDelete(row.n_cxc)}>
            <BsTrashFill className="me-2 d-flex align-items-center" />
          </Button>
        </div>
      )
    }
  ];
  const [showExportModal, setShowExportModal] = useState(false);
  const [exportData, setExportData] = useState({ cliente: '', fecha_inicio: '', fecha_fin: '' });

  const handleExportChange = (e) => {
    const { name, value } = e.target;
    setExportData(prev => ({ ...prev, [name]: value }));
  };

  const exportar = async (tipo) => {

  const isValidDate = (str) => /^\d{4}-\d{2}-\d{2}$/.test(str);
  if (!isValidDate(exportData.fecha_inicio) || !isValidDate(exportData.fecha_fin)) {
    setError('Formato de fecha inválido. Usa YYYY-MM-DD.');
    return;
  }

  const inicio = new Date(exportData.fecha_inicio);
  const fin = new Date(exportData.fecha_fin);
  if (inicio > fin) {
    setError('La fecha de inicio no puede ser posterior a la fecha de fin.');
    return;
  }


    if (!exportData.fecha_inicio || !exportData.fecha_fin) {
      setError('Debes seleccionar una fecha de inicio y fin para exportar.');
      return;
    }

    const payload = {
      fecha_inicio: exportData.fecha_inicio,
      fecha_fin: exportData.fecha_fin,
    };
    if (exportData.cliente) {
      payload.cliente = exportData.cliente;
    }

    try {
      const res = await (tipo === 'pdf'
        ? postExportarCXCpdf(payload)
        : postExportarCXCexcel(payload));
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `cuentas_cobrar_export.${tipo === 'pdf' ? 'pdf' : 'xlsx'}`);
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

      <DataTable title="Cuentas por Cobrar" columns={columns} data={registros} pagination striped highlightOnHover />

      <EntityModal
        show={showModal}
        onHide={() => setShowModal(false)}
        onSubmit={handleSubmit}
        title={editId ? 'Editar Cuenta' : 'Crear Cuenta'}
        loading={loading}
      >
        <FormGroup label="Cliente" name="cliente" value={form.cliente} onChange={handleChange} as="select" required>
          <option value="">Seleccione...</option>
          {clientes.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </FormGroup>
        <FormGroup label="Concepto Fijo" name="conceptoFijo" value={form.conceptoFijo} onChange={handleChange} as="select" required>
          <option value="">Seleccione...</option>
          {conceptos.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </FormGroup>
        <FormGroup label="Detalle (opcional)" name="conceptoDetalle" value={form.conceptoDetalle} onChange={handleChange} />
        <FormGroup
          label="Valor Bruto"
          name="val_bruto"
          value={formatMiles(form.val_bruto)}
          onChange={handleChange}
          required
        />
        <FormGroup label="IVA (%)" name="iva" value={form.iva} onChange={handleChange} as="select" required>
          <option value="0">0%</option>
          <option value="5">5%</option>
          <option value="19">19%</option>
        </FormGroup>
        <FormGroup label="Retenciones (%)" name="retenciones" value={form.retenciones} onChange={handleChange} type="number" required />
        <FormGroup label="Abonos" name="abonos" value={form.abonos} onChange={handleChange} type="number" />
        {parseInt(form.val_bruto) < 0 && (
          <FormGroup label="Descripción Nota Crédito" name="descripcion_nota_credito" value={form.descripcion_nota_credito} onChange={handleChange} required />
        )}
        <div className="d-grid gap-2 mb-3">
          <Button variant="secondary" type="button" onClick={handleCalcularTotales}>
            Calcular Totales
          </Button>
        </div>
        {totales && (
          <>
            <FormGroup label="IVA estimado ($)" value={totales.iva} type="text" readOnly disabled />
            <FormGroup label="Retenciones estimadas ($)" value={totales.retenciones} type="text" readOnly disabled />
            <FormGroup label="Neto Facturado estimado ($)" value={totales.neto} type="text" readOnly disabled />
          </>
        )}
      </EntityModal>

      <Modal show={showNotaModal} onHide={() => setShowNotaModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Detalle de Nota Crédito</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {notaSeleccionada && (
            <>
              <p><strong>ID:</strong> #{notaSeleccionada.id}</p>
              <p><strong>Descripción:</strong></p>
              <p>{notaSeleccionada.descripcion}</p>
            </>
          )}
        </Modal.Body>
      </Modal>

      <Modal show={showExportModal} onHide={() => setShowExportModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Exportar Cuentas por Cobrar</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group className="mb-3">
            <Form.Label>Cliente (opcional)</Form.Label>
            <Form.Select name="cliente" value={exportData.cliente} onChange={handleExportChange}>
              <option value="">Todos</option>
              {clientes.map(c => (
                <option key={c.id} value={c.id}>{c.nombre}</option>
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

export default CuentasPorCobrar;



