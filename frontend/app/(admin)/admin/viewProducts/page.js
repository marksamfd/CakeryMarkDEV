'use client';
import React, { useState, useEffect } from 'react';
import Title from '@/app/(customer)/components/title';

export default function ViewProducts() {
  const [products, setProducts] = useState([]);

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
      .then((res) => res.json())
      .then((data) => {
        console.log('Fetched products:', data);
        setProducts(data); 
      })
      .catch((error) => console.error('Error fetching products:', error));
  }, []);

  return (
    <div className="container mt-5">
      <Title>Products Info</Title>
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
                <tr key={product.product_id}>
                  <td>
                    <div className="d-flex align-items-center">
                      <div>{product.name}</div>
                    </div>
                  </td>
                  <td>{product.price} EGP</td>
                  <td>
                    <a
                      href={`/admin/editProduct/${product.product_id}`}
                      className="btn btn-light"
                      style={{ marginRight: '10px' }}
                    >
                      <i className="fa fa-pencil"></i>
                    </a>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
