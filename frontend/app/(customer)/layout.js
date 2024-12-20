import '../styles/barfiller.css';
import '../styles/bootstrap.min.css';
import '../styles/elegant-icons.css';
import '../styles/flaticon.css';
import '../styles/font-awesome.min.css';
import '../styles/magnific-popup.css';
import '../styles/nice-select.css';
// import "./styles/owl.carousel.min.css";
import '../styles/slicknav.min.css';
import '../styles/style.css';
import { cookies } from 'next/headers';

import HeaderNav from './components/header';
import FooterNav from './components/footer';
/* const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
 */

export const metadata = {
  title: 'Cakery',
};

export default async function RootLayout({ children }) {
  const cookieStore = await cookies();
  let itemsInCart = 0;
  let sumInCart = 0.0;
  let cookie = await cookieStore.get('token');
  let name = await cookieStore.get('name');
  if (cookie) {
    let cartReq = await fetch(
      `${process.env.backend}/cakery/user/customer/Cart`,
      {
        headers: {
          Authorization: `Bearer ${cookie.value}`,
        },
      },
    );
    let cartJson = await cartReq.json();
    console.log(cartJson);
    let cartItems = cartJson.items;
    const calculateTotal = () => {
      let total = 0;
      for (let i = 0; i < cartItems?.length; i++) {
        total += cartItems[i].price * cartItems[i].quantity;
      }
      return total;
    };
    itemsInCart = cartItems?.length;
    sumInCart = calculateTotal();
  }
  return (
    <html lang="en">
      <body className={``}>
        <HeaderNav
          itemsInCart={itemsInCart}
          sumInCart={sumInCart}
          name={name?.value}
          token={cookie?.value}
        />
        {children}
        <FooterNav />
      </body>
    </html>
  );
}
