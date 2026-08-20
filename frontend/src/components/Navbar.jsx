import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <h2>Hospital Appointment System</h2>

      <Link to="/register">Register</Link> |{" "}
      <Link to="/login">Login</Link>
    </nav>
  );
}

export default Navbar;