'use client';
import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import ProductCard from '../components/productCard';
import Breadcrumb from '../components/breadcrumb';
// imgs :
import customize from '../../img/shop/customize.png';
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

/**
 * Shop component fetches product data from an API and displays a list of products.
 *
 * The component:
 * - Fetches an authentication token from cookies and uses it to request product data from the `/api/customer/shop` endpoint.
 * - Stores the fetched product data in the state and maps over it to render individual `ProductCard` components.
 * - Displays a search form and sorting options for filtering products.
 * - Provides a UI to navigate through different categories and customize cakes.
 * - Includes pagination controls for navigating through product pages.
 */
function Shop() {
  const [allProducts, setAllProducts] = useState([]);
  const [allCategories, setAllCategories] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  useEffect(() => {
    cookieStore
      .get('token')
      .then((cookie) => {
        console.log(cookie);
        return fetch(`/api/cakery/user/customer/Shop`, {
          headers: {
            Authorization: `Bearer ${cookie.value}`,
          },
        });
      })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setAllProducts(data);
        setFilteredProducts(data);
        setAllCategories(new Set(data.map((e) => e.category)));
      })
      .catch(console.error);
  }, []);
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
                    <select
                      onChange={(event) => {
                        console.log(event.target.value.length);
                        if (event.target.value.length > 0) {
                          setFilteredProducts(
                            allProducts.filter((e) =>
                              e.category
                                .toLowerCase()
                                .includes(event.target.value.toLowerCase()),
                            ),
                          );
                        } else {
                          setFilteredProducts(allProducts);
                        }
                      }}
                    >
                      <option value="">Categories</option>
                      {[...allCategories.values()].map((e, i) => (
                        <option key={`kat-${i}`} value={e}>
                          {e}
                        </option>
                      ))}
                    </select>
                    <input
                      type="text"
                      placeholder="Search"
                      onInput={(event) => {
                        console.log(event.target.value.length);
                        if (event.target.value.length > 0) {
                          setFilteredProducts(
                            allProducts.filter((e) =>
                              e.name.toLowerCase().includes(event.target.value),
                            ),
                          );
                        } else {
                          setFilteredProducts(allProducts);
                        }
                      }}
                    />
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
          <div className="row">
            <div className="col-lg-3 col-md-6 col-sm-6">
              <Link href="/customizeCake">
                <div className="product__item">
                  <div
                    className="product__item__pic set-bg"
                    style={{
                      backgroundImage: `url(${customize.src})`,
                      height: '250px',
                      backgroundSize: 'cover',
                      backgroundPosition: 'center',
                    }}
                  ></div>
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
                        textAlign: 'center',
                      }}
                    >
                      Customize Your
                      <br />
                      Cake!
                    </h6>
                  </div>
                </div>
              </Link>
            </div>
            {filteredProducts.map((products, index) => (
              <ProductCard key={index} {...products} />
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
