import { useState } from "react";
import { useNavigate } from "react-router-dom";

function DoctorLogin() {
  const navigate = useNavigate();

  const [loginId, setLoginId] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/doctor-login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            login_id: loginId,
            password: password,
          }),
        }
      );

      const data = await response.json();

      if (response.ok && data.message === "Doctor Login Successful") {
        localStorage.setItem("isLoggedIn", "true");
        localStorage.setItem("userRole", "doctor");

        localStorage.setItem("doctorId", data.doctor_id);
        localStorage.setItem("userName", data.name);

        navigate("/doctor");
      } else {
        setMessage(data.message || "Doctor login failed");
      }
    } catch (error) {
      console.error("Doctor login error:", error);
      setMessage("Could not connect to backend");
    }
  };

  return (
    <div>
      <h2>Doctor Login</h2>

      <form onSubmit={handleSubmit}>
        <label>Login ID</label>
        <br />

        <input
          type="text"
          placeholder="Enter your doctor login ID"
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
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <br />
        <br />

        <button type="submit">Login</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default DoctorLogin;