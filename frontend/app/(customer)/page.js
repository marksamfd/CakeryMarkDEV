'use client';
import Image from 'next/image';
import styles from '../page.module.css';
import HeroSection from './components/homePage/heroSection';
import AboutSection from './components/homePage/aboutSection';
import CategoriesSection from './components/homePage/categoriesSection';
import ProductSection from './components/homePage/productSection';
import ClassSection from './components/homePage/classSection';
import TeamSection from './components/homePage/teamSection';
import TestmonialSection from './components/homePage/testmonialSection';
import useFcmToken from '@/utils/hooks/useFcmToken';
import { useEffect } from 'react';

export default function Home() {
  const testimonialsFetched = [
    {
      name: 'John Doe',
      text: 'This is a great product',
      location: 'New York',
      rating: 5,
    },
    {
      name: 'Jane Doe',
      text: 'This Cake Shop is awesome',
      location: 'New York',
      rating: 5,
    },
    {
      name: 'Jane Doe',
      text: 'The custom cake was Awesome',
      location: 'New York',
      rating: 5,
    },
  ];
  const { fcmToken, notificationPermissionStatus } = useFcmToken();

  useEffect(() => {
    cookieStore.get('token').then((token) => {
      if (token && fcmToken) {
        console.log('FCM token: ', fcmToken);
        fetch(`api/cakery/user/customer/NotificationToken`, {
          method: 'post',
          headers: {
            Authorization: `Bearer ${token.value}`,
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ fcm_token: fcmToken }),
        })
          .then((res) => res.json())
          .then((data) => {})
          .catch(console.error);
      }
    });
  }, [fcmToken]);

  //
  return (
    <>
      <HeroSection />
      <CategoriesSection />
      <ProductSection />
      {/* <ClassSection /> */}
      <TeamSection />
      <TestmonialSection testimonials={testimonialsFetched} />
    </>
  );
}
