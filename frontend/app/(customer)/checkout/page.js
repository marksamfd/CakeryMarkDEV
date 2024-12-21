'use client';
import CheckoutInputField from '../components/checkoutInput';
import CheckoutSummary from '../components/checkoutSummary';
/**
 * The checkout page.
 *
 * This page renders a form with fields for billing and card information, and
 * a summary of the order.
 *
 * @returns {JSX.Element} The checkout page component.
 */
export default function checkout() {
  return (
    <section className="checkout spad">
      <div className="container">
        <div className="checkout__form">
          <form action="#">
            <div className="row">
              <div className="col-lg-8 col-md-6">
                <h6 className="checkout__title">Checkout</h6>
                {/* <div className="row">
                  <div className="col-lg-6">
                    <CheckoutInputField label={'Card Number'} />
                  </div>
                  <div className="col-lg-3">
                    <CheckoutInputField
                      type="number"
                      label={'Expiration Month'}
                    />
                  </div>
                  <div className="col-lg-3">
                    <CheckoutInputField
                      type="number"
                      label={'Expiration Date'}
                    />
                  </div>
                </div>
                <CheckoutInputField label={'CVV'} /> */}
              </div>
              <CheckoutSummary />
            </div>
          </form>
        </div>
      </div>
    </section>
  );
}
