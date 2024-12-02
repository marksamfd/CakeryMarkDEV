'use client';
import React from 'react';
import Image from 'next/image';
import cart1 from '../img/shop/cart/cart1.jpg';

const OrderItem = ({
  orderId,
  name,
  totalPrice,
  status,
  orderDate
}) => (
  <tr>
    <td>
      <Image src={cart1}/>
      <h6>{orderDate}</h6>
    </td>
    <td>
      <h6 style={{ color: 'green'}}>{status} </h6>
    </td>
    <td>
      <h6>{totalPrice} EGP</h6>
    </td>
  </tr>
);

export default OrderItem;
