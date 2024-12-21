'use client';
import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { redirect } from 'next/navigation';

export const addBtnStyle = {
  fontsize: '14px',
  border: 'none',
  borderRadius: '3px',
  background: '#f08632',
  color: 'white',
  height: '30px',
  width: '100px',
  fontFamily: 'Montserrat-Regular , sans-serif, Helvetica',
  position: 'relative',
};

export const AddToCart = async (productid, quantity = 1) => {
  const product = {
    product_id: productid,
    quantity: quantity,
  };

  const cookie = await cookieStore.get('token');
  if (cookie?.value) {
    try {
      const response = await fetch('/api/cakery/user/customer/Cart/Add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${cookie.value}`,
        },
        body: JSON.stringify(product),
      });
      const data = await response.json();
      if (response.ok) {
        console.log(data);
      } else {
        throw data.message;
      }
    } catch (error) {
      console.error(error);
    }
  } else {
    redirect('/signIn');
  }
};
/**
 
 * A card component for each product in the shop page, which displays the product
 * image, name, category, price, rating, and an "Add to cart" button.
 * @param {string} name - The name of the product.
 * @param {number} productid - The ID of the product.
 * @param {string|Image} image - The image of the product. Defaults to `product3`.
 * @param {string} category - The category of the product.
 * @param {number} price - The price of the product.
 * @param {number} [rating=5] - The rating of the product. Defaults to 5.
 * @returns {ReactElement} The product card component.
 */
const ProductCard = ({
  name,
  productid,
  image,
  category,
  price,
  rating = 5,
}) => {
  return (
    <div className="col-lg-3 col-md-6 col-sm-6 ">
      <div className="product__item">
        <div className="product__item__pic">
          <Image
            // layout="responsive"
            // loader={}

            src={image}
            alt={name}
            width={250}
            height={220}
            className="product-img"
          />
          <div className="product__label">
            <span>{category}</span>
          </div>
        </div>
        <div className="product__item__text">
          <h6>
            <Link href={`/product/${productid}`}>{name}</Link>
          </h6>

          <div className="product__item__price">${price} </div>

          <div className="product__item__rating">
            {Array.from({ length: rating }).map((_, index) => (
              <i key={index} className="fa fa-star" style={{ color: 'gold' }} />
            ))}
          </div>
          <div className="d-flex flex-row"></div>
          <div className="cart_add">
            <button
              style={addBtnStyle}
              onClick={() => AddToCart(productid, 1)}
              href="/cart"
            >
              Add to cart
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
