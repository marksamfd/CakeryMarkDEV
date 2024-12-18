'use client';
import React from 'react';
import Title from '@/app/(customer)/components/title';
import CheckoutInputField from '@/app/(customer)/components/checkoutInput';
import Button from '@/app/(customer)/components/button';
import { useRouter } from 'next/navigation';

function EditProduct() {
    const router = useRouter();

    const handleEditProduct = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);

        const price = parseFloat(formData.get('Price'));
        const productId = parseInt(formData.get('ProductId'));
        const rawItem = formData.get('RawItem');

        const updatedProduct = {
            price,
            product_id: product_Id,
            rawItem: rawItem 
        };

        const cookieStore = document.cookie.split(';').reduce((acc, cookie) => {
            const [key, value] = cookie.trim().split('=');
            acc[key] = value;
            return acc;
        }, {});

        const token = cookieStore.token;

        try {
            const response = await fetch(`/api/cakery/user/admin/Products/edit`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(updatedProduct),
            });

            if (response.ok) {
                router.push('/admin/viewProducts');
            } else {
                console.error('Failed to update:', await response.json());
            }
        } catch (error) {
            console.error('Error updating the product:', error);
        }
    };

    return (
        <section className="sign-up spad">
            <div className="container">
                <div className="d-flex align-items-center justify-content-between mb-3">
                    <Title>Edit Product</Title>
                    <a className="primary-btn" href="/admin/manageProducts">
                        Go Back
                    </a>
                </div>
                <div className="sign-up__form">
                    <form onSubmit={handleEditProduct}>
                        <div className="row justify-content-center">
                            <div className="col-lg-11 col-md-12">
                                <div className="row">
                                    <div className="col-md-6 mb-4">
                                        <CheckoutInputField
                                            name="Price"
                                            type="number"
                                            step="0.01"
                                            label="Price (EGP)"
                                            required
                                        />
                                    </div>
                                    <div className="col-md-6 mb-4">
                                        <CheckoutInputField
                                            type="number"
                                            label="Product ID"
                                            name="ProductId"
                                            required
                                        />
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="col-md-12 mb-4">
                                        <CheckoutInputField
                                            type="text"
                                            label="Raw Item (Optional)"
                                            name="RawItem"
                                        />
                                    </div>
                                </div>

                                <div className="d-flex justify-content-center mt-4">
                                    <Button type="submit" className="btn-black">
                                        Update
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

export default EditProduct;
