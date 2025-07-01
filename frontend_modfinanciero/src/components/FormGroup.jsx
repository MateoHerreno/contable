import React from 'react';
import { Form } from 'react-bootstrap';

const FormGroup = ({ label, name, value, onChange, type = 'text', as = 'input', children, ...rest }) => {
  return (
    <Form.Group className="mb-3">
      <Form.Label>{label}</Form.Label>
      <Form.Control
        name={name}
        value={value}
        onChange={onChange}
        type={type}
        as={as}
        {...rest} // Aquí es donde pasa "multiple", "required", etc.
      >
        {children}
      </Form.Control>
    </Form.Group>
  );
};

export default FormGroup;
