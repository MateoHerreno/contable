import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ConfirmModal = ({ show, onHide, onConfirm, title = "¿Confirmar acción?", body = "", confirmText = "Sí, continuar" }) => (
  <Modal show={show} onHide={onHide}>
    <Modal.Header closeButton>
      <Modal.Title>{title}</Modal.Title>
    </Modal.Header>
    <Modal.Body>{body}</Modal.Body>
    <Modal.Footer>
      <Button variant="secondary" onClick={onHide}>Cancelar</Button>
      <Button variant="danger" onClick={onConfirm}>{confirmText}</Button>
    </Modal.Footer>
  </Modal>
);

export default ConfirmModal;
