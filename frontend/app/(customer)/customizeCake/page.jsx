'use client';

import { Suspense, useEffect, useState } from 'react';
import StepperIndicatior from '../components/stepperIndicatior';
import Button from '../components/button';
import CheckoutInputField from '../components/checkoutInput';
import Breadcrumb from '../components/breadcrumb';
import { redirect } from 'next/navigation';

/**
 * This is the main component of the "Make Your Own Cake" page.
 *
 * It renders a stepper component that allows the user to navigate
 * through the different steps of the customization process.
 *
 * The first step allows the user to choose the cake shape, size, and
 * flavor.
 *
 * The second step allows the user to choose the inner fillings, inner
 * toppings, outer coating, and outer toppings for the cake.
 *
 * The third step shows the user a summary of their customizations
 * and the total price of the cake.
 *
 * The user can go back and forth between the different steps using
 * the Previous and Next buttons.
 *
 * When the user clicks the Submit button, the component submits a
 * POST request to the server with the customization data and
 * redirects the user to the shop page.
 *
 * @returns {ReactElement} The main component of the "Make Your Own
 *   Cake" page.
 */
function Page() {
  const [currentStep, setCurrentStep] = useState(0);
  const [cakeShape, setCakeShape] = useState(`Circle`);
  const [cakeSize, setCakeSize] = useState(`Small 16 cm`);
  const [cakeFlavour, setCakeFlavour] = useState(`Chocolate`);
  const [cakeLayers, setCakeLayers] = useState([]);
  const [cakeCurrentLayer, setCakeCurrentLayer] = useState(0);
  const steps = ['Structure', 'Layers', 'Summary'];
  const [cakeMessage, setcakeMesssage] = useState('');
  const [allSizes, setAllSizes] = useState([]);
  const [allShapes, setAllShapes] = useState([]);
  const [allFlavours, setAllFlavours] = useState([]);
  const [innerFillings, setInnerFillings] = useState([]);
  const [innerToppings, setInnerToppings] = useState([]);
  const [outerCoating, setOuterCoating] = useState([]);
  const [outerToppings, setOuterToppings] = useState([]);
  const [layersSum, setLayersSum] = useState([]);
  const [rawItemsPricing, setRawItemsPricing] = useState([]);
  const [customResponse, setCustomResponse] = useState('');
  const addNewLayer = () => {
    setCakeLayers([
      ...cakeLayers,
      {
        innerFillings: innerFillings[0].item,
        innerToppings: innerToppings[0].item,
        outerCoating: outerCoating[0].item,
        outerToppings: outerToppings[0].item,
      },
    ]);
  };
  useEffect(() => {
    cookieStore
      .get('token')
      .then((cookie) => {
        return fetch(`/api/cakery/user/customer/Customize_Cake`, {
          headers: {
            Authorization: `Bearer ${cookie.value}`,
          },
        });
      })
      .then((res) => res.json())
      .then((objectsPrices) => {
        console.log(objectsPrices);
        setRawItemsPricing(objectsPrices);
        let cakeShapes = objectsPrices.filter(
          (obj) => obj.category === 'Cake Shape',
        );
        setAllShapes(cakeShapes);
        setCakeShape(cakeShapes[0].item);

        let cakeSizes = objectsPrices.filter(
          (obj) => obj.category === 'Cake Size',
        );
        setAllSizes(cakeSizes);
        setCakeSize(cakeSizes[0].item);
        let cakeFlavours = objectsPrices.filter(
          (obj) => obj.category === 'Cake Type',
        );
        setAllFlavours(cakeFlavours);
        setCakeFlavour(cakeFlavours[0].item);

        let innerFillingsFilter = objectsPrices.filter(
          (obj) => obj.category === 'Inner Fillings',
        );
        setInnerFillings(innerFillingsFilter);
        let innerToppingsFilter = objectsPrices.filter(
          (obj) => obj.category === 'Inner Toppings',
        );
        setInnerToppings(innerToppingsFilter);

        let outerToppingsFilter = objectsPrices.filter(
          (obj) => obj.category === 'Outer Toppings',
        );
        setOuterToppings(outerToppingsFilter);
        let outerCoatingsFilter = objectsPrices.filter(
          (obj) => obj.category === 'Outer Coating',
        );
        setOuterCoating(outerCoatingsFilter);
        setCakeLayers([
          ...cakeLayers,
          {
            innerFillings: innerFillingsFilter[0].item,
            innerToppings: innerToppingsFilter[0].item,
            outerCoating: outerCoatingsFilter[0].item,
            outerToppings: outerToppingsFilter[0].item,
          },
        ]);
      })
      .catch(console.error);
  }, []);

  useEffect(() => {
    let layers = cakeLayers.map((layer) => {
      let sum = 0;
      for (let key in layer) {
        sum += rawItemsPricing.find((obj) => obj.item === layer[key])?.price;
      }
      return sum;
    });
    layers.push(rawItemsPricing.find((obj) => obj.item === cakeFlavour)?.price);
    layers.push(rawItemsPricing.find((obj) => obj.item === cakeShape)?.price);
    layers.push(rawItemsPricing.find((obj) => obj.item === cakeSize)?.price);

    setLayersSum(layers);
  }, [cakeLayers, cakeFlavour, cakeShape, cakeSize]);

  const changeLayerProps = (prop, value) => {
    const newCakeLayers = [...cakeLayers];
    newCakeLayers[cakeCurrentLayer][prop] = value;
    setCakeLayers(newCakeLayers);
  };

  const changeCurrentLayer = (i) => {
    setCakeCurrentLayer(i);
  };

  return (
    <>
      <div style={{ marginBottom: '50px' }}>
        <Breadcrumb title="Make Your Own Cake" />
      </div>
      <StepperIndicatior steps={steps} currentStep={currentStep} />

      {currentStep == 0 && (
        <div className="container" style={styles.stepContainer}>
          <div className="row mt-4">
            <div className="col-2 flex-wrap" style={styles.rowLabel}>
              Cake Shape
            </div>
            <div className="col flex-wrap" style={styles.selectorContainer}>
              {allShapes?.map((shape) => {
                return (
                  <div
                    key={`shape-${shape.item}`}
                    className="form-check form-check-inline"
                  >
                    <input
                      className="form-check-input"
                      type="radio"
                      name="cakeShape"
                      id={`shape-${shape.item}`}
                      value={shape.item}
                      checked={cakeShape === shape.item}
                      onChange={(e) => setCakeShape(e.target.value)}
                    />
                    <label
                      className="form-check-label"
                      htmlFor={`shape-${shape.item}`}
                    >
                      {shape.item}
                    </label>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="row mt-4">
            <div className="col-2 flex-wrap" style={styles.rowLabel}>
              Cake Size
            </div>

            <div className="col" style={styles.selectorContainer}>
              {allSizes?.map((size) => {
                return (
                  <div
                    key={`size-${size.item}`}
                    className="form-check form-check-inline"
                  >
                    <input
                      className="form-check-input"
                      type="radio"
                      name="cakeSizes"
                      id={`size-${size.item}`}
                      value={size.item}
                      checked={cakeSize === size.item}
                      onChange={(e) => setCakeSize(e.target.value)}
                    />
                    <label
                      className="form-check-label"
                      htmlFor={`size-${size.item}`}
                    >
                      {size.item}
                    </label>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="row mt-4">
            <div className="col-2 flex-wrap" style={styles.rowLabel}>
              Cake Flavour
            </div>

            <div className="col flex-wrap" style={styles.selectorContainer}>
              {allFlavours?.map((flavour) => {
                return (
                  <div
                    key={`flavour-${flavour.item}`}
                    className="form-check form-check-inline"
                  >
                    <input
                      className="form-check-input"
                      type="radio"
                      name="cakeFlavour"
                      key={`flavour-${flavour.item}`}
                      id={`flavour-${flavour.item}`}
                      value={flavour.item}
                      checked={cakeFlavour === flavour.item}
                      onChange={(e) => setCakeFlavour(e.target.value)}
                    />
                    <label
                      className="form-check-label"
                      htmlFor={`flavour-${flavour.item}`}
                    >
                      {flavour.item}
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
              onChange={(e) => setcakeMesssage(e.current.value)}
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
                      key={filling.item}
                      id={`option-innerFillings-${+i}`}
                      autoComplete="off"
                      checked={
                        cakeLayers[cakeCurrentLayer].innerFillings ===
                        filling.item
                      }
                      onChange={(e) =>
                        changeLayerProps('innerFillings', filling.item)
                      }
                    />
                    <label
                      className="btn mt-2 text-uppercase text-start"
                      htmlFor={`option-innerFillings-${+i}`}
                    >
                      {filling.item}
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
                      key={filling.item}
                      id={`option-innerToppings-${+i}`}
                      autoComplete="off"
                      checked={
                        cakeLayers[cakeCurrentLayer].innerToppings ===
                        filling.item
                      }
                      onChange={(e) =>
                        changeLayerProps('innerToppings', filling.item)
                      }
                    />
                    <label
                      className="btn mt-2 text-uppercase text-start"
                      htmlFor={`option-innerToppings-${+i}`}
                    >
                      {filling.item}
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
                      key={filling.item}
                      id={`option-outerCoating-${+i}`}
                      autoComplete="off"
                      checked={
                        cakeLayers[cakeCurrentLayer].outerCoating ===
                        filling.item
                      }
                      onChange={(e) =>
                        changeLayerProps('outerCoating', filling.item)
                      }
                    />
                    <label
                      className="btn mt-2 text-uppercase text-start"
                      htmlFor={`option-outerCoating-${+i}`}
                    >
                      {filling.item}
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
                      key={filling.item}
                      id={`option-outerTopping-${+i}`}
                      autoComplete="off"
                      checked={
                        cakeLayers[cakeCurrentLayer].outerToppings ===
                        filling.item
                      }
                      onChange={(e) =>
                        changeLayerProps('outerToppings', filling.item)
                      }
                    />
                    <label
                      className="btn mt-2 text-uppercase text-start"
                      htmlFor={`option-outerTopping-${+i}`}
                    >
                      {filling.item}
                    </label>
                  </>
                );
              })}
            </div>
          </div>
        </div>
      )}
      {currentStep == 2 && (
        <div className="container" style={styles.stepContainer}>
          Your Custom Cake is total at $
          {layersSum.reduce((partialSum, a) => partialSum + a, 0)}
          <div>{customResponse.message}</div>
        </div>
      )}

      <div className="container d-lg-flex w-100" style={styles.bottomSection}>
        <div
          className="w-75"
          style={{ ...styles.layersSummary, ...styles.layersBase }}
        >
          <div className="d-flex justify-content-between flex-column">
            <h6>Base Cake</h6>
            <div className="d-flex flex-row justify-content-between">
              <div
                className="d-flex justify-content-between"
                style={{ ...styles.layersBase }}
              >
                {cakeShape}
                <span>
                  $
                  {
                    rawItemsPricing?.find((obj) => obj.item === cakeShape)
                      ?.price
                  }
                </span>
              </div>
              <div
                className="d-flex justify-content-between"
                style={{ ...styles.layersBase }}
              >
                {cakeSize}
                <span>
                  $
                  {rawItemsPricing?.find((obj) => obj.item === cakeSize)?.price}
                </span>
              </div>
              <div
                className="d-flex justify-content-between"
                style={{ ...styles.layersBase }}
              >
                {cakeFlavour}
                <span>
                  $
                  {
                    rawItemsPricing?.find((obj) => obj.item === cakeFlavour)
                      ?.price
                  }
                </span>
              </div>
            </div>
          </div>
          <div className="d-flex justify-content-between align-items-center">
            <h6>Layers</h6>
            {currentStep == 1 && (
              <span className="btn" onClick={addNewLayer}>
                +
              </span>
            )}
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
                <span>${layersSum[i]}</span>
              </div>
            ) : (
              <div
                className="d-flex justify-content-between"
                onClick={() => changeCurrentLayer(i)}
                style={{ ...styles.layersBase }}
              >
                <div key={`layer${i}`}>Layer {i + 1}</div>
                <span>${layersSum[i]}</span>
              </div>
            );
          })}
          <div className="d-flex justify-content-between pt-2">
            <h6>Current Total</h6>
            <span>
              ${layersSum.reduce((partialSum, a) => partialSum + a, 0)}
            </span>
          </div>
        </div>

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
              else {
                cookieStore
                  .get('token')
                  .then((cookie) => {
                    return fetch(
                      `/api/App/User/Customer/Customize_Cake/Create`,
                      {
                        headers: {
                          Authorization: `Bearer ${cookie.value}`,
                          Accept: 'application/json',
                          'Content-Type': 'application/json',
                        },
                        method: 'post',
                        body: JSON.stringify({
                          cakeshape: cakeShape,
                          cakesize: cakeSize,
                          caketype: cakeFlavour,
                          cakeMessage,
                          layers: [...cakeLayers],
                        }),
                      },
                    );
                  })
                  .then((res) => res.json())
                  .then(setCustomResponse)
                  .then(() => redirect('/shop'));
              }
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
