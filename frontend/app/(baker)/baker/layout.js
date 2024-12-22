'use client';
import React from 'react';
import BakerHeader from '../../(customer)/components/bakerHeader';
import '../../styles/barfiller.css';
import '../../styles/bootstrap.min.css';
import '../../styles/elegant-icons.css';
import '../../styles/flaticon.css';
import '../../styles/font-awesome.min.css';
import '../../styles/magnific-popup.css';
import '../../styles/nice-select.css';
import '../../styles/slicknav.min.css';
import '../../styles/style.css';

/**
 * RootLayout component
 *
 * This component renders the layout for the pages of the baker application.
 *
 * @param {JSX.Element} children The children components to render inside the layout.
 * @returns {JSX.Element} The layout component.
 */
function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={``}>
        <BakerHeader />
        <div className="container-fluid">{children}</div>
      </body>
    </html>
  );
}

export default RootLayout;
{
}
