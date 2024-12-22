'use client';
import React, { useState, useEffect } from 'react';
import Title from '@/app/(customer)/components/title';

/**
 * ViewProducts component fetches and displays a list of products for admin.
 * 
 * This component:
 * - Retrieves an authentication token from cookies to fetch product data from the admin API.
 * - Handles error states and displays an error message if fetching fails.
 * - Maps over the fetched product data to render a table of product items with options to edit.
 *
 * @returns {JSX.Element} A JSX element representing the product list view for admin users.
 */

export default function ViewProducts() {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    cookieStore
      .get('token')
      .then((cookie) =>
        fetch(`/api/cakery/user/admin/Products`, {
          headers: {
            Authorization: `Bearer ${cookie.value}`,
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
        }),
      )
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch products');
        return res.json();
      })
      .then((data) => {
        console.log('products:', data);
        const productsArray = Object.entries(data).map(([key, value]) => ({
          item: decodeURIComponent(key),
          price: value.price,
          product_id: value.product_id || null,
        }));
        setProducts(productsArray);
      })
      .catch((error) => {
        console.error('Error fetching products:', error);
        setError(error.message);
      });
  }, []);

  return (
    <div className="container mt-5">
      <Title>Products Info</Title>
      {error ? (
        <div className="alert alert-danger">Error: {error}</div>
      ) : (
        <div
          className="table-responsive"
          style={{ maxHeight: '400px', overflowY: 'auto' }}
        >
          <table className="table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Price</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {Array.isArray(products) &&
                products.map((product) => (
                  <tr key={product.item}>
                    <td>{product.item}</td>
                    <td>{product.price} EGP</td>
                    <td>
                      {product.item && (
                        <a
                          href={`/admin/editProducts/${product.product_id || encodeURIComponent(product.item)}`}
                          className="btn btn-light"
                          style={{ marginRight: '10px' }}
                          title="Edit Price"
                        >
                          <i className="fa fa-pencil" style={{color:'#f08632'}}></i>
                        </a>
                      )}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
