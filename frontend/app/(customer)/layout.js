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

  let cookie = await cookieStore.get('token');
  return (
    <html lang="en">
      <body className={``}>
        <HeaderNav itemsInCart={0} token={cookie?.value} />
        {children}
        <FooterNav />
      </body>
    </html>
  );
}
