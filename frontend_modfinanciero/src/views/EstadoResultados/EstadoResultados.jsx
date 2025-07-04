import React, { useState } from 'react';
import {
  postEstadoResultados,
  postPDFEstadoResultados,
  postExcelEstadoResultados
} from '../../services/estadoResultadosService';
import { handleApiError } from '../../utils/handleApiError';
import AlertAutoHide from '../../components/AlertAutoHide';
import { Button, Modal, Form } from 'react-bootstrap';

const EstadoResultados = () => {
  const [showModal, setShowModal] = useState(true);
  const [form, setForm] = useState({ anio: '', mes: '' });
  const [filtros, setFiltros] = useState({ anio: null, mes: null });
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.anio || !form.mes) {
      setError('Debes seleccionar año y mes.');
      return;
    }

    setLoading(true);
    try {
      const res = await postEstadoResultados(form);
      setData(res.data);
      setFiltros({ anio: form.anio, mes: form.mes });
      setShowModal(false);
    } catch (err) {
      handleApiError(err, setError);
    } finally {
      setLoading(false);
    }
  };

  const exportarPDF = async () => {
  try {
    const res = await postPDFEstadoResultados({
      anio: filtros.anio,
      mes: filtros.mes
    });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `estado_resultados_${filtros.anio}_${filtros.mes}.pdf`);
    document.body.appendChild(link);
    link.click();
  } catch (err) {
    handleApiError(err, setError);
  }
};

const exportarExcel = async () => {
  try {
    const res = await postExcelEstadoResultados({
      anio: filtros.anio,
      mes: filtros.mes
    });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `estado_resultados_${filtros.anio}_${filtros.mes}.xlsx`);
    document.body.appendChild(link);
    link.click();
  } catch (err) {
    handleApiError(err, setError);
  }
};

  return (
    <div className="container mt-4">
      <AlertAutoHide message={error} />

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>Seleccionar Mes y Año</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group>
              <Form.Label>Año</Form.Label>
              <Form.Control
                name="anio"
                type="number"
                value={form.anio}
                onChange={handleChange}
                required
              />
            </Form.Group>
            <Form.Group>
              <Form.Label>Mes</Form.Label>
              <Form.Select name="mes" value={form.mes} onChange={handleChange} required>
                <option value="">Seleccione...</option>
                {Array.from({ length: 12 }, (_, i) => (
                  <option key={i + 1} value={i + 1}>
                    {i + 1}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
            <div className="d-grid gap-2 mt-3">
              <Button variant="primary" type="submit" disabled={loading}>
                {loading ? 'Consultando...' : 'Consultar'}
              </Button>
            </div>
          </Form>
        </Modal.Body>
      </Modal>

      {data && (
        <div className="mt-4">
          <div className="d-flex justify-content-between align-items-center">
            <h4>Estado de Resultados</h4>
            <div>
              <Button variant="outline-danger" size="sm" onClick={exportarPDF} className="me-2">
                Exportar PDF
              </Button>
              <Button variant="outline-success" size="sm" onClick={exportarExcel}>
                Exportar Excel
              </Button>
            </div>
          </div>

          <table className="table table-bordered mt-3">
            <thead className="table-light">
              <tr>
                <th colSpan="2">INGRESOS</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data.ingresos.detalle).map(([nombre, valor]) => (
                <tr key={nombre}>
                  <td>{nombre}</td>
                  <td>${parseFloat(valor).toLocaleString('es-CO')}</td>
                </tr>
              ))}
              <tr className="fw-bold">
                <td>Total Ingresos</td>
                <td>${parseFloat(data.ingresos.total).toLocaleString('es-CO')}</td>
              </tr>
            </tbody>

            <thead className="table-light">
              <tr>
                <th colSpan="2">COSTOS DE OPERACIÓN</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data.costos_operacion.detalle).map(([nombre, valor]) => (
                <tr key={nombre}>
                  <td>{nombre}</td>
                  <td>${parseFloat(valor).toLocaleString('es-CO')}</td>
                </tr>
              ))}
              <tr className="fw-bold">
                <td>Total Costos</td>
                <td>${parseFloat(data.costos_operacion.total).toLocaleString('es-CO')}</td>
              </tr>
              <tr className="table-secondary">
                <td><strong>UTILIDAD BRUTA</strong></td>
                <td><strong>${parseFloat(data.utilidad_bruta).toLocaleString('es-CO')}</strong></td>
              </tr>
            </tbody>

            <thead className="table-light">
              <tr>
                <th colSpan="2">GASTOS ADMINISTRATIVOS</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data.gastos_administrativos.detalle).map(([nombre, valor]) => (
                <tr key={nombre}>
                  <td>{nombre}</td>
                  <td>${parseFloat(valor).toLocaleString('es-CO')}</td>
                </tr>
              ))}
              <tr className="fw-bold">
                <td>Total Gastos</td>
                <td>${parseFloat(data.gastos_administrativos.total).toLocaleString('es-CO')}</td>
              </tr>
              <tr className="table-secondary">
                <td><strong>UTILIDAD OPERACIONAL</strong></td>
                <td><strong>${parseFloat(data.utilidad_operacional).toLocaleString('es-CO')}</strong></td>
              </tr>
            </tbody>

            <thead className="table-light">
              <tr>
                <th colSpan="2">OTROS COSTOS</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data.otros_costos.detalle).map(([nombre, valor]) => (
                <tr key={nombre}>
                  <td>{nombre}</td>
                  <td>${parseFloat(valor).toLocaleString('es-CO')}</td>
                </tr>
              ))}
              <tr className="fw-bold">
                <td>Total Otros Costos</td>
                <td>${parseFloat(data.otros_costos.total).toLocaleString('es-CO')}</td>
              </tr>
              <tr className="table-secondary">
                <td><strong>UTILIDAD ANTES DE IMPUESTOS</strong></td>
                <td><strong>${parseFloat(data.utilidad_antes_impuestos).toLocaleString('es-CO')}</strong></td>
              </tr>
            </tbody>

            <thead className="table-light">
              <tr>
                <th colSpan="2">GASTOS POR IMPUESTOS</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data.gastos_impuestos.detalle).map(([nombre, valor]) => (
                <tr key={nombre}>
                  <td>{nombre}</td>
                  <td>${parseFloat(valor).toLocaleString('es-CO')}</td>
                </tr>
              ))}
              <tr className="fw-bold">
                <td>Total Impuestos</td>
                <td>${parseFloat(data.gastos_impuestos.total).toLocaleString('es-CO')}</td>
              </tr>
              <tr className="table-success">
                <td><strong>UTILIDAD NETA</strong></td>
                <td><strong>${parseFloat(data.utilidad_neta).toLocaleString('es-CO')}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default EstadoResultados;
