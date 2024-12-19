'use client';
import { useState, useEffect } from 'react';
import Breadcrumb from '../components/breadcrumb';
import CartItem from '../components/cartItem';


/**
 * Displays the customer's cart and allows them to modify its contents.
 * Retrieves the customer's cart from the server and displays the items in a
 * table. The customer can remove items from the cart, increase or decrease the
 * quantity of an item, or proceed to checkout.
 *
 * @returns {JSX.Element} The Shopping Cart page.
 */

export default function Cart() {
  const [cartItems, setCartItems] = useState([]);
  
  useEffect(() => {
    cookieStore
      .get('token')
      .then((cookie) =>
        fetch(`/api/cakery/user/customer/Cart`, {
          headers: {
            Authorization: `Bearer ${cookie.value}`,
          },
        }),
      )
      .then((res) => res.json())
      .then((data) => {
        console.log(data.items);
        setCartItems(data.items);
      })
      .catch((error) => console.error('Error fetching cart:', error));
  }, []);

  function incOrDec(productId, action, pos) {
    cookieStore
      .get('token')
      .then((cookie) =>
        fetch(`/api/cakery/user/customer/Cart/Increment`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${cookie.value}`,
          },
          body: JSON.stringify({
            action,
            product_id: productId,
          }),
        }),
      )
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        let tmpCart = [...cartItems];
        tmpCart[pos].quantity = data[0].new_quantity * 1;
        setCartItems(tmpCart);
      })
      .catch((error) => console.error('Error fetching cart:', error));
  }

  async function RemoveItem(productid, quantity) {
    try {
      const cookie = await cookieStore.get('token');
      const response = await fetch('/api/cakery/user/customer/Cart/Remove', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${cookie.value}`,
        },
        body: JSON.stringify({
          product_id: productid,
          quantity: quantity,
        }),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        setCartItems(prevItems => prevItems.filter(item => item.productid !== productid));
      } else {
        console.error('Failed to delete item');
      }
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  }
  
/**
   * Calculates the total price of items in the cart.
   *
   * Iterates through each item in the cart and multiplies the price
   * by the quantity for each item, accumulating the result in the total.
   *
   * @returns {number} The total price of all items in the cart.
   */  
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
                    {Array.isArray(cartItems) &&
                      cartItems.map((item, pos) => (
                        <CartItem
                          key={item.productid}
                          productname={item.productname}
                          productId={item.productid}
                          customCakeId={item.customcakeid}
                          price={item.price}
                          quantity={item.quantity}
                          total={item.price * item.quantity}
                          onRemove={() => 
                            RemoveItem(item.productid, item.quantity)}
                          onIncrease={() =>
                             incOrDec(item.productid, 'increment', pos)}
                          onDecrease={() => 
                            incOrDec(item.productid, 'decrement', pos)}
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
