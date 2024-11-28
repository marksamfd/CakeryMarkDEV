import React from 'react';

function Button({ children, type = 'button', onClick }) {
  return (
    <button type={type} className="site-btn" onClick={onClick}>
      {children}
    </button>
  );
}

export default Button;
