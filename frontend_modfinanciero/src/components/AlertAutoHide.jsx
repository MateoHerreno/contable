import React, { useEffect, useState } from 'react';

const AlertAutoHide = ({ variant = 'danger', message, duration = 6000 }) => {
  const [visible, setVisible] = useState(!!message);

  useEffect(() => {
    if (message) {
      setVisible(true);
      const timer = setTimeout(() => setVisible(false), duration);
      return () => clearTimeout(timer);
    }
  }, [message, duration]);

  if (!visible) return null;

  return (
    <div className={`alert alert-${variant}`} role="alert">
      {message}
    </div>
  );
};

export default AlertAutoHide;
