import { cookies } from 'next/headers';
export const authConfig = {
  pages: {
    signIn: '/signIn',
  },
  callbacks: {
    authorized: async ({ auth, request: { nextUrl } }) => {
      const cookieStore = await cookies();
      const role = cookieStore.get('role');
      const token = cookieStore.get('token');
      const isLoggedIn = token !== undefined;

      const isUserPage =
        nextUrl.pathname.startsWith('/customerOrders') ||
        nextUrl.pathname.startsWith('/customizeCake') ||
        nextUrl.pathname.startsWith('/cart');
      const isBakerPage = nextUrl.pathname.startsWith('/baker');

      if (isUserPage) {
        if (isLoggedIn) return true;
        return false; // Redirect unauthenticated users to login page
      }
      // if (isBakerPage) {
      //   if (isLoggedIn && role === 'baker') return true;
      //   return false; // Redirect unauthenticated users to login page
      // }
      return true;
    },
  },
};
