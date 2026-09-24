import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function AppointmentHistory() {
  const navigate = useNavigate();

  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const userId = localStorage.getItem("userId");

  const fetchAppointments = async () => {
    if (!userId) {
      setMessage("Please login again to view your appointments.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/appointments/${userId}`
      );

      if (!response.ok) {
        throw new Error("Could not fetch appointments");
      }

      const data = await response.json();

      setAppointments(data);
    } catch (error) {
      console.error("Error fetching appointments:", error);
      setMessage("Could not load your appointments.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAppointments();
  }, [userId]);

  const handleCancel = async (appointmentId) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/appointments/${appointmentId}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Could not cancel appointment");
      }

      setMessage(data.message);

      fetchAppointments();
    } catch (error) {
      console.error("Cancel error:", error);
      setMessage(error.message);
    }
  };

  const handleReschedule = async (appointmentId) => {
    const newDate = prompt("Enter new appointment date (YYYY-MM-DD):");
    const newTime = prompt("Enter new appointment time (HH:MM):");

    if (!newDate || !newTime) {
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/appointments/${appointmentId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            appointment_date: newDate,
            appointment_time: newTime,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Could not reschedule appointment"
        );
      }

      setMessage(data.message);

      fetchAppointments();
    } catch (error) {
      console.error("Reschedule error:", error);
      setMessage(error.message);
    }
  };

  if (loading) {
    return <p>Loading appointments...</p>;
  }

  return (
    <div style={{ padding: "30px" }}>
      <h1>Appointment History</h1>

      {message && <p>{message}</p>}

      {appointments.length === 0 ? (
        <div>
          <p>No appointments found.</p>

          <button onClick={() => navigate("/hospitals")}>
            Book an Appointment
          </button>
        </div>
      ) : (
        <div>
          {appointments.map((appointment) => (
            <div
              key={appointment.id}
              style={{
                border: "1px solid #ccc",
                borderRadius: "10px",
                padding: "20px",
                marginBottom: "15px",
              }}
            >
              <p>
                <strong>Appointment ID:</strong>{" "}
                {appointment.id}
              </p>

              <p>
                <strong>Doctor ID:</strong>{" "}
                {appointment.doctor_id}
              </p>

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

              {appointment.status !== "Cancelled" && (
                <div>
                  <button
                    onClick={() =>
                      handleCancel(appointment.id)
                    }
                  >
                    Cancel Appointment
                  </button>

                  <button
                    onClick={() =>
                      handleReschedule(appointment.id)
                    }
                    style={{ marginLeft: "10px" }}
                  >
                    Reschedule Appointment
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div style={{ marginTop: "30px" }}>
        <button onClick={() => navigate("/feedback")}>
          Give Feedback
        </button>
      </div>

      <div style={{ marginTop: "15px" }}>
        <button onClick={() => navigate("/hospitals")}>
          Back to Hospitals
        </button>
      </div>
    </div>
  );
}

export default AppointmentHistory;