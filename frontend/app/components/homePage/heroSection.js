import React from 'react';
import hero1 from '../../img/hero/hero-1.jpg';

/**
 * The HeroSection component is a section of the homepage that displays
 * a hero image of a cake with a heading and a link to the cakes page.
 *
 * @return {ReactElement} The hero section component.
 */
function HeroSection() {
  return (
    <section className="hero">
      <div
        className="hero__item set-bg"
        style={{
          backgroundImage: `url(${hero1.src})`,
          backgroundSize: 'cover',
        }}
      >
        <div className="container">
          <div className="row d-flex justify-content-center">
            <div className="col-lg-8">
              <div className="hero__text">
                <h2>Making your life sweeter one bite at a time!</h2>
                <a href="#" className="primary-btn">
                  Our cakes
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default HeroSection;
