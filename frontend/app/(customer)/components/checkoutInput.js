import React from 'react';


const CheckoutInputField = React.forwardRef(function InputField(props, ref) {
  const inputType = props.type || `text`;
  const requiredField = props.requiredfield;
  return (
    <div className="checkout__input">
      <p>
        {props.label}
        {requiredField ? <span>*</span> : ''}
      </p>
      <input
        required={requiredField}
        name={`${props?.name ? props?.name : 'inputddd'}`}
        type={inputType}
        ref={ref}
        {...props}
      />
    </div>
  );
});
export default CheckoutInputField;
