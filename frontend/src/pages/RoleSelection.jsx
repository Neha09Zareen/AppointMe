import { useNavigate } from "react-router-dom";

function RoleSelection() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Welcome to AppointMe</h1>

      <p>How would you like to continue?</p>

      {/* PATIENT */}
      <div>
        <h2>👤 Patient</h2>

        <button onClick={() => navigate("/login")}>
          Patient Login
        </button>

        <button onClick={() => navigate("/register")}>
          Patient Register
        </button>
      </div>

      <br />

      {/* DOCTOR */}
      <div>
        <h2>👨‍⚕️ Doctor</h2>

        <button onClick={() => navigate("/doctor-login")}>
          Doctor Login
        </button>

        <button onClick={() => navigate("/doctor-register")}>
          Doctor Register
        </button>
      </div>

      <br />

      {/* ADMIN */}
      <div>
        <h2>🏥 Admin</h2>

        <button onClick={() => navigate("/admin-login")}>
          Admin Login
        </button>

        <button onClick={() => navigate("/admin-register")}>
          Admin Register
        </button>
      </div>
    </div>
  );
}

export default RoleSelection;