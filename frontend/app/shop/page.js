'use client';
import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import ProductCard from '../components/productCard';
import Breadcrumb from '../components/breadcrumb';
import customize from '../img/shop/customize.png';
import product1 from '../img/shop/product1.jpg';
import product2 from '../img/shop/product2.jpg';
import product3 from '../img/shop/product3.jpg';
import product4 from '../img/shop/product4.jpg';
import product5 from '../img/shop/product5.jpg';
import product6 from '../img/shop/product6.jpg';
import product7 from '../img/shop/product7.jpg';
import product8 from '../img/shop/product8.jpg';
import product9 from '../img/shop/product9.jpg';
import product10 from '../img/shop/product10.jpg';
import product11 from '../img/shop/product11.jpg';
import product12 from '../img/shop/product12.jpg';



function Shop() {
  const products = [
    { name: 'Dozen Cupcakes', image: product1, category: 'Cupcake', price: 10.0, rating: 5 },
    { name: 'Cookies and Cream', image: product2, category: 'Cupcake', price: 30.0, rating: 4 },
    { name: 'Gluten Free Mini Dozen', image: product3, category: 'Cupcake', price: 31.0, rating: 5 },
    { name: 'Cookie Dough', image: product4, category: 'Cupcake', price: 25.0, rating: 4 },
    { name: 'Vanilla Salted Caramel', image: product5, category: 'Cupcake', price: 5.00, rating: 4 },
    { name: 'German Chocolate', image: product6, category: 'Cupcake', price: 14.00, rating: 5 },
    { name: 'Dulce De Leche', image: product7, category: 'Cupcake', price: 32.00, rating: 5 },
    { name: 'Mississippi Mud', image: product8, category: 'Cupcake', price: 8.00, rating: 3 },
    { name: 'VEGAN/GLUTEN FREE', image: product9, category: 'Cupcake', price: 98.85, rating: 5 },
    { name: 'SWEET CELTICS', image: product10, category: 'Cupcake', price: 5.77, rating: 4 },
    { name: 'SWEET AUTUMN LEAVES', image: product11, category: 'Cupcake', price: 26.41, rating: 4 },
    { name: 'PALE YELLOW SWEET', image: product12, category: 'Cupcake', price: 22.47, rating: 5 },
  ];
  return (
    <>
      <Breadcrumb title="Shop" />
      <section className="shop spad">
        <div className="container">
          <div className="shop__option">
            <div className="row">
              <div className="col-lg-7 col-md-7">
                <div className="shop__option__search">
                  <form action="#">
                    <select>
                      <option value="">Categories</option>
                      <option value="red velvet">Red Velvet</option>
                      <option value="cup cake">Cup Cake</option>
                      <option value="biscuit">Biscuit</option>
                    </select>
                    <input type="text" placeholder="Search" />
                    <button type="submit">
                      <i className="fa fa-search" />
                    </button>
                  </form>
                </div>
              </div>
              <div className="col-lg-5 col-md-5">
                <div className="shop__option__right">
                  <select>
                    <option value="">Default sorting</option>
                    <option value="A-Z">A to Z</option>
                    <option value="1-8">1 - 8</option>
                    <option value="name">Name</option>
                  </select>
                  <a href="#">
                    <i className="fa fa-list" />
                  </a>
                  <a href="#">
                    <i className="fa fa-reorder" />
                  </a>
                </div>
              </div>
            </div>
          </div>
          <div className="row" style={{ justifyContent: 'center'}}>
  <Link href="/customizeCake">
    <div style={{
        display: 'flex',
        justifyContent: 'center'
      
      }}
    >
      <div className="product__item">
        <div
          className="product__item__pic set-bg"
          style={{ backgroundImage: `url(${customize.src})`,width: '350px', height: '300px' }}
        >
        </div>
        <div className="product__item__text">
          <h6
            style={{
              color: '#F08632',
              fontSize: '25px',
              fontFamily: 'Montserrat',
              fontWeight: '800',
              textTransform: 'uppercase',
              lineHeight: '19.20px',
              wordWrap: 'break-word',
            }}
          >
            Customize Your<br /><br /> Cake!
          </h6>
        </div>
      </div>
    </div>
  </Link>
</div>


<div className="row">
            {products.map((product, index) => (
              <ProductCard key={index} {...product} />
            ))}
          </div>
          <div className="shop__last__option">
            <div className="row">
              <div className="col-lg-6 col-md-6 col-sm-6">
                <div className="shop__pagination">
                  <a href="#">1</a>
                  <a href="#">2</a>
                  <a href="#">3</a>
                  <a href="#">
                    <span className="arrow_carrot-right" />
                  </a>
                </div>
              </div>
              <div className="col-lg-6 col-md-6 col-sm-6">
                <div className="shop__last__text">
                  <p>Showing 1-9 of 10 results</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default Shop;
