'use client';
import React from 'react';
import Image from 'next/image';
import cart1 from '../img/shop/cart/cart1.jpg';

const OrderItem = ({
  productName,
  orderID,
  name,
  totalPrice,
  quantity,
  status,
  orderDate
}) => (
  <tr>
    <td>
      <h6 className="cart-item__name">
          <Image
            src={cart1}
            alt={`Image of ${productName}`}
            className="cart-item__image"
          />
          <span className="cart-item__name-text">Name : {productName}</span>
          <span className="cart-item__name-text">Quantity : {quantity}</span>


        </h6>
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
