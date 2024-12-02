'use client';
import React, { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import Breadcrumb from '../components/breadcrumb';
import OrderItem from '../components/orderItem';

/**
 * CustomerOrders component.
 *
 * This component is used to display the list of orders made by the customer.
 *
 * @returns {ReactElement} The CustomerOrders component.
 */
export default function CustomerOrders() {
  const [orderItems, setOrderItems] = useState([]);

  useEffect(() => {
    cookieStore
      .get('token')
      .then((cookie) =>
        fetch(`/api/customer/orders`, {
          headers: {
            Authorization: `Bearer ${cookie.value}`,
          },
        }),
      )
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setOrderItems(data);
      })
      .catch((error) => console.error('Error fetching orders:', error));
  }, []);

  return (
    <>
      <Breadcrumb title="My Orders" />
      <section className="shopping-cart spad">
        <div className="container">
          <div className="row">
            <div className="col-lg-8">
              <div className="shopping_cart_table">
                <table className="order-table">
                  <thead>
                    <tr>
                      <th>Order</th>
                      <th>Status</th>
                      <th>Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orderItems.map((item) => (
                      <OrderItem
                        key={item.orderID}
                        productName={item.items[0].productName}
                        orderId={item.orderID}
                        quantity={item.items[0].quantity}
                        totalPrice={item.totalPrice}
                        status={item.status}
                        orderDate={item.orderDate}
                      />
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
