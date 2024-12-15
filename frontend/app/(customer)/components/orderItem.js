'use client';
import React from 'react';
import Image from 'next/image';
import cart1 from '../../img/shop/cart/cart1.jpg';

/**
 * A component that displays a single row in the orders table, including the product name, quantity, total price, and status.
 *
 * @param {string} productName - The name of the product.
 * @param {number} orderID - The ID of the order.
 * @param {string} name - The name of the user who placed the order.
 * @param {number} totalPrice - The total price of the order.
 * @param {number} quantity - The quantity of the product in the order.
 * @param {string} status - The status of the order.
 * @param {string} orderDate - The date on which the order was placed.
 * @returns {ReactElement} The component.
 */
const OrderItem = ({
  productName,
  orderID,
  name,
  totalPrice,
  quantity,
  status,
  orderDate,
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
      <h6 style={{ color: 'green' }}>{status} </h6>
    </td>
    <td>
      <h6>{totalPrice} EGP</h6>
    </td>
  </tr>
);

export default OrderItem;
