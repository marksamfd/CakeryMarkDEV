import React from 'react';
import Image from 'next/image';

function Testimonial({ image, name, location, rating, text }) {
  return (
    <div className="testimonial__item">
      <div className="testimonial__author">
        <div className="testimonial__author__pic">
          <Image src={image} alt="" />
        </div>
        <div className="testimonial__author__text">
          <h5>{name}</h5>
          <span>{location}</span>
        </div>
      </div>
      <div className="rating">
        {Array.from({ length: 0 <= rating <= 5 ? rating : 5 }).map(
          (_, index) => (
            <span key={index} className={`icon_star me-1`}></span>
          ),
        )}
      </div>
      <p>{text}</p>
    </div>
  );
}

export default Testimonial;
