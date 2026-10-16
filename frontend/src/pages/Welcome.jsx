import { Link } from "react-router-dom";

function Welcome() {
  return (
    <div>
      <h1>Welcome to AppointMe</h1>

      <p>Healthcare Appointment Scheduling System</p>

      <h2>Get Started</h2>

      <Link to="/register">
        <button>Create an Account</button>
      </Link>

      <Link to="/login">
        <button>Login</button>
      </Link>
    </div>
  );
}

export default Welcome;