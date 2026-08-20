import "./AppointmentHistory.css";
import { useEffect, useState } from "react";

function AppointmentHistory() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/appointments/1"
        );

        const data = await response.json();

        setAppointments(data);
      } catch (error) {
        console.error("Error fetching appointments:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAppointments();
  }, []);

  if (loading) {
    return <p>Loading appointment history...</p>;
  }

  return (
    <div className="appointment-history-page">
      <div className="appointment-history-card">

        <h1>Appointment History</h1>

        {appointments.length === 0 ? (
          <p>No appointments found.</p>
        ) : (
          <div className="appointment-list">

            {appointments.map((appointment) => (
              <div
                className="appointment-item"
                key={appointment.id}
              >
                <h2>
                  Doctor ID: {appointment.doctor_id}
                </h2>

                <p>
                  <strong>Date:</strong>{" "}
                  {appointment.appointment_date}
                </p>

                <p>
                  <strong>Time:</strong>{" "}
                  {appointment.appointment_time}
                </p>

                <p>
                  <strong>Status:</strong>{" "}
                  {appointment.status}
                </p>
              </div>
            ))}

          </div>
        )}

      </div>
    </div>
  );
}

export default AppointmentHistory;