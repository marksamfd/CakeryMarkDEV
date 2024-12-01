'use client';
import React, { useState, useEffect } from 'react';
import Breadcrumb from '../components/breadcrumb';
import CartItem from '../components/cartItem';

export default function Cart() {
  const [cartItems, setCartItems] = useState([
    // { cartItemId: 1, productId: 1, customCakeId: null, price: 30.0, quantity: 2 },
    // { cartItemId: 2, productId: 2, customCakeId: null, price: 47.0, quantity: 1 },
  ]);
  useEffect(() => {
    cookieStore
      .get('token')
      .then((cookie) => {
        console.log(cookie);
        return fetch(`/api/customer/Cart`, {
          headers: {
            Authorization: `Bearer ${cookie.value}`,
          },
        });
      })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setCartItems(data.cartItems);
      })
      .catch((error) => {
        console.error;
      });
  }, []);

  function RemoveItem(cartItemId) {
    const updatedCart = [];
    for (let i = 0; i < cartItems.length; i++) {
      if (cartItems[i].cartItemId !== cartItemId) {
        updatedCart.push(cartItems[i]);
      }
    }
    setCartItems(updatedCart);
  }

  const calculateTotal = () => {
    let total = 0;
    for (let i = 0; i < cartItems.length; i++) {
      total += cartItems[i].price * cartItems[i].quantity;
    }
    return total;
  };
  return (
    <>
      <Breadcrumb title="Shopping Cart" />
      <section className="shopping-cart spad">
        <div className="container">
          <div className="row">
            <div className="col-lg-8">
              <div className="shopping__cart__table">
                <table>
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th>Price</th>
                      <th>Quantity</th>
                      <th>Total</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {cartItems.map((item) => (
                      <CartItem
                        key={item.cartItemId}
                        productId={item.productId}
                        customCakeId={item.customCakeId}
                        price={item.price}
                        quantity={item.quantity}
                        total={item.price * item.quantity}
                        onRemove={() => RemoveItem(item.cartItemId)}
                      />
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="row">
                <div className="col-lg-6 col-md-6 col-sm-6">
                  <div className="continue__btn">
                    <a href="/shop">Continue Shopping</a>
                  </div>
                </div>
              </div>
            </div>
            <div className="col-lg-4">
              <div className="cart__total">
                <h6>Cart total</h6>
                <ul>
                  <li>
                    Subtotal <span>${calculateTotal()}</span>
                  </li>
                  <li>
                    Total <span>${calculateTotal()}</span>
                  </li>
                </ul>
                <a href="/checkout" className="primary-btn">
                  Proceed to checkout
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
