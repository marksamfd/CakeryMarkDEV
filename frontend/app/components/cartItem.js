'use client';
import React from 'react';
import Image from 'next/image';
import cart1 from '../img/shop/cart/cart1.jpg';

const CartItem = ({ cartid, productid, productname, cartitemid, customcakeid, quantity, price, total, onRemove }) => (
  <tr className="cart-item-row">
    <td>
      <h6 className="cart-item__name">
        <Image
          src={cart1}
          alt={`Image of ${productname}`}
          className="cart-item__image"
        />
        <span className="cart-item__name-text">{productname}</span>
      </h6>
    </td>
    <td>
      <h6>${price}</h6>
    </td>
    <td>
      <h6>{quantity}</h6>
    </td>
    <td>
      <h6>${total}</h6>
    </td>
    <td>
      <button
        onClick={onRemove}
        className="remove-btn"
      >
        <i className="fa fa-times text-danger"></i>
      </button>
    </td>
  </tr>
);

export default CartItem;
