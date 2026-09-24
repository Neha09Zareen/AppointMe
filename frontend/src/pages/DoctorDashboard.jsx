import { useEffect, useState } from "react";

function DoctorDashboard() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  const doctorId = 13;

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/doctor-appointments/${doctorId}`)
      .then((response) => response.json())
      .then((data) => {
        setAppointments(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching doctor appointments:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: "30px" }}>
      <h1>Doctor Dashboard</h1>

      <div
        style={{
          background: "#fff",
          padding: "20px",
          marginTop: "20px",
          borderRadius: "10px",
          boxShadow: "0 0 10px rgba(0,0,0,0.1)",
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
              <li key={appointment.id}>
                {appointment.appointment_date} -{" "}
                {appointment.appointment_time} -{" "}
                {appointment.patient_name} -{" "}
                {appointment.status}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default DoctorDashboard;