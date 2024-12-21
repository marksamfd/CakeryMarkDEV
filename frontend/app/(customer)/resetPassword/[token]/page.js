'use client';
import { resetPassswordForm } from '@/app/lib/actions';
import Button from '../../components/button';
import CheckoutInputField from '../../components/checkoutInput';
import Title from '../../components/title';
import { useParams } from 'next/navigation';
import { useActionState } from 'react';

function resetPassword() {
  const token = useParams().token;

  const [state, formAction, pending] = useActionState(resetPassswordForm);

  return (
    <div className="container">
      <Title>Reset your Password</Title>
      <h2>{state}</h2>
      <from action={formAction} className="d-flex flex-column">
        <CheckoutInputField name={'password'} label={'Password'} />
        <CheckoutInputField
          name={'confirmPassword'}
          label={'Confirm Password'}
        />
        <input type="hidden" defaultValue={token} />
        <Button type={'submit'} classNameProp={'w-100'}>
          Submit
        </Button>
      </from>
    </div>
  );
}

export default resetPassword;
