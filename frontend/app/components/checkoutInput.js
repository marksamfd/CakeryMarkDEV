import React from 'react';
const CheckoutInputField = React.forwardRef((props, ref) => {
  const inputType = props.type || `text`;
  const requiredField = props.requiredField || true;
  return (
    <div className="checkout__input">
      <p>
        {props.label}
        {requiredField ? <span>*</span> : ''}
      </p>
      <input
        required={requiredField}
        name={`${props?.name}`}
        type={inputType}
        ref={ref}
      />
    </div>
  );
});
export default CheckoutInputField;
