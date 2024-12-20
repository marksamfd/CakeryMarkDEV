import React from 'react';
import Image from 'next/image';
import contactImage from '@/img/class/class-4.jpg'; 
import Title from '../components/title';

const ContactPage = () => {
  return (
      <div className="container mt-5">
        <div className="contact-content">
          <div className="contact-details">
          <h4 className='contact-header mb-4'>
          <Title >Baked with Love,<br /><br/>Served with a Smile!
          </Title>
          Having a question or craving something sweet? We are here here to help!<br/>
          Reach out to us anytime!
          </h4>
            <ul>
              <li>
                <strong>Email:</strong> <a href="mailto:admin@cakery_admin.com">admin@cakery_admin.com</a>
              </li>
              <li>
                <strong>Phone:</strong> <a href="tel:+201010203073">+201010203073</a>
              </li>
              <li>
                <strong>Address:</strong> ZewailCity, 6th of October City, Egypt
              </li>
            </ul>
            <div className="mt-5"/>
          </div>

          <div className="contact-image mb-5">
            <Image
              src={contactImage}
              alt="Contact Us"
              width={600}
              height={400}
              className="contact-image__image"
            />
          </div>
        </div>
      </div>
  );
};

export default ContactPage;
