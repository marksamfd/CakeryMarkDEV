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
    return { loggedIn: true };
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

  const parsedCredentials = z.object({
    firstname: z.string(),
    lastname: z.string(),
    email: z.string().email(),
    password: z.string().min(6),
    phonenum: z.string().min('01200000000'.length).max('01200000000'.length),
    addressgooglemapurl: z.string().url(),
  });

  const result = parsedCredentials.safeParse(body);
  if (result.success) {
    if (body.password !== formData.get('confirmPassword')) {
      return { error: 'Passwords does not Match', prevState };
    }
    try {
      let register = await fetch(`${process.env.backend}/cakery/user/SignUp`, {
        body: JSON.stringify(body),
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        method: 'post',
      });
      if (register.ok) return { registered: true };
      else return { error: 'an Error occured in the registeration' };
    } catch (error) {
      // return { error };
    }
  } else {
    return { error: JSON.stringify(result) };
  }
  redirect('/signIn');
}

export async function editData(prevState, formData) {
  const body = {
    firstname: formData.get('FirstName'),
    lastname: formData.get('LastName'),
    phonenum: formData.get('Phone'),
    addressgooglemapurl: formData.get('Location'),
  };

  const parsedCredentials = z.object({
    firstname: z.string(),
    lastname: z.string(),
    phonenum: z.string().min('01200000000'.length).max('01200000000'.length),
    addressgooglemapurl: z.string().url(),
  });

  const cookieStore = await cookies();
  const token = cookieStore.get('token');

  const result = parsedCredentials.safeParse(body);
  if (result.success) {
    try {
      let editData = await fetch(
        `${process.env.backend}/cakery/user/customer/EditData`,

        {
          body: JSON.stringify(body),
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token.value}`,
          },
          method: 'put',
        },
      );
      if (!editData.ok) return { error: 'an Error occured During Editing' };
      else return { edited: true };
    } catch (error) {
      return { error };
    }
  } else {
    console.log(result);
    return { error: 'Check your input' };
  }
}

export async function loginWithGoogle(gcback) {
  console.log(gcback);
  const body = { code: gcback.credential };
  try {
    let register = await fetch(
      `${process.env.backend}/App/User/Google-Callback`,
      {
        body: JSON.stringify(body),
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        method: 'post',
      },
    );
    if (!register.ok) return { error: 'an Error occured in the registeration' };
    else {
      let response = await register.json();
      const cookieStore = await cookies();
      await cookieStore.set('token', response.jwt_access_token);
      await cookieStore.set('role', 'customer');
      return redirect('/signUp/' + response.jwt_access_token);
    }
  } catch (error) {
    if (isRedirectError(error)) {
      throw error;
    }
  }
}

export async function resetPassswordForm(fd) {
  const req = await fetch(
    `${process.env.backend}/cakery/user/customer/ResetPassword`,
    {
      headers: {
        Authorization: `Bearer ${fd.get('token')}`,
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        newpassword: fd.get('password'),
        newpasswordconfirm: fd.get('confirmPassword'),
      }),
    },
  );
  const resJson = await req.json();
  if (req.ok) {
    return { edited: true };
  } else {
    return { message: resJson.message };
  }
}
