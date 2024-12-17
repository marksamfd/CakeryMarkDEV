'use client';
import CheckoutInputField from './checkoutInput';
import AllProducts from './allProducts';
// import { cookies } from 'next/headers';
import Button from './button';
import { useRef, useState } from 'react';

/**
 * Displays a summary of the cart items and their total cost.
 * The summary also includes a form to input a voucher code, and a button to place the order.
 * @returns {JSX.Element} A JSX element representing the checkout summary.
 * @example
 * <CheckoutSummary />
 */
function CheckoutSummary() {
  const [items, setItems] = useState([]);
  const voucherRef = useRef();
  cookieStore
    .get('token')
    .then((token) => {
      return fetch(`api/cakery/user/customer/Cart`, {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });
    })
    .then((res) => res.json())
    .then((data) => {
      setItems(data);
    });

  console.log(items);
  let total = 0;
  items.forEach((item) => {
    total += item.price * 1.0 * item.quantity;
  });
  function PlaceOrder() {
    fetch(`api/cakery/user/customer/Checkout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token.value}`,
      },
      body: { voucher: voucherRef.current.value },
    });
  }
  return (
    <div className="col-lg-4 col-md-6">
      <div className="checkout__order">
        <h6 className="order__title">Your order</h6>
        <div className="checkout__order__products">
          Product <span>Total</span>
        </div>
        <AllProducts items={items} />
        <CheckoutInputField
          requiredfield={false}
          label={'Voucher'}
          ref={voucherRef}
        />
        <ul className="checkout__total__all">
          <li>
            Total <span>${total}</span>
          </li>
        </ul>

        <Button onClick={PlaceOrder}>PLACE ORDER</Button>
      </div>
    </div>
  );
}

export default CheckoutSummary;
