'use client';
import { useState } from 'react';
import Button from '../components/button';
import CheckoutInputField from '../components/checkoutInput';
import Title from '../components/title';

function ForgotPassword() {
  const [email, setEmail] = useState('');
  function sendEmail() {
    fetch;
  }
  return (
    <div className="container pb-5  d-flex flex-column">
      <Title>Forgot Password</Title>
      <CheckoutInputField
        value={email}
        type="email"
        onChange={(e) => setEmail(e.target.value)}
        label={'Enter your Email'}
      />
      <Button classNameProp="w-100">Send Email</Button>
    </div>
  );
}

export default ForgotPassword;
