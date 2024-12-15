'use client';
/**
 * A basic button component.
 *
 * @param {React.ReactNode} children - The label of the button
 * @param {string} [type=button] - The type of the button. One of "button", "submit", or "reset"
 * @param {React.MouseEventHandler<HTMLButtonElement>} [onClick] - A callback fired when the button is clicked
 */
function Button({ children, type = 'button', onClick, classNameProp }) {
  return (
    <button
      type={type}
      style={{ marginBottom: '30px' }}
      className={'site-btn ' + classNameProp}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

export default Button;
