'use client';
import { resetPassswordForm } from '@/app/lib/actions';
import Button from '../../components/button';
import CheckoutInputField from '../../components/checkoutInput';
import Title from '../../components/title';
import { useParams } from 'next/navigation';
import { useActionState } from 'react';

/**
 * Renders a form to reset a user's password with a provided token.
 *
 * The form is a column of fields, with the token passed in as a hidden field.
 *
 * On form submission, the `resetPassswordForm` action is called with the form data.
 *
 * The component will display any response from the server as a heading above the form.
 *
 * @returns {JSX.Element} The reset password form component.
 */
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
