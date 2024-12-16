import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
/**
 * A custom navigation bar for the Baker pages.
 *
 * @returns {React.ReactElement} A custom navigation bar
 */
function BakerHeader({ pos }) {
  return (
    <Navbar style={{ backgroundColor: '#f08632' }} expand={'lg'}>
      <div className="container-fluid">
        <Navbar.Brand href="#">{'Cakery ' + pos || 'Baker'}</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
      </div>
    </Navbar>
  );
}

export default BakerHeader;
