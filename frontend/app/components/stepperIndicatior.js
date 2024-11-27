'use client';
import React from 'react';

function StepperIndicatior({ steps, currentStep }) {
  return (
    <div
      style={{
        position: 'sticky',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div
        className="progress"
        role="progressbar"
        style={{ height: '10px', position: 'absolute', width: '50%' }}
      >
        <div
          className="progress-bar"
          style={{
            width: `${(currentStep / (steps.length - 1)) * 100}%`,
            backgroundColor: '#f08632',
          }}
        ></div>
      </div>

      <ul
        style={{
          display: 'flex',
          listStyle: 'none',
          justifyContent: 'space-evenly',
          position: 'relative',
          width: '100%',
          zIndex: '55',
        }}
      >
        {steps.map((step, index) => {
          return (
            <li
              key={index}
              className="stepper-item border text-center rounded-circle p-2 active-step"
              style={
                currentStep === index
                  ? { backgroundColor: '#f08632', color: 'white' }
                  : {}
              }
            >
              {index + 1}
              <span className="position-absolute top-100 translate-middle badge  text-bg-secondary">
                {steps[index]}
                <span className="visually-hidden">unread messages</span>
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default StepperIndicatior;
