'use client';
import React from 'react';
import Title from '@/app/(customer)/components/title';
import CheckoutInputField from '@/app/(customer)/components/checkoutInput';
import Button from '@/app/(customer)/components/button';
import { useRouter, usePathname } from 'next/navigation';

function EditVoucher() {
    const router = useRouter();
    const pathname = usePathname();

    const slug = decodeURIComponent(pathname);
    const voucher = slug.split('/editVoucher/').pop();
    console.log('Extracted Voucher ID:', voucher);

    const handleEditVoucher = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const newDiscount = parseFloat(formData.get('discountPercentage'));

        try {
            const cookie = await cookieStore.get('token');
            const token = cookie?.value;

            if (!token) {
                console.error('No token found');
                return;
            }
            const response = await fetch(`/api/cakery/user/admin/Vouchers/Edit`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    voucher_code: voucher,
                    discount : newDiscount
                }),
            });

            if (response.ok) {
                console.log('Voucher updated successfully.');
                router.push('/admin/viewVouchers');
            } else {
                console.error('Update failed:', await response.json());
            }
        } catch (error) {
            console.error('Error updating the voucher:', error);
        }
    };

    return (
        <section className="sign-up spad">
            <div className="container">
                <div className="d-flex align-items-center justify-content-between mb-3">
                    <Title>Edit Voucher</Title>
                    <a className="primary-btn" href="/admin/viewVouchers">
                        Go Back
                    </a>
                </div>
                <div className="sign-up__form">
                    <form onSubmit={handleEditVoucher}>
                        <div className="row justify-content-center">
                            <div className="col-lg-11 col-md-12">
                                <div className="row">
                                    <div className="col-md-6 mb-4">
                                    <p>Voucher to be edited: {voucher}</p>
                                        <CheckoutInputField
                                            type="number"
                                            label="Change Discount Percentage"
                                            name="discountPercentage"
                                            placeholder="Enter the New Percentage"
                                            required
                                        />
                                    </div>
                                </div>
                                <div className="d-flex justify-content-center mt-4">
                                    <Button type="submit" className="btn-black">
                                        Update Voucher
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

export default EditVoucher;
