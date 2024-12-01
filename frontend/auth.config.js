import { cookies } from 'next/headers';
export const authConfig = {
  pages: {
    signIn: '/signIn',
  },
  callbacks: {
    authorized: async ({ auth, request: { nextUrl } }) => {
      const cookieStore = await cookies();
      const token = cookieStore.get('token');
      const isLoggedIn = token !== undefined;
      const isOnDashboard =
        nextUrl.pathname.startsWith('/customerOrders') ||
        nextUrl.pathname.startsWith('/customizeCake') ||
        nextUrl.pathname.startsWith('/api/customer/Cart');
      if (isOnDashboard) {
        if (isLoggedIn) return true;
        return false; // Redirect unauthenticated users to login page
      }
      return true;
    },
  },
  providers: [], // Add providers with an empty array for now
};
