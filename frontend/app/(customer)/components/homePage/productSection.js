import React from 'react';
import ProductCard from '../productCard';

import product1 from '../../../img/shop/product1.jpg';
import product2 from '../../../img/shop/product2.jpg';
import product3 from '../../../img/shop/product3.jpg';
import product4 from '../../../img/shop/product4.jpg';
import product5 from '../../../img/shop/product5.jpg';
import product6 from '../../../img/shop/product6.jpg';
import product7 from '../../../img/shop/product7.jpg';
import product8 from '../../../img/shop/product8.jpg';
import product9 from '../../../img/shop/product9.jpg';
import product10 from '../../../img/shop/product10.jpg';
import product11 from '../../../img/shop/product11.jpg';
import product12 from '../../../img/shop/product12.jpg';

/**
 * Fetches a list of products from the backend and renders a section
 * containing a row of ProductCard components.
 * @returns {ReactElement} The product section component.
 */
async function ProductSection() {
  console.log('backend', process.env.BACKEND);
  const productsReq = await fetch(`/api/cakery/user/customer/Shop`);
  const products = await productsReq.json();

  return (
    <section className="product spad">
      <div className="container">
        <div className="row">
          {products.map((product, index) => (
            <ProductCard key={index} {...product} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default ProductSection;
