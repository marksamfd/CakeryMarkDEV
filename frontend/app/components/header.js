"use client";
import Image from "next/image";
import logo from "@/img/logo.png";
import heart from "@/img/icon/heart.png";
import cart from "@/img/icon/cart.png";
import search from "@/img/icon/search.png";
import { useEffect, useRef, useState } from "react";

function HeaderNav({ itemsInCart = 0 }) {
    const [buttonClicked, setButtonClicked] = useState(false)
    const iconSize = 25
    const logoHeight = 85
    const logoWidth = 150
    return<>
     <div className={`offcanvas-menu-overlay ${buttonClicked ? "active": ""}`} onClick={()=>{setButtonClicked(!buttonClicked)}}>
            <div className={`offcanvas-menu-wrapper ${buttonClicked ? "active": ""}`}>
                <div className="offcanvas__cart">
                    <div className="offcanvas__cart__item">
                    <a href="#"><Image width={iconSize - 2} height={iconSize + 2} src={cart} alt="" /> <span>{itemsInCart}</span></a>
                    <div className="cart__price">Cart: <span>$0.00</span></div>
                    </div>
                </div>
                <div className="offcanvas__logo">
                    <a href="./index.html"><Image width={logoWidth} height={logoHeight} src={logo} alt=""/></a>
                </div>
                <div id="mobile-menu-wrap"></div>
                <div className="offcanvas__option">
                    <ul>
                        <li><a href="#">Sign in</a> <span className="arrow_carrot-down"></span></li>
                    </ul>
                </div>
            </div>
        </div>

    <div className="header">
        <div className="header__top">
            <div className="container">
                <div className="row">
                    <div className="col-lg-12">
                        <div className="header__top__inner">
                            <div className="header__top__left">
                                <ul>
                                    <li><a href="#">Sign in</a> </li>
                                </ul>
                            </div>
                            <div className="header__logo">
                                <a href="./index.html"><Image width={logoWidth} height={logoHeight} src={logo} alt="" /></a>
                            </div>
                            <div className="header__top__right">
                               
                                <div className="header__top__right__cart">
                                    <a href="#"><Image width={iconSize - 2} height={iconSize + 2} src={cart} alt="" /> <span>{itemsInCart}</span></a>
                                    <div className="cart__price">Cart: <span>$0.00</span></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="canvas__open" onClick={()=>{
                    setButtonClicked(!buttonClicked)
                }}><i className="fa fa-bars"></i></div>
            </div>
        </div>
        <div className="container">
            <div className="row">
                <div className="col-lg-12">
                    <nav className="header__menu mobile-menu">
                        <ul>
                            <li className="active"><a href="./index.html">Home</a></li>
                            <li><a href="./about.html">About</a></li>
                            <li><a href="./shop.html">Shop</a></li>
                            <li><a href="#">Pages</a>
                                <ul className="dropdown">
                                    <li><a href="./shop-details.html">Shop Details</a></li>
                                    <li><a href="./shoping-cart.html">Shoping Cart</a></li>
                                    <li><a href="./checkout.html">Check Out</a></li>
                                    <li><a href="./wisslist.html">Wisslist</a></li>
                                    <li><a href="./className.html">className</a></li>
                                    <li><a href="./blog-details.html">Blog Details</a></li>
                                </ul>
                            </li>
                            <li><a href="./blog.html">Blog</a></li>
                            <li><a href="./contact.html">Contact</a></li>
                        </ul>
                    </nav>
                </div>
            </div>
        </div>
    </div>
    </>
}

export default HeaderNav
