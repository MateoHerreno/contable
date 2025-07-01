import React, { useEffect, useState } from 'react';
import { postEstadoResultados } from '../../services/estadoResultadosService';
import { handleApiError } from '../../services/handleApiError';
import AlertAutoHide from '../../components/AlertAutoHide';
import { Button, Modal, Form } from 'react-bootstrap';

const EstadoResultados = () => {
  const [showModal, setShowModal] = useState(true);
  const [form, setForm] = useState({ anio: '', mes: '' });
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
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
      setShowModal(false);
    } catch (err) {
      handleApiError(err, setError);
    } finally {
      setLoading(false);
    }
  };

  const renderSeccion = (titulo, items = []) => (
    <div className="mb-3">
      <h5>{titulo}</h5>
      <ul>
        {items.map((item, idx) => (
          <li key={idx}>{item.nombre}: ${parseFloat(item.valor).toLocaleString('es-CO')}</li>
        ))}
      </ul>
    </div>
  );

  return (
    <div className="container mt-4">
      <h3>Estado de Resultados</h3>

      <AlertAutoHide message={error} />

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>Seleccionar Mes y Año</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group>
              <Form.Label>Año</Form.Label>
              <Form.Control name="anio" type="number" value={form.anio} onChange={handleChange} required />
            </Form.Group>
            <Form.Group>
              <Form.Label>Mes</Form.Label>
              <Form.Select name="mes" value={form.mes} onChange={handleChange} required>
                <option value="">Seleccione...</option>
                {Array.from({ length: 12 }, (_, i) => (
                  <option key={i + 1} value={i + 1}>{i + 1}</option>
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
          {renderSeccion('INGRESOS', data.ingresos)}
          {renderSeccion('COSTOS DE OPERACIÓN', data.costos)}
          <h5>UTILIDAD BRUTA: ${parseFloat(data.utilidad_bruta).toLocaleString('es-CO')}</h5>

          {renderSeccion('GASTOS ADMINISTRATIVOS', data.gastos)}
          <h5>UTILIDAD OPERACIONAL: ${parseFloat(data.utilidad_operacional).toLocaleString('es-CO')}</h5>

          {renderSeccion('OTROS COSTOS', data.otros_costos)}
          <h5>UTILIDAD ANTES DE IMPUESTOS: ${parseFloat(data.utilidad_antes_impuestos).toLocaleString('es-CO')}</h5>

          {renderSeccion('GASTOS POR IMPUESTOS', data.impuestos)}
          <h4 className="text-success">UTILIDAD NETA: ${parseFloat(data.utilidad_neta).toLocaleString('es-CO')}</h4>
        </div>
      )}
    </div>
  );
};

export default EstadoResultados;