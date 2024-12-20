'use client';
import Button from '../components/button';
import CheckoutInputField from '../components/checkoutInput';
import Title from '../components/title';
import { useActionState, useEffect } from 'react';
import { authenticate, loginWithGoogle } from '@/app/lib/actions';
import { useSearchParams, redirect } from 'next/navigation';
import GoogleBtn from '../components/googleBtn';

/**
 * Renders a sign in form with email and password fields, and a button to
 * authenticate the user.
 *
 * Also renders a link to sign up if the user doesn't have an account yet.
 *
 * @returns {JSX.Element} The sign in form component.
 */
export default function SignIn({ providers }) {
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get('callbackUrl') || '/';
  const googleStyle = {
    width: '500px',
    height: '60px',
    marginBottom: '30px',
    backgroundColor: 'white',
    color: 'black',
    padding: '10px 20px',
    border: '1px solid black',
    borderRadius: '40px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '20px',
    gap: '10px',
  };
  useEffect(() => {
    cookieStore
      .get('token')
      .then((c) => {
        if (c) {
          if (callbackUrl) {
            redirect(callbackUrl);
          }
          return cookieStore.get('role');
        }
      })
      .then((role) => {
        if (role) {
          switch (role) {
            case 'baker':
              redirect('../baker');
              break;
            case 'delivary':
              redirect('../delivery');
              break;
            case 'admin':
              redirect('../admin');
              break;
            default:
              redirect('../');
          }
        }
      });
  });
  const [errorMessage, formAction, isPending] = useActionState(
    authenticate,
    undefined,
  );
  console.log({ providers });
  return (
    <section className="checkout spad">
      <div className="container">
        <Title>Sign In</Title>
        <div className="checkout__form">
          <form action={formAction}>
            <div className="row justify-content-center">
              <div className="col-lg-8 col-md-6">
                <div className="row">
                  <div className="col-8 mx-auto mb-3">
                    <CheckoutInputField
                      type="email"
                      name="email"
                      label="Email"
                    />
                  </div>
                  <div className="col-8 mx-auto mb-3">
                    <CheckoutInputField
                      type="password"
                      name="password"
                      label="Password"
                    />
                    <input
                      type="hidden"
                      name="callbackUrl"
                      value={callbackUrl}
                    />
                  </div>

                  <div className="col-8 d-flex justify-items-center mx-auto mb-3">
                    <GoogleBtn googleCallback={loginWithGoogle} />
                  </div>
                </div>
                <div className="d-flex flex-column align-items-center mt-4">
                  <Button type="submit">Log In</Button>
                  {errorMessage}
                  {/*   <button type="button" style={googleStyle}>
                    <Image width={20} height={20} src={googleIcon} alt="" />
                    Continue with Google {isPending}
                  </button> */}

                  <p
                    style={{
                      fontFamily: 'Montserrat',
                      textTransform: 'uppercase',
                    }}
                  >
                    Don't have an account?{' '}
                  </p>
                  <a href="/signUp" className="text-primary ">
                    SIGN UP
                  </a>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </section>
  );
}
