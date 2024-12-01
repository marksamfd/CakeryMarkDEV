import './styles/barfiller.css';
import './styles/bootstrap.min.css';
import './styles/elegant-icons.css';
import './styles/flaticon.css';
import './styles/font-awesome.min.css';
import './styles/magnific-popup.css';
import './styles/nice-select.css';
// import "./styles/owl.carousel.min.css";
import './styles/slicknav.min.css';
import './styles/style.css';

import HeaderNav from './components/header';
import FooterNav from './components/footer';
import { SessionProvider } from 'next-auth/react';
/* const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
 */

export const metadata = {
  title: 'Cakery',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={``}>
        <HeaderNav itemsInCart={0} />
        {children}
        <FooterNav />
      </body>
    </html>
  );
}
