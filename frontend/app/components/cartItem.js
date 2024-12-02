'use client';
import React from 'react';
import Image from 'next/image';
import cart1 from '../img/shop/cart/cart1.jpg';


const CartItem = ({ cartid, productid, cartitemid, customcakeid, quantity, price, onRemove }) => (
  <tr>
    <td>
      <h6 ><Image src={cart1} alt="cart1" />{productid}, {customcakeid}</h6>
    </td>
    <td>
      <h6>{price}</h6>
    </td>
    <td>
      <h6>{quantity}</h6>
    </td>
    <td>
      {/* <h6>{total}</h6> */}
    </td>
    <td>
      <button
        onClick={onRemove}
        className="icon_close"
        style={{
          fontSize: '25px',
          backgroundColor: '#F2F2F2',
          width: '40px',
          height: '40px',
          borderRadius: '360px',
          border: 'none',
        }}
      >
      </button>
    </td>
  </tr>
);

export default CartItem;
