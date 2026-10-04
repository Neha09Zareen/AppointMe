import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

function AdminRegister() {
  const navigate = useNavigate();

  const [loginId, setLoginId] = useState("");
  const [password, setPassword] = useState("");
  const [registrationKey, setRegistrationKey] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/admin-register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            login_id: loginId,
            password: password,
            registration_key: registrationKey,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setMessage(
          "Admin registration successful. You can now login."
        );

        setTimeout(() => {
          navigate("/admin-login");
        }, 2000);
      } else {
        setMessage(
          data.message || "Admin registration failed."
        );
      }
    } catch (error) {
      console.error("Admin registration error:", error);
      setMessage("Could not connect to backend.");
    }
  };

  return (
    <div>
      <h1>AppointMe</h1>

      <p>Healthcare Appointment Scheduling System</p>

      <h2>Admin Registration</h2>

      <p>
        Admin registration requires a valid registration key.
      </p>

      <form onSubmit={handleSubmit}>
        <label>Admin Login ID</label>
        <br />

        <input
          type="text"
          placeholder="Create an admin login ID"
          value={loginId}
          onChange={(e) => setLoginId(e.target.value)}
          required
        />

        <br />
        <br />

        <label>Password</label>
        <br />

        <input
          type="password"
          placeholder="Create an admin password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <br />
        <br />

        <label>Admin Registration Key</label>
        <br />

        <input
          type="password"
          placeholder="Enter registration key"
          value={registrationKey}
          onChange={(e) => setRegistrationKey(e.target.value)}
          required
        />

        <br />
        <br />

        <button type="submit">
          Register Admin
        </button>
      </form>

      {message && <p>{message}</p>}

      <p>
        Already have an admin account?{" "}
        <Link to="/admin-login">Admin Login</Link>
      </p>

      <p>
        <Link to="/">Back to Role Selection</Link>
      </p>
    </div>
  );
}

export default AdminRegister;