import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
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

        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="navbar-nav">
            <Nav.Link className="nav-link active" aria-current="page" href="#">
              Home
            </Nav.Link>

            <NavDropdown title="Manage Users" id="basic-nav-dropdown">
              <NavDropdown.Item className="dropdown-item" href="#">
                Baker
              </NavDropdown.Item>
              <NavDropdown.Item className="dropdown-item" href="#">
                Delivary
              </NavDropdown.Item>
              <NavDropdown.Item className="dropdown-item" href="#">
                Customer
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </div>
    </Navbar>
  );
}

export default BakerHeader;
