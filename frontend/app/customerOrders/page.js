'use client';
import React, { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import Breadcrumb from '../components/breadcrumb';
import OrderItem from '../components/orderItem';

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
        })
      )
      .then((res) => res.json())
      .then((data) => {
        console.log(data.orderItems);
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
                <table>
                  <thead>
                    <tr>
                      <th>Order</th>
                      <th>Status</th>
                      <th>Total</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {orderItems.map((item) => (
                      <OrderItem
                        key={item.orderId}
                        orderId={item.orderId}
                        totalPrice={item.totalPrice}
                        status={item.status } 
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