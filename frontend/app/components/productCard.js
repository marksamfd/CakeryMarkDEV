'use client';
import React from 'react';
import Image from 'next/image';

const ProductCard = ({ name, image, category, price, rating }) => {
  return (
    <div className="col-lg-3 col-md-6 col-sm-6 ">
      <div className="product__item">
        <div className="product__item__pic">
          <Image
            src={image}
            alt={name}
            width={300}
            height={300}
            className="product-img"
          />
          <div className="product__label">
            <span>{category}</span>
          </div>
        </div>
        <div className="product__item__text">
          <h6>
            <a href="#">{name}</a>
          </h6>

          <div className="product__item__price">${price} </div>

          <div className="product__item__rating">
            {Array.from({ length: rating }).map((_, index) => (
              <i key={index} className="fa fa-star" style={{ color: 'gold' }} />
            ))}
          </div>
          <div className="d-flex flex-row"></div>
          <div className="cart_add">
            <a href="#">Add to cart</a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
