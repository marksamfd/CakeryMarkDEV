import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
/**
 * A custom navigation bar for the Baker pages.
 *
 * @returns {React.ReactElement} A custom navigation bar
 */
function AdminHeader({ pos }) {
  return (
    <Navbar style={{ backgroundColor: '#f08632' }} expand={'lg'}>
      <div className="container-fluid">
        <Navbar.Brand href="#">{'Cakery ' + pos }</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />

        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="navbar-nav">
            <Nav.Link className="nav-link active" aria-current="page" href="#">
              Home
            </Nav.Link>

            <NavDropdown title="Manage Users" id="basic-nav-dropdown">
              <NavDropdown.Item className="dropdown-item" href="/admin/manageUsers/baker">
                Baker
              </NavDropdown.Item>
              <NavDropdown.Item className="dropdown-item" href="/admin/manageUsers/delivery">
                Delivery
              </NavDropdown.Item>
              <NavDropdown.Item className="dropdown-item" href="/admin/manageUsers/customer">
                Customer
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </div>
    </Navbar>
  );
}

export default AdminHeader;
