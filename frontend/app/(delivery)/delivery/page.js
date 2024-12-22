'use client';
import React, { useState, useEffect } from 'react';
import NavDropdown from 'react-bootstrap/NavDropdown';

/**
 * Displays the orders assigned to the delivery person and allows them to
 * update the status of the orders to "out_for_delivery" or "delivered".
 *
 * @returns {JSX.Element} The DeliveryOrders component.
 */
function DeliveryOrders() {
  const [orderItems, setOrderItems] = useState([]);
  const [deliveryName, setDeliveryName] = useState('');

  useEffect(() => {
    cookieStore
    .get('token')
      .then((cookie) => {
        return fetch(`/api/cakery/user/delivery/name`, {
          headers: {
            Authorization: `Bearer ${cookie.value}`,
          },
        });
      })
      .then((res) => res.json())
      .then((data) => {
        setDeliveryName(data.name);
      })
      .catch((err) => {
        console.error('Error fetching name:', err);
      });
  }, []);

  useEffect(() => {
    cookieStore
      .get('token')
      .then((cookie) => {
        return fetch(`/api/cakery/user/delivery/orders`, {
          headers: {
            Authorization: `Bearer ${cookie.value}`,
          },
        });
      })
      .then((res) => res.json())
      .then((data) => {
        console.log('Fetched orders:', data); 
        setOrderItems(data.orders);
      })
      .catch((err) => {
        console.error('Error fetching orders:', err);
      });
  }, []);
  

 

  const getStatusColor = (status) => {
    switch (status) {
      case 'out_for_delivery': return 'blue';
      case 'delivered': return 'green';
      
      default: return '#f08632';
    }
  };
  const handleChangeOrderStatus = async (orderId, newStatus) => {
    try {
      const token = await cookieStore.get('token');
      const response = await fetch(`/api/cakery/user/delivery/orders/change_status`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token.value}`,
        },
        body: JSON.stringify({ order_id: orderId, status: newStatus }),
      });
      setOrderItems((prevState) =>
        prevState.map((item) =>
          item.order_id === orderId ? { ...item, status: newStatus } : item
        )
      );
    } catch (err) {
      console.error('Error updating status:', err);
    }
  };
  
  
  return (
    <>
      <div className="breadcrumb-option">
        <div className="container">
          <div className="row">
            <div className="col-lg-6 col-md-6 col-sm-6">
              <div className="breadcrumb__text font-size">
                <h2> Welcome, {deliveryName}</h2>
                <br />
                <h2>Your Orders to Deliver :</h2>
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
          <div style={{ width: '100%', maxWidth: '1200px'}}>
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
                  <th>Total Price</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
              {orderItems.map((item, index) => (
  <tr key={`${item.customerName}-${index}`}>
    <td>{index + 1}</td>
    <td>{item.numberOfItems}</td>
    <td>{item.customerName}</td>
    <td><a href={`tel:${item.phone}`}>{item.phone}</a></td>
    <td>
      <a href={item.location} target="_blank" rel="noopener noreferrer">
        View Location
      </a>
    </td>
    <td>${item.price}</td>
    <td>
      <NavDropdown
        title={<span style={{ color: getStatusColor(item.status) }}>{item.status}</span>}
        id={`status-dropdown-${index}`}
      >
        <NavDropdown.Item onClick={() => handleChangeOrderStatus(item.order_id, 'out_for_delivery')}>
          Out for Delivery
        </NavDropdown.Item>
        <NavDropdown.Item onClick={() => handleChangeOrderStatus(item.order_id, 'delivered')}>
          Delivered
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

export default DeliveryOrders;
