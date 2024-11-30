import React from 'react';

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
              <a href="./index.html">Home</a>
              <span>{title}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Breadcrumb;
