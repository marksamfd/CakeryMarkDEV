import React from 'react';
import ProductCard from '../productCard';
import product1 from '../../img/shop/product1.jpg';
import product2 from '../../img/shop/product2.jpg';
import product3 from '../../img/shop/product3.jpg';
import product4 from '../../img/shop/product4.jpg';
import product5 from '../../img/shop/product5.jpg';
import product6 from '../../img/shop/product6.jpg';
import product7 from '../../img/shop/product7.jpg';
import product8 from '../../img/shop/product8.jpg';
import product9 from '../../img/shop/product9.jpg';
import product10 from '../../img/shop/product10.jpg';
import product11 from '../../img/shop/product11.jpg';
import product12 from '../../img/shop/product12.jpg';

function ProductSection() {
  const products = [
    {
      name: 'Dozen Cupcakes',
      image: product1,
      category: 'Cupcake',
      price: 10.0,
      rating: 5,
    },
    {
      name: 'Cookies and Cream',
      image: product2,
      category: 'Cupcake',
      price: 30.0,
      rating: 4,
    },
    {
      name: 'Gluten Free Mini Dozen',
      image: product3,
      category: 'Cupcake',
      price: 31.0,
      rating: 5,
    },
    {
      name: 'Cookie Dough',
      image: product4,
      category: 'Cupcake',
      price: 25.0,
      rating: 4,
    },
    {
      name: 'Vanilla Salted Caramel',
      image: product5,
      category: 'Cupcake',
      price: 5.0,
      rating: 4,
    },
    {
      name: 'German Chocolate',
      image: product6,
      category: 'Cupcake',
      price: 14.0,
      rating: 5,
    },
    {
      name: 'Dulce De Leche',
      image: product7,
      category: 'Cupcake',
      price: 32.0,
      rating: 5,
    },
    {
      name: 'Mississippi Mud',
      image: product8,
      category: 'Cupcake',
      price: 8.0,
      rating: 3,
    },
  ];
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
