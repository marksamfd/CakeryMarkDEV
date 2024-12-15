'use server';
import { cookies } from 'next/headers';
import { permanentRedirect, redirect } from 'next/navigation';
import { signIn } from '@/auth';
import { AuthError } from 'next-auth';
import { z } from 'zod';
import { isRedirectError } from 'next/dist/client/components/redirect';

export async function authenticate(prevState, formData) {
  try {
    let sign = await signIn('credentials', formData);
    console.log({ dd: formData.get('callbackUrl') });
  } catch (error) {
    if (isRedirectError(error)) {
      throw error;
    }
    if (error instanceof AuthError) {
      console.error(error);
      switch (error.type) {
        case 'CredentialsSignin':
          return 'Invalid credentials.';
        default:
          return 'Something went wrong.';
      }
    }
  }
}
export async function signUp(prevState, formData) {
  const body = {
    firstname: formData.get('FirstName'),
    lastname: formData.get('LastName'),
    email: formData.get('Email'),
    password: formData.get('password'),
    phonenum: formData.get('Phone'),
    addressgooglemapurl: formData.get('Location'),
  };
  const parsedCredentials = z
    .object({
      firstname: z.string(),
      lastname: z.string(),
      email: z.string().email(),
      password: z.string().min(6),
      phonenum: z.string().min('01200000000'.length).max('01200000000'.length),
      addressgooglemapurl: z.string().url(),
    })
    .safeParse(body);
  if (parsedCredentials.success) {
    if (body.password !== formData.get('confirmPassword')) {
      return { error: 'Passwords does not Match', prevState };
    }
    try {
      let register = await fetch(`${process.env.backend}/App/User/SignUp`, {
        body: JSON.stringify(body),
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        method: 'post',
      });
      if (!register.ok)
        return { error: 'an Error occured in the registeration' };
    } catch (error) {
      // return { error };
    }
  } else {
    return { error: 'Check your inoput' };
  }
  redirect('/signIn');
}
