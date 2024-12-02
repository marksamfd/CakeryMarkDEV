import CheckoutInputField from '../components/checkoutInput';
import CheckoutSummary from '../components/checkoutSummary';
export default function checkout() {
  return (
    <section className="checkout spad">
      <div className="container">
        <div className="checkout__form">
          <form action="#">
            <div className="row">
              <div className="col-lg-8 col-md-6">
                <h6 className="checkout__title">Billing Details</h6>
                <div className="row">
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
                <CheckoutInputField label={'CVV'} />
              </div>
              <CheckoutSummary />
            </div>
          </form>
        </div>
      </div>
    </section>
  );
}
