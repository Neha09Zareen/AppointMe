import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const isLoggedIn = localStorage.getItem("isLoggedIn");
  const userRole = localStorage.getItem("userRole");

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("userRole");

    localStorage.removeItem("userId");
    localStorage.removeItem("userName");
    localStorage.removeItem("userEmail");

    localStorage.removeItem("doctorId");
    localStorage.removeItem("adminId");
    localStorage.removeItem("adminLoginId");

    navigate("/");
  };

  return (
    <nav>
      <h2>AppointMe</h2>

      {isLoggedIn && userRole === "patient" && (
        <>
          <button onClick={() => navigate("/appointment-history")}>
            Appointment History
          </button>

          <button onClick={handleLogout}>
            Logout
          </button>
        </>
      )}

      {isLoggedIn && userRole === "doctor" && (
        <button onClick={handleLogout}>
          Logout
        </button>
      )}

      {isLoggedIn && userRole === "admin" && (
        <button onClick={handleLogout}>
          Logout
        </button>
      )}
    </nav>
  );
}

export default Navbar;