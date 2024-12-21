'use client';
import React from 'react';
import Title from '@/app/(customer)/components/title';
import CheckoutInputField from '@/app/(customer)/components/checkoutInput';
import Button from '@/app/(customer)/components/button';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

function AddUser() {
  const router = useRouter();

  const handleAddUser = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);

    const firstName = formData.get('FirstName');
    const lastName = formData.get('LastName');
    const email = formData.get('Email');
    const phone = formData.get('Phone');
    const role = formData.get('role');
    const password = formData.get('password');

    const newUser = {
      FirstName: firstName,
      LastName: lastName,
      Email: email,
      Phone: phone,
      Role: role,
      Password: password,
    };
    const cookieStore = document.cookie.split(';').reduce((acc, cookie) => {
      const [key, value] = cookie.trim().split('=');
      acc[key] = value;
      return acc;
    }, {});

    const token = cookieStore.token;

    await fetch(`/api/cakery/user/admin/Staff/Add`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        email: newUser.Email,
        password: newUser.Password,
        firstname: newUser.FirstName,
        lastname: newUser.LastName,
        phone: newUser.Phone,
        role: newUser.Role,
      }),
    });
    router.push('/admin/manageUsers/staff');
  };

  return (
    <section className="sign-up spad">
      <div className="container">
        <div className="d-flex align-items-center justify-content-between mb-3">
          <Title>Add New User</Title>
          <Link className="primary-btn" href="/admin/manageUsers/staff">
            Go Back
          </Link>
        </div>
        <div className="sign-up__form">
          <form onSubmit={handleAddUser}>
            <div className="row justify-content-center">
              <div className="col-lg-11 col-md-12">
                <div className="row">
                  <div className="col-md-6 mb-4">
                    <CheckoutInputField
                      name="FirstName"
                      type="text"
                      label="First Name"
                      required
                    />
                  </div>
                  <div className="col-md-6 mb-4">
                    <CheckoutInputField
                      type="text"
                      label="Last Name"
                      name="LastName"
                      required
                    />
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-6 mb-4">
                    <CheckoutInputField
                      type="email"
                      label="Email"
                      name="Email"
                      required
                    />
                  </div>
                  <div className="col-md-6 mb-4">
                    <CheckoutInputField
                      type="tel"
                      label="Phone"
                      name="Phone"
                      required
                    />
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-6 mb-4">
                    <CheckoutInputField
                      type="text"
                      label="User Role"
                      name="role"
                      required
                    />
                  </div>
                  <div className="col-md-6 mb-4">
                    <CheckoutInputField
                      type="password"
                      label="Password"
                      name="password"
                      required
                    />
                  </div>
                </div>

                <div className="d-flex justify-content-center mt-4">
                  <Button type="submit" className="btn-black">
                    Add
                  </Button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </section>
  );
}

export default AddUser;
