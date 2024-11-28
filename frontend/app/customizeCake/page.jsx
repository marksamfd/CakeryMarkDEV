'use client';

import { useState } from 'react';
import StepperIndicatior from '../components/stepperIndicatior';
import Button from '../components/button';
import CheckoutInputField from '../components/checkoutInput';

function Page() {
  const [currentStep, setCurrentStep] = useState(0);
  const [cakeShape, setCakeShape] = useState(`Circle`);
  const [cakeSize, setCakeSize] = useState(`Small 16 cm`);
  const [cakeLayers, setCakeLayers] = useState([
    {
      innerFillings: 'Nutella',
      innerToppings: 'Chocolate Chips',
      outerCoating: 'Butter Cream',
      outerToppings: 'Fruits',
    },
  ]);
  const [cakeCurrentLayer, setCakeCurrentLayer] = useState(0);
  const [cakeType, setCakeType] = useState(`Chocolate`);
  const steps = ['Structure', 'Layers', 'Summary'];
  const allSizes = ['Small 16 cm', 'Medium 20 cm', 'Large 24 cm'];
  const allShapes = ['Circle', 'Rectangle', 'Square', 'Heart'];
  const allFlavours = [
    'Chocolate',
    'Vanilla',
    'Half Chocolate Half Vanilla',
    'Red Velvet',
    'Carrot Cake',
    'Ice Cream',
  ];
  const innerFillings = [
    'None',
    'Chocolate Ganache',
    'Strawberry Jam',
    'Nutella',
    'Cream Chease',
    'Salted Carame',
  ];
  const innerToppings = [
    'None',
    'Strawberries',
    'Mango',
    'Berries',
    'Chocolate Chips',
    'Nuts',
  ];
  const outerCoating = [
    'None',
    'Froasting',
    'Butter Cream',
    'Cream Chease',
    'White Sugar Paste',
    'White Fondant',
  ];
  const outerToppings = [
    'None',
    'Fruits',
    'Sprinkles',
    'Candies (M&Ms)',
    'Gold/Silver Beads',
    'Chocolate Chips',
  ];
  const changeLayerProps = (prop, value) => {
    const newCakeLayers = [...cakeLayers];
    newCakeLayers[cakeCurrentLayer][prop] = value;
    setCakeLayers(newCakeLayers);
  };

  const addNewLayer = () => {
    setCakeLayers([
      ...cakeLayers,
      {
        innerFillings: 'Nutella',
        innerToppings: 'Chocolate Chips',
        outerCoating: 'Butter Cream',
        outerToppings: 'Fruits',
      },
    ]);
  };
  const changeCurrentLayer = (i) => {
    setCakeCurrentLayer(i);
  };

  return (
    <>
      <StepperIndicatior steps={steps} currentStep={currentStep} />

      {currentStep == 0 && (
        <div className="container" style={styles.stepContainer}>
          <div className="row mt-4">
            <div className="col-2" style={styles.rowLabel}>
              Cake Shape
            </div>
            <div className="col" style={styles.selectorContainer}>
              {allShapes.map((shape) => {
                return (
                  <div className="form-check form-check-inline">
                    <input
                      className="form-check-input"
                      type="radio"
                      name="cakeShape"
                      key={shape}
                      id={shape}
                      value={shape}
                      checked={cakeShape === shape}
                      onChange={(e) => setCakeShape(e.target.value)}
                    />
                    <label className="form-check-label" htmlFor={shape}>
                      {shape}
                    </label>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="row mt-4">
            <div className="col-2" style={styles.rowLabel}>
              Cake Size
            </div>
            <div className="col" style={styles.selectorContainer}>
              {allSizes.map((size) => {
                return (
                  <div className="form-check form-check-inline">
                    <input
                      className="form-check-input"
                      type="radio"
                      name="cakeSize"
                      key={size}
                      id={size}
                      value={size}
                      checked={cakeSize === size}
                      onChange={(e) => setCakeSize(e.target.value)}
                    />
                    <label className="form-check-label" htmlFor={size}>
                      {size}
                    </label>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="row mt-4">
            <div className="col-2" style={styles.rowLabel}>
              Cake Flavour
            </div>
            <div className="col" style={styles.selectorContainer}>
              {allFlavours.map((flavour) => {
                return (
                  <div className="form-check form-check-inline">
                    <input
                      className="form-check-input"
                      type="radio"
                      name="cakeFlavour"
                      key={flavour}
                      id={flavour}
                      value={flavour}
                      checked={cakeType === flavour}
                      onChange={(e) => setCakeType(e.target.value)}
                    />
                    <label className="form-check-label" htmlFor={flavour}>
                      {flavour}
                    </label>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="row mt-4">
            <CheckoutInputField
              label="WRITE YOUR CUSTOM MESSAGE"
              required={false}
            />
          </div>
        </div>
      )}
      {currentStep == 1 && (
        <div className="container" style={styles.stepContainer}>
          <div className="d-lg-flex flex-row">
            <div className="d-lg-flex flex-column mt-2 me-2">
              <h3>Inner Fillings</h3>
              {innerFillings.map((filling, i) => {
                return (
                  <>
                    <input
                      type="radio"
                      className="btn-check"
                      name="innerFillings"
                      key={filling}
                      id={`option-innerFillings-${+i}`}
                      autoComplete="off"
                      checked={
                        cakeLayers[cakeCurrentLayer].innerFillings === filling
                      }
                      onChange={(e) =>
                        changeLayerProps('innerFillings', filling)
                      }
                    />
                    <label
                      className="btn mt-2 text-uppercase text-start"
                      htmlFor={`option-innerFillings-${+i}`}
                    >
                      {filling}
                    </label>
                  </>
                );
              })}
            </div>
            <div className="d-lg-flex flex-column mt-2 me-2">
              <h3>Inner Toppings</h3>
              {innerToppings.map((filling, i) => {
                return (
                  <>
                    <input
                      type="radio"
                      className="btn-check"
                      name="innerToppings"
                      key={filling}
                      id={`option-innerToppings-${+i}`}
                      autoComplete="off"
                      checked={
                        cakeLayers[cakeCurrentLayer].innerToppings === filling
                      }
                      onChange={(e) =>
                        changeLayerProps('innerToppings', filling)
                      }
                    />
                    <label
                      className="btn mt-2 text-uppercase text-start"
                      htmlFor={`option-innerToppings-${+i}`}
                    >
                      {filling}
                    </label>
                  </>
                );
              })}
            </div>
            <div className="d-lg-flex flex-column mt-2 me-2">
              <h3>Outer Coating</h3>
              {outerCoating.map((filling, i) => {
                return (
                  <>
                    <input
                      type="radio"
                      className="btn-check"
                      name="outerCoating"
                      key={filling}
                      id={`option-outerCoating-${+i}`}
                      autoComplete="off"
                      checked={
                        cakeLayers[cakeCurrentLayer].outerCoating === filling
                      }
                      onChange={(e) =>
                        changeLayerProps('outerCoating', filling)
                      }
                    />
                    <label
                      className="btn mt-2 text-uppercase text-start"
                      htmlFor={`option-outerCoating-${+i}`}
                    >
                      {filling}
                    </label>
                  </>
                );
              })}
            </div>
            <div className="d-lg-flex flex-column mt-2 me-2">
              <h3>Outer Topping</h3>
              {outerToppings.map((filling, i) => {
                return (
                  <>
                    <input
                      type="radio"
                      className="btn-check"
                      name="outerTopping"
                      key={filling}
                      id={`option-outerTopping-${+i}`}
                      autoComplete="off"
                      checked={
                        cakeLayers[cakeCurrentLayer].outerToppings === filling
                      }
                      onChange={(e) =>
                        changeLayerProps('outerToppings', filling)
                      }
                    />
                    <label
                      className="btn mt-2 text-uppercase text-start"
                      htmlFor={`option-outerTopping-${+i}`}
                    >
                      {filling}
                    </label>
                  </>
                );
              })}
            </div>
          </div>
        </div>
      )}
      {currentStep == 2 && <div className="container">Step 3</div>}

      <div className="container d-lg-flex w-100" style={styles.bottomSection}>
        {currentStep == 1 && (
          <div
            className="w-75"
            style={{ ...styles.layersSummary, ...styles.layersBase }}
          >
            <div className="d-flex justify-content-between align-items-center">
              <h6>Layers</h6>
              <span className="btn" onClick={addNewLayer}>
                +
              </span>
            </div>
            {cakeLayers.map((layer, i) => {
              return i == cakeCurrentLayer ? (
                <div
                  className="d-flex justify-content-between mt-1"
                  style={{ ...styles.layersBase, ...styles.activeLayer }}
                >
                  <div key={`layer${i}`}>
                    <span>Layer {i + 1}</span>
                  </div>
                  <span>$699</span>
                </div>
              ) : (
                <div
                  className="d-flex justify-content-between"
                  onClick={() => changeCurrentLayer(i)}
                  style={{ ...styles.layersBase }}
                >
                  <div key={`layer${i}`}>Layer {i + 1}</div>
                  <span>$699</span>
                </div>
              );
            })}
          </div>
        )}
        <div style={styles.buttonContainer}>
          <Button
            onClick={() => {
              setCurrentStep(currentStep - 1);
            }}
            disabled={currentStep === 0}
          >
            Previous
          </Button>
          <Button
            onClick={() => {
              // Submit form
              if (currentStep !== steps.length - 1)
                setCurrentStep(currentStep + 1);
            }}
          >
            {currentStep !== steps.length - 1 ? 'Next' : 'Submit'}
          </Button>
        </div>
      </div>
    </>
  );
}

const styles = {
  buttonContainer: {
    padding: '10px',
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
  },
  layersSummary: {
    paddingTop: '10px',
    paddingBottom: '10px',
    paddingLeft: '5px',
    paddingRight: '5px',
    marginLeft: '10%',
    width: '30%',
    backgroundColor: '#FDF3EA',
  },
  stepContainer: {
    marginTop: '2%',
    paddingLeft: '7%',
    marginTop: '5%',
  },
  rowLabel: {
    textTransform: 'uppercase',
    fontWeight: 'bold',
  },
  selectorContainer: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'start',
  },
  bottomSection: {
    marginTop: '5%',
    marginBottom: '5%',
    flexDirection: 'row',

    alignItems: 'center',
    justifyContent: 'space-around',
  },
  layersBase: {
    width: '100%',
    paddingLeft: '2%',
    paddingRight: '2%',
  },
  activeLayer: {
    borderColor: 'black',
    borderStyle: 'solid',
    borderWidth: 1,
  },
};

export default Page;
