/**
 * DeliveryHeader component
 *
 * This component renders a navigation bar specifically designed for the
 * delivery dashboard. The navbar uses a distinct background color to
 * differentiate it from other sections and contains a brand link displaying
 * the "Delivery Dashboard" title.
 *
 * @returns {JSX.Element} The delivery header navigation bar.
 */

function DeliveryHeader() {
    return (
      <nav
        className="navbar navbar-expand-lg"
        style={{ backgroundColor: '#f08632' }}
      >
        <div className="container-fluid">
          <a className="navbar-brand" >
            Delivery Dashboard
          </a>
        </div>
      </nav>
    );
  }
  
  export default DeliveryHeader;