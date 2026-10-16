
import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function AppointmentHistory() {
  const navigate = useNavigate();

  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const userId = localStorage.getItem("userId");

  const fetchAppointments = useCallback(async () => {
    if (!userId) {
      setAppointments([]);
      setMessage("Please login again to view your appointments.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/appointments/${userId}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Could not fetch appointments."
        );
      }

      if (!Array.isArray(data)) {
        throw new Error("Unexpected appointment data received.");
      }

      setAppointments(data);
      setMessage("");
    } catch (error) {
      console.error("Error fetching appointments:", error);
      setMessage(error.message || "Could not load your appointments.");
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
  let ignore = false;

  const loadAppointments = async () => {
    if (!userId) {
      setAppointments([]);
      setMessage("Please login again to view your appointments.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/appointments/${userId}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Could not fetch appointments."
        );
      }

      if (!Array.isArray(data)) {
        throw new Error("Unexpected appointment data received.");
      }

      if (!ignore) {
        setAppointments(data);
        setMessage("");
      }
    } catch (error) {
      if (!ignore) {
        console.error("Error fetching appointments:", error);
        setMessage(error.message || "Could not load your appointments.");
      }
    } finally {
      if (!ignore) {
        setLoading(false);
      }
    }
  };

  loadAppointments();

  return () => {
    ignore = true;
  };
}, [userId]);

  const handleCancel = async (appointmentId) => {
    const confirmed = window.confirm(
      "Are you sure you want to cancel this appointment?"
    );

    if (!confirmed) return;

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/appointments/${appointmentId}`,
        { method: "DELETE" }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Could not cancel appointment."
        );
      }

      setMessage(data.message || "Appointment cancelled successfully.");
      await fetchAppointments();
    } catch (error) {
      console.error("Cancel error:", error);
      setMessage(error.message || "Could not cancel appointment.");
    }
  };

  const handleReschedule = async (appointmentId) => {
    const newDate = window.prompt(
      "Enter new appointment date (YYYY-MM-DD):"
    );

    if (!newDate) return;

    const newTime = window.prompt(
      "Enter new appointment time (HH:MM, e.g. 14:00):"
    );

    if (!newTime) return;

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
          data.message || "Could not reschedule appointment."
        );
      }

      setMessage(data.message || "Appointment rescheduled successfully.");
      await fetchAppointments();
    } catch (error) {
      console.error("Reschedule error:", error);
      setMessage(error.message || "Could not reschedule appointment.");
    }
  };

  if (loading) {
    return <p>Loading appointments...</p>;
  }

  return (
    <div style={{ padding: "30px" }}>
      <h1>Appointment History</h1>

      {message && (
        <p role="status" aria-live="polite">
          {message}
        </p>
      )}

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
                <strong>Appointment ID:</strong> {appointment.id}
              </p>

              <p>
                <strong>Doctor ID:</strong> {appointment.doctor_id}
              </p>

              <p>
                <strong>Date:</strong> {appointment.appointment_date}
              </p>

              <p>
                <strong>Time:</strong> {appointment.appointment_time}
              </p>

              <p>
                <strong>Status:</strong> {appointment.status}
              </p>

              {appointment.status !== "Cancelled" && (
                <div>
                  <button
                    onClick={() => handleCancel(appointment.id)}
                  >
                    Cancel Appointment
                  </button>

                  {(appointment.status === "Booked" ||
                    appointment.status === "Rescheduled") && (
                    <button
                      onClick={() => handleReschedule(appointment.id)}
                      style={{ marginLeft: "10px" }}
                    >
                      Reschedule Appointment
                    </button>
                  )}
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
