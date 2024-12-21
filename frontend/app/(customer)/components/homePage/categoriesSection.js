import React from 'react';

/**
 * Renders an "About" section on the homepage, including a short paragraph
 * describing the company and a set of three progress bars representing the
 * company's expertise in cake design, cake classes, and cake recipes.
 */
function CategoriesSection() {
  return (
    <section className="about spad">
      <div className="container">
        <div className="row">
          <div className="col-lg-6 col-md-6">
            <div className="about__text">
              <div className="section-title">
                <span>About Cake shop</span>
                <h2>Cakes and bakes from the house of Queens!</h2>
              </div>
              <p>
                The &quot;Cake Shop&quot; is a Jordanian Brand that started as a
                small family business. The owners are Dr. Iyad Sultan and Dr.
                Sereen Sharabati, supported by a staff of 80 employees.
              </p>
            </div>
          </div>
          <div className="col-lg-6 col-md-6">
            <div className="about__bar">
              <div className="about__bar__item">
                <p>Cake design</p>
                <div id="bar1" className="barfiller">
                  <div className="tipWrap">
                    <span className="tip"></span>
                  </div>
                  <span className="fill" data-percentage="95"></span>
                </div>
              </div>
              <div className="about__bar__item">
                <p>Cake Class</p>
                <div id="bar2" className="barfiller">
                  <div className="tipWrap">
                    <span className="tip"></span>
                  </div>
                  <span className="fill" data-percentage="80"></span>
                </div>
              </div>
              <div className="about__bar__item">
                <p>Cake Recipes</p>
                <div id="bar3" className="barfiller">
                  <div className="tipWrap">
                    <span className="tip"></span>
                  </div>
                  <span className="fill" data-percentage="90"></span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default CategoriesSection;
