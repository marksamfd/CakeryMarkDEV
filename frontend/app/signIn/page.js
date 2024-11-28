'use client';
import '../styles/style.css';
import Image from 'next/image';
import googleIcon from '@/img/icon/googleIcon.svg';
import Button from '../components/button';
import CheckoutInputField from '../components/checkoutInput';
import Title from '../components/title';

export default function SignIn() {
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
  return (
    <section className="checkout spad">
      <div className="container">
        <Title>Sign In</Title>       
         <div className="checkout__form">
          <form action="#">
            <div className="row justify-content-center">
              <div className="col-lg-8 col-md-6">
                <div className="row">
                  <div className="col-8 mx-auto mb-3">
                    <CheckoutInputField type="email" label="Email" />
                  </div>
                  <div className="col-8 mx-auto mb-3">
                    <CheckoutInputField type="password" label="Password" />
                  </div>
                </div>
                <div className="d-flex flex-column align-items-center mt-4">
                  <Button type="submit">Log In</Button>

                  <button
                    type="button"
                    style={googleStyle} >
              <Image width={20} height={20} src={googleIcon} alt="" />
                    Continue with Google
                  </button>

                  <p style={{fontFamily:'Montserrat', textTransform:'uppercase'}}>Don't have an account? </p>
                  <a
                    href="/sign-up"
                    className="text-primary "
                  >
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
