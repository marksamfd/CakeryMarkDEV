'use client';
import Image from 'next/image';
import logo from '@/img/logo.png';
import heart from '@/img/icon/heart.png';
import cart from '@/img/icon/cart.png';
import search from '@/img/icon/search.png';
import bell from '@/img/icon/bell.svg';
import { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

/**
 * A header navigation component that includes a logo, cart icon,
 * and links to various pages such as Home, Shop, and Contact.
 * It also provides an off-canvas menu for mobile view.
 *
 * @param {Object} props - The component properties.
 * @param {number} props.itemsInCart - The number of items in the cart.
 * @param {string} [props.name] - The authentication token to determine user login status.
 * @param {string} [props.token] - The authentication token to determine user login status.
 *
 * @returns {React.ReactElement} The rendered header navigation component.
 */
function HeaderNav({ itemsInCart = 0, sumInCart, name, token }) {
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
              <Link href="#">
                <Image
                  width={iconSize - 2}
                  height={iconSize + 2}
                  src={cart}
                  alt=""
                />{' '}
                <span>{itemsInCart}</span>
              </Link>
            </div>
          </div>
             <div className="offcanvas__cart">
            <div className="offcanvas__cart__item">
              <Link href="/notifications">
                <Image
                  width={iconSize - 2}
                  height={iconSize + 2}
                  src={bell}
                  alt=""
                />{' '}
                <span></span>
              </Link>
            </div>
          </div>
          <div className="offcanvas__logo">
            <Link href="/">
              <Image width={logoWidth} height={logoHeight} src={logo} alt="" />
            </Link>
          </div>
          <div id="mobile-menu-wrap"></div>
          <div className="offcanvas__option">
            <ul>
              <li>
                <Link href="#">Sign in</Link>{' '}
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
                        {token === undefined ? (
                          <Link href="/signIn">Sign in</Link>
                        ) : (
                          <>
                            <Link href="/customerOrders">{'My Orders'}</Link> |{' '}
                            <Link href={`/signUp/${token}`}>
                              Update Profile{' '}
                            </Link>
                          </>
                        )}
                      </li>
                    </ul>
                  </div>
                  <div className="header__logo">
                    <Link href="/">
                      <Image
                        width={logoWidth}
                        height={logoHeight}
                        src={logo}
                        alt=""
                      />
                    </Link>
                  </div>
                  <div className="header__top__right">
                    <div className="header__top__right__cart">
                    <Link href="/notifications">
                          <Image
                           width={iconSize - 2}
                             height={iconSize + 2}
                            src={bell}
                             alt=""
                         />
                      </Link>
                      <Link href="/cart">
                        <Image
                          width={iconSize - 2}
                          height={iconSize + 2}
                          src={cart}
                          alt=""
                        />{' '}
                        <span>{itemsInCart}</span>
                      </Link>
                      <div className="cart__price">
                        Cart: <span>${sumInCart}</span>
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
                    <Link href="/contact">Contact</Link>
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