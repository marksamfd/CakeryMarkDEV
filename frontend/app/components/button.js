import React from 'react';

function Button({ children, type = 'button', onClick }) {
  return (
    <button type={type} style={{ marginBottom: '30px' }} className="site-btn" onClick={onClick}>
      {children}
    </button>
  );
}

export default Button;
