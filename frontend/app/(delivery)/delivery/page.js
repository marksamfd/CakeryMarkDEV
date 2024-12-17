'use client';
import React, { useState, useEffect } from 'react';
import Breadcrumb from '@/app/(customer)/components/breadcrumb';
import NavDropdown from 'react-bootstrap/NavDropdown';

export default function DeliveryOrders() {
  const [orderItems, setOrderItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [DeliveryName, setDeliveryName] = useState('');

//need an endpoint here for the name
//   useEffect(() => {
//     const cookie = cookieStore.get('name'); 
//     if (cookie) {
//       setCustomerName(cookie.value);
//     }
//   }, []);

  useEffect(() => {
    cookieStore
      .get('token')
      .then((cookie) =>
        fetch(`/api/user/delivery/order_details`, {
          headers: {
            Authorization: `Bearer ${cookie.value}`,
          },
        })
      )
      .then((res) => res.json())
      .then((data) => {
        setOrderItems(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching orders:', error);
        setLoading(false);
      });
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 0: return 'blue';    //out for delivery
      case 1: return 'green';   //Delivered
      case 2: return 'red';     //cancelled
      default: return 'black';
    }
  };

  const handleChangeOrderStatus = (orderId, newStatus) => {
    cookieStore
      .get('token')
      .then((cookie) =>
        fetch('/api/user/delivery/Order_Status', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${cookie.value}`,
          },
          body: JSON.stringify({
            OrderId: orderId,
            Status: newStatus,
          }),
        })
      )
      .then((res) => res.json())
      .then(() => {
        setOrderItems((prevState) =>
          prevState.map((item) =>
            item.orderID === orderId ? { ...item, status: newStatus } : item
          )
        );
      })
      .catch((error) => console.error('error while updating order status:', error));
  };
  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <Breadcrumb title={`Welcome, ${DeliveryName}`} />
      <div className="breadcrumb-option">
        <div className="container">
          <div className="row">
            <div className="col-lg-6 col-md-6 col-sm-6">
              <div className="breadcrumb__text font-size">
                <h2>Your Delivery Orders</h2>
              </div>
            </div>
          </div>
        </div>
      </div>

      <section className="shopping-cart spad">
        <div
          className="container-fluid"
          style={{ display: 'flex', justifyContent: 'center', padding: '20px' }}
        >
          <div style={{ width: '100%', maxWidth: '1200px', overflowX: 'auto' }}>
            <table
              className="order-table"
              style={{
                width: '100%',
                textAlign: 'center',
              }}
            >
              <thead>
                <tr>
                  <th>Order</th>
                  <th>Number of Items</th>
                  <th>Customer Name</th>
                  <th>Phone</th>
                  <th>Location</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {orderItems.map((item) => (
                  <tr key={item.orderID}>
                    <td>{item.orderID}</td>
                    <td>{item.numberOfItemsinOrder}</td>
                    <td>{item.customerName}</td>
                    <td>
                      <a href={`tel:${item.phone}`} style={{ color: 'blue' }}>
                        {item.phone}
                      </a>
                    </td>
                    <td>{item.location}</td>
                    <td>
                      <NavDropdown
                        title={
                          <span style={{ color: getStatusColor(item.status) }}>
                            {item.status === 0
                              ? 'In Delivery'
                              : item.status === 1
                              ? 'Delivered'
                              : 'Cancelled'}
                          </span>
                        }
                        id={`status-dropdown-${item.orderID}`}
                      >
                        <NavDropdown.Item
                          onClick={() => handleChangeOrderStatus(item.orderID, 0)}
                        >
                          In Delivery
                        </NavDropdown.Item>
                        <NavDropdown.Item
                          onClick={() => handleChangeOrderStatus(item.orderID, 1)}
                        >
                          Delivered
                        </NavDropdown.Item>
                        <NavDropdown.Item
                          onClick={() => handleChangeOrderStatus(item.orderID, 2)}
                        >
                          Cancelled 
                        </NavDropdown.Item>
                      </NavDropdown>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </>
  );
}
