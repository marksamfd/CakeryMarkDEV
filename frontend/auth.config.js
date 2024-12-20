import { cookies } from 'next/headers';
import {
  isAdminPage,
  isBakerPage,
  isDeliveryPage,
  isUserPage,
} from '@/authUtils';

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

      if (isUserPage(nextUrl.pathname)) {
        if (isLoggedIn && role === 'customer') return true;
        return false; // Redirect unauthenticated users to login page
      }
      if (isBakerPage(nextUrl.pathname)) {
        if (isLoggedIn && role === 'baker') return true;
        return false; // Redirect unauthenticated users to login page
      }
      if (isAdminPage(nextUrl.pathname)) {
        if (isLoggedIn && role === 'admin') return true;
        return false; // Redirect unauthenticated users to login page
      }
      if (isDeliveryPage(nextUrl.pathname)) {
        if (isLoggedIn && role === 'delivery') return true;
        return false; // Redirect unauthenticated users to login page
      }
      return true;
    },
  },
};
