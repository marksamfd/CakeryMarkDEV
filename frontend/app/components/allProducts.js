import React from 'react';

/**
 * Displays an ordered list of all items in the cart.
 * @param {object} props
 * @param {array} props.items - an array of objects with name and price
 * @returns {ReactElement} - an ordered list
 */
function AllProducts(props) {
  return (
    <ol className="checkout__total__products">
      {props.items?.length > 0
        ? props.items.map((item) => {
            return (
              <li>
                {item.name} <span>$ {item.price}</span>
              </li>
            );
          })
        : ''}
    </ol>
  );
}

export default AllProducts;
