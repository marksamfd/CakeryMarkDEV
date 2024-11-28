"use client";
import Image from "next/image";
import footer_bg from "@/img/footer_bg.jpg";
import footer_logo from "@/img/footer_logo.png";
import { useEffect, useRef, useState } from "react";
import React from 'react'

 function FooterNav(){
    const currentYear = new Date().getFullYear();
    return<>
    <footer className="footer set-bg" style={{ backgroundImage: `url(${footer_bg.src})` }}>
  <div className="container">
    <div className="row">
      <div className="col-lg-4 col-md-6 col-sm-6">
        <div className="footer__widget">
          <h6>WORKING HOURS</h6>
          <ul>
            <li>Monday - Friday: 08:00 am – 08:30 pm</li>
            <li>Saturday: 10:00 am – 16:30 pm</li>
            <li>Sunday: 10:00 am – 16:30 pm</li>
          </ul>
        </div>
      </div>
      <div className="col-lg-4 col-md-6 col-sm-6">
        <div className="footer__about">
          <div className="footer__logo">
            <a href="#">
                <Image src={footer_logo} alt="" width={250} height={250}/>
            </a>
          </div>
          <p> Welcome to our Cakery, where every cake is crafted with love and passion!
            Explore our menu, and let us make your cake dreams come true!</p>
          <div className="footer__social">
            <a href="#">
              <i className="fa fa-facebook" />
            </a>
            <a href="#">
              <i className="fa fa-twitter" />
            </a>
            <a href="#">
              <i className="fa fa-instagram" />
            </a>
            <a href="#">
              <i className="fa fa-youtube-play" />
            </a>
          </div>
        </div>
      </div>
      <div className="col-lg-4 col-md-6 col-sm-6">
        <div className="footer__newslatter">
          <h6>Subscribe</h6>
          <p>Get latest updates and offers.</p>
          <form action="#">
            <input type="text" placeholder="Email" />
            <button type="submit">
              <i className="fa fa-send-o" />
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div className="copyright">
    <div className="container">
      <div className="row">
        <div className="col-lg-7">
          <p className="copyright__text text-white">
            {/* Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. */}
            <a href="https://colorlib.com" target="_blank">
              Colorlib
            </a>
            {/* Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. */}
          </p>
        </div>
        <div className="col-lg-5">
          
        </div>
      </div>
    </div>
  </div>
</footer>


    </>
 }
 
export default FooterNav;
