import React from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

const EntityModal = ({
  show,
  onHide,
  onSubmit,
  title,
  children,
  loading,
  submitText = 'Guardar',
}) => {
  return (
    <Modal show={show} onHide={onHide}>
      <Form onSubmit={onSubmit}>
        <Modal.Header closeButton>
          <Modal.Title>{title}</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          {children}
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={onHide}>
            Cancelar
          </Button>
          <Button variant="primary" type="submit" disabled={loading}>
            {loading ? 'Guardando...' : submitText}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default EntityModal;
