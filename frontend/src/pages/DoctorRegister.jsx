import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";

function DoctorRegister() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [phone, setPhone] = useState("");
  const [specialization, setSpecialization] = useState("");
  const [experience, setExperience] = useState("");
  const [degrees, setDegrees] = useState("");
  const [hospitalId, setHospitalId] = useState("");

  const [hospitals, setHospitals] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/hospitals")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Could not fetch hospitals");
        }

        return response.json();
      })
      .then((data) => {
        setHospitals(data);
      })
      .catch((error) => {
        console.error("Error fetching hospitals:", error);
        setMessage("Could not load hospitals.");
      });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/doctor-register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: name,
            email: email,
            password: password,
            phone: phone,
            specialization: specialization,
            experience: experience,
            degrees: degrees,
            hospital_id: hospitalId,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setMessage(
          "Doctor registration submitted successfully. Please wait for admin approval before logging in."
        );

        setTimeout(() => {
          navigate("/doctor-login");
        }, 2500);
      } else {
        setMessage(data.message || "Doctor registration failed.");
      }
    } catch (error) {
      console.error("Doctor registration error:", error);
      setMessage("Could not connect to backend.");
    }
  };

  return (
    <div>
      <h1>AppointMe</h1>

      <p>Healthcare Appointment Scheduling System</p>

      <h2>Doctor Registration</h2>

      <p>
        Create your doctor account. Your account will be reviewed by an
        administrator before you can log in.
      </p>

      <form onSubmit={handleSubmit}>
        <label>Full Name</label>
        <br />

        <input
          type="text"
          placeholder="Enter your full name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <br />
        <br />

        <label>Email</label>
        <br />

        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <br />
        <br />

        <label>Password</label>
        <br />

        <input
          type="password"
          placeholder="Create a password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <br />
        <br />

        <label>Phone</label>
        <br />

        <input
          type="text"
          placeholder="Enter your phone number"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          required
        />

        <br />
        <br />

        <label>Specialization</label>
        <br />

        <input
          type="text"
          placeholder="Example: Cardiologist"
          value={specialization}
          onChange={(e) => setSpecialization(e.target.value)}
          required
        />

        <br />
        <br />

        <label>Experience (years)</label>
        <br />

        <input
          type="number"
          min="0"
          placeholder="Enter years of experience"
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
          required
        />

        <br />
        <br />

        <label>Degrees</label>
        <br />

        <input
          type="text"
          placeholder="Example: MBBS, MD"
          value={degrees}
          onChange={(e) => setDegrees(e.target.value)}
          required
        />

        <br />
        <br />

        <label>Hospital</label>
        <br />

        <select
          value={hospitalId}
          onChange={(e) => setHospitalId(e.target.value)}
          required
        >
          <option value="">Select your hospital</option>

          {hospitals.map((hospital) => (
            <option key={hospital.id} value={hospital.id}>
              {hospital.name}
            </option>
          ))}
        </select>

        <br />
        <br />

        <button type="submit">
          Submit Registration
        </button>
      </form>

      {message && <p>{message}</p>}

      <p>
        Already have a doctor account?{" "}
        <Link to="/doctor-login">Doctor Login</Link>
      </p>

      <p>
        <Link to="/">Back to Role Selection</Link>
      </p>
    </div>
  );
}

export default DoctorRegister;