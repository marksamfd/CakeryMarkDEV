'use client';
import React, { useState, useEffect } from 'react';
import Breadcrumb from '../components/breadcrumb';
import OrderItem from '../components/orderItem';
import { useRouter } from 'next/navigation';
import CheckoutInputField from '../components/checkoutInput';
import Button from '../components/button';

/**
 * Displays the customer's orders and allows them to confirm the delivery of
 * delivered orders by providing an OTP.
 *
 * @returns {JSX.Element} The My Orders page.
 */
function CustomerOrders() {
  const [orderItems, setOrderItems] = useState([]);
  const [otp, setOtp] = useState('');
  const [verifyingOrder, setVerifyingOrder] = useState(null);
  const [token, setToken] = useState(null);
  const router = useRouter();
  useEffect(() => {
    cookieStore
      .get('token')
      .then((cookie) =>
        fetch(`/api/cakery/user/customer/Orders`, {
          headers: {
            Authorization: `Bearer ${cookie.value}`,
          },
        })
      )
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setOrderItems(data);
      })
      .catch((error) => console.error('Error fetching orders:', error));
  }, []);

  console.log(orderItems);
  const handleVerifyOTP = async (orderId) => {
    setVerifyingOrder(orderId);
    try {
      if (!token) {
        throw new Error('Token not found');
      }
      const response = await fetch(`/api/cakery/user/customer/VerifyOTP`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          otp_code: otp,
        }),
      });

      if (!response.ok) {
        const message = await response.json();
        throw new Error(message.error);
      }
      const data = await response.json();
      console.log(data);
      setOrderItems((prev) =>
        prev.map((item) =>
          item.orderID === orderId ? { ...item, status: 'confirmed' } : item
        )
      );
      setOtp('');
      router.refresh();
    } catch (error) {
      console.log('Error verifying OTP:', error);
    } finally {
      setVerifyingOrder(null);
    }
  };

  const handleOtpChange = (e) => {
    setOtp(e.target.value);
  };

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
                      <th>    </th>
                      <th>   </th>
                    </tr>
                  </thead>
                  <tbody>
                    {Array.isArray(orderItems) ? (
                      orderItems?.map((item) => (
                        <tr key={item.orderID}>
                          <td>
                            <OrderItem
                              productName={item.items[0].productName}
                              orderId={item.orderID}
                              quantity={item.items[0].quantity}
                              totalPrice={item.totalPrice}
                              orderDate={item.orderDate}
                            />
                          </td>
                          <td>{item.status}</td>
                          <td>${item.totalPrice}</td>
                          <td> </td>
                          <td>
                            {item.status === 'delivered' &&
                              (verifyingOrder === item.orderID ? (
                                <Button disabled>verifying...</Button>
                              ) : (
                                <>
                                  <CheckoutInputField
                                    type="text"
                                    label="OTP"
                                    name="otp"
                                    value={otp}
                                    onChange={handleOtpChange}
                                  />
                                  <Button
                                    onClick={() =>
                                      handleVerifyOTP(item.orderID)
                                    }
                                  >
                                    Confirm with OTP
                                  </Button>
                                </>
                              ))}
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan="4">{orderItems.message}</td>
                      </tr>
                    )}
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
export default CustomerOrders;
