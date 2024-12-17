'use client';
import React from 'react';
import Image from 'next/image';
import cart1 from '../../img/shop/cart/cart1.jpg';

/**
 * A component that displays a single row in the cart table, including the product name,
 * price, quantity, total, and a remove button.
 *
 * @param {number} cartid - The ID of the cart item.
 * @param {number} productid - The ID of the product.
 * @param {string} productname - The name of the product.
 * @param {number} cartitemid - The ID of the cart item.
 * @param {number} customcakeid - The ID of the custom cake.
 * @param {number} quantity - The quantity of the item in the cart.
 * @param {number} price - The price of the item.
 * @param {number} total - The total price of the item in the cart.
 * @param {Function} onRemove - A function to call when the remove button is clicked.
 */
const CartItem = ({
  cartid,
  productId,
  productname,
  cartitemid,
  customcakeid,
  quantity,
  price,
  total,
  onRemove,
  onIncrease,
  onDecrease,
}) => {
  return (
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
        <div className="d-flex flex-row justify-content-between">
          <span onClick={onIncrease}>-</span>
          <h6>{quantity}</h6>
          <span onClick={onDecrease}>+</span>
        </div>
      </td>
      <td>
        <h6>${total}</h6>
      </td>
      <td>
        <button onClick={onRemove} className="remove-btn">
          <i className="fa fa-times text-danger"></i>
        </button>
      </td>
    </tr>
  );
};

export default CartItem;
