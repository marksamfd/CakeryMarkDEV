'use client';
import React from 'react';
import AdminHeader from '@/app/(customer)/components/adminHeader';
import SmallFooter from '@/app/(customer)/components/smallFooter';
import '@/app/styles/barfiller.css';
import '@/app/styles/bootstrap.min.css';
import '@/app/styles/elegant-icons.css';
import '@/app/styles/flaticon.css';
import '@/app/styles/font-awesome.min.css';
import '@/app/styles/magnific-popup.css';
import '@/app/styles/nice-select.css';
import '@/app/styles/slicknav.min.css';
import '@/app/styles/style.css';

function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={``}>
        <AdminHeader pos={'Admin'} />
        <div className="container-fluid h-100">{children}</div>
        <SmallFooter />
      </body>
    </html>
  );
}

export default RootLayout;
{
}
