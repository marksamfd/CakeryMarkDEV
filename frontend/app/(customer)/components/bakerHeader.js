/**
 * A custom navigation bar for the Baker pages.
 *
 * @returns {React.ReactElement} A custom navigation bar
 */
function BakerHeader() {
  return (
    <nav
      className="navbar navbar-expand-lg"
      style={{ backgroundColor: '#f08632' }}
    >
      <div className="container-fluid">
        <a className="navbar-brand" href="#">
          Navbar
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavAltMarkup"
          aria-controls="navbarNavAltMarkup"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div className="navbar-nav">
            <a className="nav-link active" aria-current="page" href="#">
              Home
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default BakerHeader;
