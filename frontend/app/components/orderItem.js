'use client';
import React from 'react';
import Image from 'next/image';
import cart1 from '../img/shop/cart/cart1.jpg';

const OrderItem = ({
  orderId,
  totalPrice,
  status,
  orderDate,
  deliveryDate,
}) => (
  <tr>
    <td>
      <Image src={cart1.src} alt="cart1" />
      <h6>{orderId} , {orderDate}, {deliveryDate}</h6>
    </td>
    <td>
      <h6>{status}</h6>
    </td>
    <td>
      <h6>{totalPrice}</h6>
    </td>
  </tr>
);

export default OrderItem;
