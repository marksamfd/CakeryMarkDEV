'use client';
import React, { useState, useEffect } from 'react';
import Title from '@/app/(customer)/components/title';

export default function ViewVouchers() {
  const [vouchers, setVouchers] = useState({});
  const [error, setError] = useState(null);
useEffect(() => {
    cookieStore
      .get('token')
      .then((cookie) =>
        fetch(`/api/cakery/user/admin/Vouchers`, {
          headers: {
            Authorization: `Bearer ${cookie.value}`,
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
        }),
      )
      .then((res) => res.json())
      .then((data) => {
        console.log(' vouchers:', data);
        setVouchers(data); 
      })
      .catch((error) => console.error('error fetching vouchers:', error));
  }, []);


  const handleDelete = async (voucherCode) => {
    try {
      const cookie = await cookieStore.get('token');
      const res = await fetch(`/api/cakery/user/admin/Vouchers/Delete`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${cookie.value}`,
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ voucher_code: voucherCode }),
      });
  
      if (!res.ok) {
        console.error('Failed to delete voucher');
        return;
      }
      console.log(`The voucher: ${voucherCode} deleted.`);
  
  setVouchers((prevVouchers) => {
        const updatedVouchers = { ...prevVouchers };
        delete updatedVouchers[voucherCode];
        return updatedVouchers;
      });
    } catch (error) {
      console.error('cannot delete voucher:', error);
    }
  };

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between align-items-center mt-3 mb-3">
                    <Title>Vouchers</Title>
                    <a
                        href={`/admin/addVoucher`}
                        className="primary-btn"
                    >
                        Add New Voucher
                    </a>
                </div>
      {error ? (
        <div className="alert alert-danger mt-3">Error: {error}</div>
      ) : (
        <div
          className="table-responsive"
          style={{ maxHeight: '400px', overflowY: 'auto' }}
        >
          <table className="table">
            <thead>
              <tr>
                <th>Voucher Code</th>
                <th>Discount Percentage</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(vouchers).map(([voucherCode, details]) => (
                <tr key={voucherCode}>
                  <td>{voucherCode}</td>
                  <td>{details.discount_percentage}%</td>
                  <td>
                    <a
                      href={`/admin/editVoucher/${voucherCode}`}
                      className="btn btn-light"
                      style={{ marginRight: '10px' }}
                      title='Edit Voucher'
                    >
                      <i className="fa fa-pencil" style={{color:'#f08632'}}></i>
                    </a>
                    <button
                      onClick={() => handleDelete(voucherCode)}
                      className="btn btn-light" title='Delete Voucher'>
                      <i className="fa fa-trash" style={{color:'darkred' }} ></i>
                    </button>
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
