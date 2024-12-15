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
        ? props.items.map((item, i) => {
            return (
              <li key={`product-${i}`}>
                {item.productname}{' '}
                <span className="blockquote-footer">
                  $ {item.price} X {item.quantity}
                </span>
                <span>$ {item.price * 1 * item.quantity}</span>
              </li>
            );
          })
        : ''}
    </ol>
  );
}

export default AllProducts;
