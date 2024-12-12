import React from 'react';

/**
 * @function TeamMember
 * @description A React component for a team member.
 * @param {Object} props Component props.
 * @param {Image} props.img The image of the team member.
 * @param {string} props.bakerName The name of the team member.
 * @param {string} props.positionBaker The position of the team member.
 * @return {ReactElement} The TeamMember component.
 */
function TeamMember({ img, bakerName, positionBaker }) {
  return (
    <div
      className="team__item set-bg"
      style={{
        backgroundImage: `url(${img.src})`,
        backgroundSize: 'cover',
      }}
    >
      <div className="team__item__text">
        <h6>{bakerName}</h6>
        <span>{positionBaker}</span>
        <div className="team__item__social">
          <a href="#">
            <i className="fa fa-facebook"></i>
          </a>
          <a href="#">
            <i className="fa fa-twitter"></i>
          </a>
          <a href="#">
            <i className="fa fa-instagram"></i>
          </a>
          <a href="#">
            <i className="fa fa-youtube-play"></i>
          </a>
        </div>
      </div>
    </div>
  );
}

export default TeamMember;
