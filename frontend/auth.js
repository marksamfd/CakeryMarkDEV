import NextAuth from 'next-auth';
import { authConfig } from './auth.config';
import Credentials from 'next-auth/providers/credentials';
import GoogleProvider from 'next-auth/providers/google';

import { z } from 'zod';
import { cookies } from 'next/headers';

export const { auth, signIn, signOut } = NextAuth({
  ...authConfig,
  providers: [
    Credentials({
      async authorize(credentials) {
        const parsedCredentials = z
          .object({ email: z.string().email(), password: z.string().min(6) })
          .safeParse(credentials);

        if (parsedCredentials.success) {
          const { email, password } = parsedCredentials.data;
          const user = await fetch(
            `${process.env.backend}/cakery/user/SignIn`,
            {
              body: JSON.stringify({ email, password }),
              headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
              },
              method: 'POST',
            },
          );
          const res = await user.json();
          console.error(res);
          if (res.status !== 'success') return null;
          const cookieStore = await cookies();
          await cookieStore.set('token', res.access_token);
          await cookieStore.set('role', res.role);
          await cookieStore.set('name', res?.firstname);

          return res;
        }
      },
    }),
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
  ],
});
