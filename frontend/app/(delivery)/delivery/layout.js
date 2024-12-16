'use client';
import React from 'react';
import DeliveryHeader from '@/app/(customer)/components/deliveryHeader';
import SmallFooter from '../../(customer)/components/smallFooter';
import '../../styles/barfiller.css';
import '../../styles/bootstrap.min.css';
import '../../styles/elegant-icons.css';
import '../../styles/flaticon.css';
import '../../styles/font-awesome.min.css';
import '../../styles/magnific-popup.css';
import '../../styles/nice-select.css';
import '../../styles/slicknav.min.css';
import '../../styles/style.css';

function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="d-flex flex-column" style={{ minHeight: '100vh' }}>
        <DeliveryHeader />
        <div className="container-fluid flex-grow-1">
          {children}
        </div>
        <SmallFooter />
      </body>
    </html>
  );
}

export default RootLayout;
