'use client';
import Image from 'next/image';
import { useEffect, useRef, useState } from 'react';
import React from 'react';

/**
 * SmallFooter component
 *
 * This component renders the footer section of the website with the
 * copyright information.
 *
 * @returns {JSX.Element} The footer component
 */
function SmallFooter() {
  return (
    <>
      <footer className="footer set-bg" >
        <div className="copyright">
              <div className="col-lg-7">
                <p className="copyright__text text-white">
                  {/* Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. */}
                  <a href="https://colorlib.com" target="_blank">
                    Colorlib
                  </a>
                  {/* Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. */}
                </p>
              </div>
              <div className="col-lg-5"></div>
          </div>
      </footer>
    </>
  );
}

export default SmallFooter;
