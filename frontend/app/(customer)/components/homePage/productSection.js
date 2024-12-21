import React, { useEffect, useState } from 'react';
import ProductCard from '../productCard';

/**
 * Fetches a list of products from the backend and renders a section
 * containing a row of ProductCard components.
 * @returns {ReactElement} The product section component.
 */
function ProductSection() {
  const [products, setProducts] = useState([]);
  useEffect(() => {
    fetch(`/api/cakery/user/customer/Shop`)
      .then((p) => p.json())
      .then(setProducts);
  }, []);
  return (
    <section className="product spad">
      <div className="container">
        <div className="row">
          {products?.map((product, index) => (
            <ProductCard key={index} {...product} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default ProductSection;
