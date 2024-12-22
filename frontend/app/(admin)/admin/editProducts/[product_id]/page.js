'use client';
import React from 'react';
import Title from '@/app/(customer)/components/title';
import CheckoutInputField from '@/app/(customer)/components/checkoutInput';
import Button from '@/app/(customer)/components/button';
import { useRouter, usePathname } from 'next/navigation';

/**
 * EditProduct component allows for editing the details of a specific product.
 * 
 * It retrieves the product identifier from the URL, provides a form for updating
 * the product's price, and performs the update via an API call.
 * 
 * Utilizes a secure token for authentication. Upon successful update, the user
 * is redirected to the product view page.
 * 
 * @returns {JSX.Element} A section containing a form to edit the product details.
 */

function EditProduct() {
    const router = useRouter();

    const pathname = usePathname();
    const decoded = decodeURIComponent(pathname);
    console.log(decoded);
    const slug = decoded.split('/editProducts/').pop();
    console.log(slug);
    

    const handleEditProduct = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);

        const price = parseFloat(formData.get('Price'));

        const updatedProduct = {
            price,
            product_id: slug || 0, 
            rawItem: slug || '',
        };

        try {
            const cookie = await cookieStore.get('token');
            const token = cookie?.value;

            if (!token) {
                console.error('No token found');
                return;
            }

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
                console.error(' update failed', await response.json());
            }
        } catch (error) {
            console.error('error updating the product:', error);
        }
    };

    return (
        <section className="sign-up spad">
            <div className="container">
                <div className="d-flex align-items-center justify-content-between mb-3">
                    <Title>Edit Item</Title>
                    <a className="primary-btn" href="/admin/viewProducts">
                        Go Back
                    </a>
                </div>
                <div className="sign-up__form">
                    <form onSubmit={handleEditProduct}>
                        <div className="row justify-content-center">
                            <div className="col-lg-11 col-md-12">
                                <div className="row">
                                    <div className="col-md-12 mt-4 mb-4">
                                        <p>Item to be edited: {slug}</p>
                                        <CheckoutInputField
                                            name="Price"
                                            type="number"
                                            step="0.01"
                                            label="New Price"
                                            placeholder="Enter new price"
                                            required
                                        />
                                    </div>
                                    
                                </div>

                                <div className="d-flex justify-content-center mt-4">
                                    <Button type="submit" className="btn-black" >
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
