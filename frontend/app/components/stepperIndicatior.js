'use client';
import React from 'react';

/**
 * A React component that renders a horizontal stepper indicator.
 * The component takes in a required `steps` prop which is an array of strings
 * representing the steps in the stepper. The component also takes in a required
 * `currentStep` prop which is the current step index in the stepper.
 *
 * The component renders a horizontal progress bar with a width that is
 * proportional to the current step index. The component also renders a list
 * of steps with a `li` element for each step. The `li` element renders the step
 * number as well as a badge with the step name. The `li` element also applies
 * a CSS class of `active-step` to the `li` element if the current step index
 * matches the step index.
 *
 * @param {Object} props - The props object.
 * @param {string[]} props.steps - The array of strings representing the steps
 *   in the stepper.
 * @param {number} props.currentStep - The current step index in the stepper.
 *
 * @returns {React.ReactElement} A React element representing the stepper
 *   indicator.
 */
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
        style={{
          height: '10px',
          position: 'absolute',
          width: `${50}%`,
        }}
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
