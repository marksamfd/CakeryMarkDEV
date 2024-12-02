// import React from 'react';
import Image from 'next/image';
import ta1 from '../../img/testimonial/ta-1.jpg';
import ta2 from '../../img/testimonial/ta-2.jpg';
import { Carousel, CarouselItem, Row } from 'react-bootstrap';
import Testimonial from '../testimonial';

/**
 * A React component that renders a section of the page containing a carousel
 * of testimonials from clients. The component expects a prop called
 * `testimonials` which is an array of objects with the keys `name`, `text`,
 * `location`, and `rating`. The component will render each testimonial in a
 * carousel item, with the name, text, location, and rating displayed in a
 * `Testimonial` component.
 *
 * @param {Object[]} testimonials - An array of objects with the keys `name`,
 *   `text`, `location`, and `rating`.
 * @returns {React.ReactElement} A React element representing the section of
 *   the page containing the testimonial carousel.
 */
function TestmonialSection({ testimonials }) {
  const allTestmonialsRendered = [];
  for (let i = 0; i < testimonials?.length; i += 2) {
    allTestmonialsRendered.push(
      <CarouselItem key={`testi-${i}`} className="mb-2">
        <Row>
          <div className="col-lg-6">
            <Testimonial
              name={testimonials[i].name}
              text={testimonials[i].text}
              location={testimonials[i].location}
              rating={testimonials[i].rating}
              image={ta1}
            />
          </div>

          {testimonials[i + 1] && (
            <div className="col-lg-6">
              <Testimonial
                name={testimonials[i + 1].name}
                text={testimonials[i + 1].text}
                location={testimonials[i + 1].location}
                rating={testimonials[i + 1].rating}
                image={ta1}
              />
            </div>
          )}
        </Row>
      </CarouselItem>,
    );
  }
  return (
    <section className="testimonial spad">
      <div className="container">
        <div className="row">
          <div className="col-lg-12 text-center">
            <div className="section-title">
              <span>Testimonial</span>
              <h2>Our client say</h2>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="testimonial__slider">
            <Carousel indicators={false}>{allTestmonialsRendered}</Carousel>
          </div>
        </div>
      </div>
    </section>
  );
}

export default TestmonialSection;
