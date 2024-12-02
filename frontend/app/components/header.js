'use client';
import Image from 'next/image';
import logo from '@/img/logo.png';
import heart from '@/img/icon/heart.png';
import cart from '@/img/icon/cart.png';
import search from '@/img/icon/search.png';
import { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

function HeaderNav({ itemsInCart = 0 }) {
  const [buttonClicked, setButtonClicked] = useState(false);
  const iconSize = 25;
  const logoHeight = 65;
  const logoWidth = 120;
  const pathname = usePathname();
  console.log('pathname', pathname);
  return (
    <>
      <div
        className={`offcanvas-menu-overlay ${buttonClicked ? 'active' : ''}`}
        onClick={() => {
          setButtonClicked(!buttonClicked);
        }}
      >
        <div
          className={`offcanvas-menu-wrapper ${buttonClicked ? 'active' : ''}`}
        >
          <div className="offcanvas__cart">
            <div className="offcanvas__cart__item">
              <a href="#">
                <Image
                  width={iconSize - 2}
                  height={iconSize + 2}
                  src={cart}
                  alt=""
                />{' '}
                <span>{itemsInCart}</span>
              </a>
              <div className="cart__price">
                Cart: <span>$0.00</span>
              </div>
            </div>
          </div>
          <div className="offcanvas__logo">
            <a href="./index.html">
              <Image width={logoWidth} height={logoHeight} src={logo} alt="" />
            </a>
          </div>
          <div id="mobile-menu-wrap"></div>
          <div className="offcanvas__option">
            <ul>
              <li>
                <a href="#">Sign in</a>{' '}
                <span className="arrow_carrot-down"></span>
              </li>
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
                      <li>
                        <a href="/signIn">Sign in</a>{' '}
                      </li>
                    </ul>
                  </div>
                  <div className="header__logo">
                    <a href="./index.html">
                      <Image
                        width={logoWidth}
                        height={logoHeight}
                        src={logo}
                        alt=""
                      />
                    </a>
                  </div>
                  <div className="header__top__right">
                    <div className="header__top__right__cart">
                      <a href="/cart">
                        <Image
                          width={iconSize - 2}
                          height={iconSize + 2}
                          src={cart}
                          alt=""
                        />{' '}
                        <span>{itemsInCart}</span>
                      </a>
                      <div className="cart__price">
                        Cart: <span>$0.00</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div
              className="canvas__open"
              onClick={() => {
                setButtonClicked(!buttonClicked);
              }}
            >
              <i className="fa fa-bars"></i>
            </div>
          </div>
        </div>
        <div className="container">
          <div className="row">
            <div className="col-lg-12">
              <nav className="header__menu mobile-menu">
                <ul>
                  <li className={`${pathname == '/' ? 'active' : ''}`}>
                    <Link href="./">Home</Link>
                  </li>

                  <li className={`${pathname == '/shop' ? 'active' : ''}`}>
                    <Link href="/shop">Shop</Link>
                  </li>

                  <li>
                    <a href="/contact">Contact</a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default HeaderNav;
