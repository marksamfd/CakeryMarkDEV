import Link from 'next/link';
import React from 'react';

/**
 * A component to display a breadcrumb navigation bar on a page.
 *
 * This component displays a navigation bar with two columns. The first
 * column displays the title of the page, and the second column displays a
 * link to the homepage and the title of the page.
 *
 * @param {{ title: string }} props - The props object, containing the title
 *   of the page.
 *
 * @returns {React.ReactElement} A React element representing the breadcrumb
 *   navigation bar.
 */
function Breadcrumb({ title }) {
  return (
    <div className="breadcrumb-option">
      <div className="container">
        <div className="row">
          <div className="col-lg-6 col-md-6 col-sm-6">
            <div className="breadcrumb__text">
              <h2>{title}</h2>
            </div>
          </div>
          <div className="col-lg-6 col-md-6 col-sm-6">
            <div className="breadcrumb__links">
              <Link href="/">Home</Link>
              <span>{title}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Breadcrumb;
