import React from 'react';
import Title from '@/app/(customer)/components/title';
import { cookies } from 'next/headers';
import DeleteButton from '@/app/(customer)/components/deleteButton';
import Link from 'next/link';
import Image from 'next/image';

/**
 * ManageUsers is a Next.js server-side rendered page that displays a list of users in a table.
 * The page fetches the list of users from the backend API based on the userType parameter in the URL.
 * If the userType parameter is 'customer', the page fetches the list of customers from the backend API.
 * If the userType parameter is not 'customer', the page fetches the list of staff from the backend API.
 * The page renders a table with columns for name, phone, and role (if userType is not 'customer').
 * The page also renders a button to add a new user if userType is not 'customer'.
 * The page uses the DeleteButton component to render a delete button for each user in the table.
 * The page uses the generatePlaceholderImageUrl function to generate a placeholder image URL for each user in the table.
 * The page uses the Title component to render the title of the page.
 * The page uses the Link component to render a link to the add user page if userType is not 'customer'.
 * @param {Object} params - The parameters passed to the page, including the userType parameter.
 * @param {string} params.userType - The type of user to display in the table, either 'customer' or 'staff'.
 */
async function ManageUsers({ params }) {
  const { userType } = params;
  const cookieStore = cookies();
  const token = cookieStore.get('token');

  let users = [];
  if (userType === 'customer') {
    users = await fetch(
      `${process.env.backend}/cakery/user/admin/ViewCustomers`,
      {
        headers: {
          Authorization: `Bearer ${token.value}`,
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
      },
    ).then((res) => res.json());
  } else {
    users = await fetch(`${process.env.backend}/cakery/user/admin/Staff/View`, {
      headers: {
        Authorization: `Bearer ${token.value}`,
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    }).then((res) => res.json());

    if (users && typeof users === 'object') {
      users = Object.values(users);
    }
  }
  // the staff is returned obj,
  //while the customers are in arr, so I converted the staff obj into arr
  if (userType === 'customer') {
    users = Array.isArray(users)
      ? users.map((user) => ({
          ...user,
          role: 'Customer',
        }))
      : [];
  } else {
    users = Array.isArray(users)
      ? users.map((user) => ({
          ...user,
          name: user.name,
          email: user.email,
          phone: user.phone,
          role: user.role,
        }))
      : [];
  }

  const filteredUsers = users.filter((user) =>
    userType === 'customer'
      ? user.role === 'Customer'
      : user.role !== 'Customer',
  );
  function generatePlaceholderImageUrl(name) {
    const firstLetter = name.charAt(0).toUpperCase();
    return `https://placehold.co/30x30/f08632/ffffff?text=${firstLetter}`;
  }

  return (
    <div className="container mt-5">
      <Title>
        {userType === 'customer' ? 'Your Customers' : 'Manage Staff'}
      </Title>

      {userType !== 'customer' && (
        <div className="d-flex justify-content-between align-items-center mt-3 mb-3">
          <Title>Listed Users</Title>
          <Link href={`/admin/addUser`} className="primary-btn">
            Add User
          </Link>
        </div>
      )}
      <div
        className="table-responsive"
        style={{ maxHeight: '400px', overflowY: 'auto' }}
      >
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              {userType !== 'customer' && <th>Role</th>}
              <th>Phone</th>
              {userType !== 'customer' && <th></th>}
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map((user, i) => (
              <tr key={user.email}>
                <td>
                  <div className="d-flex align-items-center">
                    <Image
                      src={generatePlaceholderImageUrl(user.name)}
                      className="rounded-circle mr-2"
                      style={{
                        width: '30px',
                        height: '30px',
                        marginRight: '10px',
                      }}
                    />
                    <div>
                      <div>{user.name}</div>
                      <small className="text-muted">{user.email}</small>
                    </div>
                  </div>
                </td>
                {userType !== 'customer' && <td>{user.role}</td>}
                <td>{user.phone}</td>
                {userType !== 'customer' && (
                  <td>
                    <DeleteButton
                      userEmail={user.email}
                      role={user.role}
                      token={token.value}
                    />
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ManageUsers;
