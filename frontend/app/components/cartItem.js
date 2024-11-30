'use client';
import React from 'react';

const CartItem = ({ productId, customCakeId, price, quantity,total, onRemove }) => (
  <tr>
    <td>
      <h6>{productId}, {customCakeId}</h6>
    </td>
    <td>
      <h6>{price}</h6>
    </td>
    <td>
      <h6>{quantity}</h6>
    </td>
    <td>
      <h6>{total}</h6>
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
