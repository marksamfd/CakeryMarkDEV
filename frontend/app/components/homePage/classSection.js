import React from 'react';

function ClassSection() {
  return (
    <section className="class spad">
      <div className="container">
        <div className="row">
          <div className="col-lg-6">
            <div className="class__form">
              <div className="section-title">
                <span>Class cakes</span>
                <h2>
                  Made from your <br />
                  own hands
                </h2>
              </div>
              <form action="#">
                <input type="text" placeholder="Name" />
                <input type="text" placeholder="Phone" />
                <select className="nice-select w-100">
                  <option value="">Studying Class</option>
                  <option value="">Writting Class</option>
                  <option value="">Reading Class</option>
                </select>
                <input type="text" placeholder="Type your requirements" />
                <button type="submit" className="site-btn">
                  registration
                </button>
              </form>
            </div>
          </div>
        </div>
        <div className="class__video set-bg" data-setbg="img/class-video.jpg">
          <a
            href="https://www.youtube.com/watch?v=8PJ3_p7VqHw&list=RD8PJ3_p7VqHw&start_radio=1"
            className="play-btn video-popup"
          >
            <i className="fa fa-play"></i>
          </a>
        </div>
      </div>
    </section>
  );
}

export default ClassSection;
