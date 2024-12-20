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
          <span className="cart-item__name-text">
            {productname ? productname : 'Custom Cake'}
          </span>
        </h6>
      </td>
      <td>
        <h6>${price}</h6>
      </td>
      <td>
        <div className="d-flex flex-row justify-content-between">
          <button onClick={onDecrease}
          className='btn btn-light' title='decrease item'>
            <i className="fa fa-minus "style={{color:'#f08632' }}></i>
          </button>
          <h6 className='mt-2'>{quantity}</h6>
          <button onClick={onIncrease}
          className='btn btn-light' title='Add item'>
            <i className="fa fa-plus"style={{color:'#f08649' }}></i>
          </button>
        </div>
      </td>
      <td>
        <h6>${total}</h6>
      </td>
      <td>
        <button onClick={onRemove}
        className="btn btn-light" title='Remove item'>
        <i className="fa fa-trash" style={{color:'red' }} ></i>  
              </button>
      </td>
    </tr>
  );
};

export default CartItem;
