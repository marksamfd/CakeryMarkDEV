import CheckoutInputField from './checkoutInput';
import AllProducts from './allProducts';

function CheckoutSummary() {
  const items = [{ name: 'Red Velvet', price: '500' }];
  let total = 0;
  items.forEach((item) => {
    total += item.price * 1.0;
  });
  return (
    <div className="col-lg-4 col-md-6">
      <div className="checkout__order">
        <h6 className="order__title">Your order</h6>
        <div className="checkout__order__products">
          Product <span>Total</span>
        </div>
        <AllProducts items={items} />
        <CheckoutInputField requiredField={false} label={'Voucher'} />
        <ul className="checkout__total__all">
          <li>
            Total <span>${total}</span>
          </li>
        </ul>
        <button type="submit" className="site-btn">
          PLACE ORDER
        </button>
      </div>
    </div>
  );
}

export default CheckoutSummary;
