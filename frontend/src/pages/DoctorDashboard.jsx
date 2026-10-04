import { useEffect, useState } from "react";

function DoctorDashboard() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const doctorId = localStorage.getItem("doctorId");
  const doctorName = localStorage.getItem("userName");

  useEffect(() => {
    if (!doctorId) {
      setMessage("Doctor information not found. Please login again.");
      setLoading(false);
      return;
    }

    fetch(`http://127.0.0.1:5000/doctor-appointments/${doctorId}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Could not fetch appointments");
        }

        return response.json();
      })
      .then((data) => {
        setAppointments(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching doctor appointments:", error);
        setMessage("Could not load appointments.");
        setLoading(false);
      });
  }, [doctorId]);

  return (
    <div style={{ padding: "30px" }}>
      <h1>Doctor Dashboard</h1>

      {doctorName && (
        <h2>Welcome, Dr. {doctorName}</h2>
      )}

      {message && <p>{message}</p>}

      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "10px",
          padding: "20px",
          marginTop: "20px",
        }}
      >
        <h3>Appointments</h3>

        {loading ? (
          <p>Loading appointments...</p>
        ) : appointments.length === 0 ? (
          <p>No appointments found.</p>
        ) : (
          <ul>
            {appointments.map((appointment) => (
              <li
                key={appointment.id}
                style={{ marginBottom: "15px" }}
              >
                <strong>
                  Appointment ID: {appointment.id}
                </strong>

                <br />

                Date: {appointment.appointment_date}

                <br />

                Time: {appointment.appointment_time}

                <br />

                Patient: {appointment.patient_name}

                <br />

                Patient ID: {appointment.patient_id}

                <br />

                Status: {appointment.status}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default DoctorDashboard;