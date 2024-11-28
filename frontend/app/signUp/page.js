'use client';
import '../styles/style.css';
import Button from '../components/button';
import CheckoutInputField from '../components/checkoutInput';
import Title from '../components/title';

function SignUp() {
  return (
    <section className="sign-up spad">
      <div className="container">
<Title>Create an Account</Title>  
      <div className="sign-up__form">
          <form action="#">
            <div className="row justify-content-center">
              <div className="col-lg-11 col-md-6">
                <div className="row ">
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField type="text" label="First Name" />
                  </div>
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField type="text" label="Last Name" />
                  </div>
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField type="email" label="Email" />
                  </div>
                  <div className="col-md-6 mb-3">
                    <CheckoutInputField type="tel" label="Phone" />
                  </div>
                  <div className="col-md-12 mb-3">
                    <CheckoutInputField
                      type="text"
                      label="Location (Google Maps link)"
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
