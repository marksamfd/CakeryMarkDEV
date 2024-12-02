import React from 'react';

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
