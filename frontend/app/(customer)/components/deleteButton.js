'use client';  
import React from 'react';
async function handleDeleteClick(userEmail, role, token) {
    await fetch(`/api/cakery/user/admin/Staff/Delete`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: userEmail,  
        role: role
      }),
      
    });
    console.log(userEmail,role);

  }
const DeleteButton = ({ userEmail, role, token }) => {
  return (
    <button
      onClick={() => handleDeleteClick(userEmail, role, token)}
      className="btn btn-light"
      style={{ marginRight: '10px' }}
    >
      <i className="fa fa-trash" style={{ color: 'red' }}></i>
    </button>
  );
};

export default DeleteButton;
