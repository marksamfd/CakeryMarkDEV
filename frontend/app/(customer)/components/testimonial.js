import React from 'react';
import Image from 'next/image';

/**
 * A component that renders a single testimonial.
 * @param {object} image - The image to display for the testimonial.
 * @param {string} name - The name of the person who provided the testimonial.
 * @param {string} location - The location of the person who provided the testimonial.
 * @param {number} rating - A number from 1 to 5 indicating the rating of the testimonial.
 * @param {string} text - The text of the testimonial.
 * @returns {React.ReactElement} The component.
 */
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
