'use client';
import Button from '../components/button';
import CheckoutInputField from '../components/checkoutInput';
import Title from '../components/title';
import { useActionState, useEffect } from 'react';
import { authenticate, loginWithGoogle } from '@/app/lib/actions';
import { useSearchParams, redirect } from 'next/navigation';
import GoogleBtn from '../components/googleBtn';
import {
  isAdminPage,
  isBakerPage,
  isDeliveryPage,
  isUserPage,
} from '@/authUtils';
import Link from 'next/link';

/**
 * Renders a sign in form with email and password fields, and a button to
 * authenticate the user.
 *
 * Also renders a link to sign up if the user doesn't have an account yet.
 *
 * @returns {JSX.Element} The sign in form component.
 */
export default function SignIn() {
  const searchParams = useSearchParams();
  const callbackUrl = searchParams?.get('callbackUrl')
    ? new URL(searchParams?.get('callbackUrl')).pathname
    : '';
  const googleError = searchParams?.get('googleError');

  const [errorMessage, formAction, isPending] = useActionState(
    authenticate,
    undefined,
  );
  useEffect(() => {
    if (searchParams)
      cookieStore
        .get('token')
        .then((c) => {
          if (c) {
            if (
              (isAdminPage(callbackUrl) &&
                cookieStore.get('role') == 'admin') ||
              (isDeliveryPage(callbackUrl) &&
                cookieStore.get('role') == 'delivery') ||
              (isBakerPage(callbackUrl) &&
                cookieStore.get('role') == 'baker') ||
              (isUserPage(callbackUrl) && cookieStore.get('role') == 'customer')
            ) {
              redirect(callbackUrl);
            } else {
              redirect('/');
            }
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
  }, [errorMessage]);

  if (errorMessage?.loggedIn) redirect('../');
  console.log(errorMessage?.loggedIn);
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
                    <p
                      style={{
                        fontFamily: 'Montserrat',
                        textTransform: 'uppercase',
                      }}
                    >
                      Forgot your Password?{' '}
                      <Link href="/forgotPassword" className="text-primary ">
                        Click Here
                      </Link>
                    </p>
                    <input
                      type="hidden"
                      name="callbackUrl"
                      value={callbackUrl}
                    />
                  </div>
                </div>
                <div className="d-flex flex-column align-items-center mt-4">
                  <Button type="submit">Log In</Button>
                  <div className="d-flex justify-items-center mx-auto mb-3">
                    <GoogleBtn googleCallback={loginWithGoogle} />
                  </div>
                  {errorMessage}
                  {/* 
                  {errorMessage || googleError
                    ? 'An error occured Sign in with Google, Try again Later or Sign up'
                    : ''} */}
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
                    Don&apos;t have an account?{' '}
                  </p>
                  <Link href="/signUp" className="text-primary ">
                    SIGN UP
                  </Link>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </section>
  );
}
