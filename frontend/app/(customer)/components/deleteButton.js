'use client';
import React from 'react';

/**
 * Makes a DELETE request to the server to delete a staff user by email and role.
 * @param {string} userEmail - The email of the user to delete.
 * @param {string} role - The role of the user to delete.
 * @param {string} token - The authentication token to use for the request.
 * @returns {Promise} A promise of the response from the server.
 */
async function handleDeleteClick(userEmail, role, token) {
    const response = await fetch(`/api/cakery/user/admin/Staff/Delete`, {
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
    if (response.ok) {
        alert('User deleted successfully');
        window.location.reload(); //
    } else {
        alert('Error deleting user');
    }
}
const DeleteButton = ({ userEmail, role, token }) => {
    return (
        <button
            onClick={() => handleDeleteClick(userEmail, role, token)}
            className="btn btn-light"
            style={{ marginRight: '10px' }}
            title='Delete User'
        >
            <i className="fa fa-trash" style={{ color: 'red' }}></i>
        </button>
    );
};

export default DeleteButton;
