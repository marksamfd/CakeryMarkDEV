'use client';
import { useState } from 'react';
import Button from '../components/button';
import CheckoutInputField from '../components/checkoutInput';
import Title from '../components/title';
import { redirect } from 'next/navigation';

function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  function sendEmail() {
    setError('s');
    fetch(`/api/cakery/user/customer/ResetPassword/email`).then((req) => {
      if (req.ok) {
        redirect('/');
      } else {
        setError('Email does not Exist');
      }
    });
  }
  return (
    <div className="container pb-5  d-flex flex-column">
      <Title>Forgot Password</Title>
      <p>{error}</p>
      <CheckoutInputField
        value={email}
        type="email"
        onChange={(e) => setEmail(e.target.value)}
        label={'Enter your Email'}
        requiredField={true}
      />
      <Button classNameProp="w-100" onClick={sendEmail}>
        Send Email
      </Button>
    </div>
  );
}

export default ForgotPassword;
