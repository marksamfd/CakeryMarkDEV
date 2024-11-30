import React from 'react';
import baker1 from '../../img/team/team-1.jpg';
import baker2 from '../../img/team/team-2.jpg';
import baker3 from '../../img/team/team-3.jpg';
import baker4 from '../../img/team/team-4.jpg';
import TeamMember from '../teamMember';

function TeamSection() {
  const bakers = [
    { bakerName: 'Randy Butler', positionBaker: 'Decorater', img: baker1 },
    { bakerName: 'Randy Butler', positionBaker: 'Decorater', img: baker2 },
    { bakerName: 'Randy Butler', positionBaker: 'Decorater', img: baker3 },
    { bakerName: 'Randy Butler', positionBaker: 'Decorater', img: baker4 },
  ];
  return (
    <section className="team spad">
      <div className="container">
        <div className="row">
          <div className="col-lg-7 col-md-7 col-sm-7">
            <div className="section-title">
              <span>Our team</span>
              <h2>Sweet Baker </h2>
            </div>
          </div>
          <div className="col-lg-5 col-md-5 col-sm-5">
            <div className="team__btn">
              <a href="#" className="primary-btn">
                Join Us
              </a>
            </div>
          </div>
        </div>
        <div className="row">
          {bakers.map((baker, index) => {
            return (
              <div key={`baker${index}`} className="col-lg-3 col-md-6 col-sm-6">
                <TeamMember
                  bakerName={baker.bakerName}
                  positionBaker={baker.positionBaker}
                  img={baker.img}
                />
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

export default TeamSection;
