'use client';
import Button from '../components/button';
import CheckoutInputField from '../components/checkoutInput';
import Title from '../components/title';
import { useActionState } from 'react';
import { useSearchParams } from 'next/navigation';

import { signUp as register } from '@/app/lib/actions';

/**
 * Renders a form to sign up a new user.
 *
 * The form includes fields for first name, last name, email, phone, password, confirm password, and location.
 *
 * @returns {JSX.Element} The sign up form component.
 */
function SignUp() {
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get('callbackUrl') || '/';

  const [state, formAction, isPending] = useActionState(register, {
    callbackUrl,
  });
  console.log(state);
  return (
    <section className="sign-up spad">
      <div className="container">
        <Title>Create an Account</Title>
        <div> {state?.error}</div>
        <div className="sign-up__form">
          <form action={formAction}>
            <div className="row justify-content-center">
              <div className="col-lg-11 col-md-6">
                <div className="row ">
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField
                      name="FirstName"
                      type="text"
                      label="First Name"
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField
                      type="text"
                      label="LastName"
                      name="LastName"
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField
                      type="email"
                      label="Email"
                      name="Email"
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField type="tel" label="Phone" name="Phone" />
                  </div>
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField
                      type="password"
                      label="Password"
                      name="password"
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField
                      type="password"
                      label="Confirm Password"
                      name="confirmPassword"
                    />
                  </div>
                  <div className="col-md-12 mb-3">
                    <CheckoutInputField
                      type="text"
                      label="Location (Google Maps link)"
                      name="Location"
                    />
                  </div>
                </div>
                <div className="d-flex flex-column align-items-center mt-4">
                  <Button type="submit" className="btn-black">
                    Sign Up
                  </Button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </section>
  );
}
export default SignUp;
