'use client';
import Button from '../../components/button';
import CheckoutInputField from '../../components/checkoutInput';
import Title from '../../components/title';
import { useActionState, useEffect, useState } from 'react';
import {
  useSearchParams,
  useRouter,
  useParams,
  redirect,
} from 'next/navigation';
// import { useRouter } from 'next/router';
import { signUp as register, editData } from '@/app/lib/actions';

/**
 * Renders a form to sign up a new user.
 *
 * The form includes fields for first name, last name, email, phone, password, confirm password, and location.
 *
 * @returns {JSX.Element} The sign up form component.
 */
function SignUp() {
  const [userData, setUserData] = useState({});
  const searchParams = useSearchParams();
  const params = useParams();

  const callbackUrl = searchParams.get('callbackUrl') || '/';
  const token = params.token;

  console.log(token ? 'editData' : 'register');
  let [state, formAction, isPending] = useActionState(
    token ? editData : register,
    {
      callbackUrl,
    },
  );

  useEffect(() => {
    if (token) {
      fetch(`/api/cakery/user/customer/CheckData`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((res) => res.json())
        .then((json) => {
          setUserData(json.data);
        });
    }
  }, []);

  useEffect(() => {
    if (token && state?.edited) {
      redirect('../');
    }
    if (token && state?.registered) {
      redirect('../login');
    }
  }, [state]);
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
                      defaultValue={token ? userData.firstname : ''}
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField
                      type="text"
                      label="Last Name"
                      name="LastName"
                      defaultValue={token ? userData.lastname : ''}
                    />
                  </div>
                  {!token && (
                    <div className="col-md-6 mb-3">
                      <CheckoutInputField
                        type="email"
                        label="Email"
                        name="Email"
                      />
                    </div>
                  )}
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField
                      type="tel"
                      label="Phone"
                      name="Phone"
                      defaultValue={token ? userData.phonenum : ''}
                    />
                  </div>
                  {!token && (
                    <>
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
                    </>
                  )}
                  <div className="col-md-12 mb-3">
                    <CheckoutInputField
                      type="text"
                      label="Location (Google Maps link)"
                      name="Location"
                      defaultValue={token ? userData.addressgooglemapurl : ''}
                    />
                  </div>
                </div>
                <div className="d-flex flex-column align-items-center mt-4">
                  <Button type="submit" className="btn-black">
                    {token ? 'Save Changes' : 'Sign Up'}
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
