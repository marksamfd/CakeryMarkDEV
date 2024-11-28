import React from 'react';

function Breadcrumb({title}) {
  return (
    <div class="breadcrumb-option">
      <div class="container">
        <div class="row">
          <div class="col-lg-6 col-md-6 col-sm-6">
            <div class="breadcrumb__text">
              <h2>{title}</h2>
            </div>
          </div>
          <div class="col-lg-6 col-md-6 col-sm-6">
            <div class="breadcrumb__links">
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
