'use client';
import React from 'react';
import Title from '@/app/(customer)/components/title';
import CheckoutInputField from '@/app/(customer)/components/checkoutInput';
import Button from '@/app/(customer)/components/button';
import { useRouter } from 'next/navigation';

function AddVoucher() {
    const router = useRouter();
    const handleAddVoucher = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const voucherCode = formData.get('VoucherCode');
        const discountPercentage = formData.get('discountPercentage');
        
        const cookieStore =  document.cookie.split(';').reduce((acc, cookie) => {
          const [key, value] = cookie.trim().split('=');
          acc[key] = value;
          return acc;
          }, {});

        const token = cookieStore.token;

          await fetch(`/api/cakery/user/admin/Vouchers/Add`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              voucher_code: voucherCode,
              discount: discountPercentage
            }),
        });
        router.push('/admin/viewVouchers');
    };


    return (
        <section className="sign-up spad">
            <div className="container">
               <div className="d-flex align-items-center justify-content-between mb-3">
                  <Title>Add New Voucher</Title>
                  <a className="primary-btn"  href="/admin/viewVouchers">
                     Go Back
                   </a>
               </div>
                <div className="sign-up__form">
                    <form onSubmit={handleAddVoucher}>
                        <div className="row justify-content-center">
                            <div className="col-lg-11 col-md-12">
                                <div className="row">
                                    <div className="col-md-6 mb-4">
                                        <CheckoutInputField
                                            name="VoucherCode"
                                            type="text"
                                            label="Voucher Code"
                                            placeholder="Enter the New Code"
                                            required
                                        />
                                    </div>
                                    <div className="col-md-6 mb-4">
                                        <CheckoutInputField
                                            type="number"
                                            label="Discount Percentage"
                                            name="discountPercentage"
                                            placeholder="Enter the Percentage"
                                            required
                                        />
                                    </div>
                                </div>                                
                                </div>
                                <div className="d-flex justify-content-center mt-4">
                                        <Button type="submit" className="btn-black" >
                                            Add
                                        </Button>
                                </div>
                            </div>
</form>
                </div>
            </div>
        </section>
    );
}

export default AddVoucher;