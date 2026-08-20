import "./AppointmentHistory.css";
import { useEffect, useState } from "react";

function AppointmentHistory() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  const [reschedulingId, setReschedulingId] = useState(null);
  const [newDate, setNewDate] = useState("");
  const [newTime, setNewTime] = useState("");

  // =========================
  // CANCEL APPOINTMENT
  // =========================
  const handleCancel = async (appointmentId) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/appointments/${appointmentId}/cancel`,
        {
          method: "PUT",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Failed to cancel appointment"
        );
      }

      alert("Appointment cancelled successfully!");

      setAppointments((currentAppointments) =>
        currentAppointments.map((appointment) =>
          appointment.id === appointmentId
            ? {
                ...appointment,
                status: "Cancelled",
              }
            : appointment
        )
      );
    } catch (error) {
      console.error("Error cancelling appointment:", error);
      alert("Could not cancel appointment.");
    }
  };

  // =========================
  // START RESCHEDULING
  // =========================
  const handleStartReschedule = (appointment) => {
    setReschedulingId(appointment.id);
    setNewDate(appointment.appointment_date);
    setNewTime(appointment.appointment_time);
  };

  // =========================
  // RESCHEDULE APPOINTMENT
  // =========================
  const handleReschedule = async (appointmentId) => {
    if (!newDate || !newTime) {
      alert("Please select a date and time.");
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
          data.message || "Failed to reschedule appointment"
        );
      }

      alert("Appointment rescheduled successfully!");

      setAppointments((currentAppointments) =>
        currentAppointments.map((appointment) =>
          appointment.id === appointmentId
            ? {
                ...appointment,
                appointment_date: newDate,
                appointment_time: newTime,
                status: "Rescheduled",
              }
            : appointment
        )
      );

      setReschedulingId(null);
      setNewDate("");
      setNewTime("");
    } catch (error) {
      console.error("Error rescheduling appointment:", error);
      alert("Could not reschedule appointment.");
    }
  };

  // =========================
  // FETCH APPOINTMENTS
  // =========================
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

  // =========================
  // LOADING
  // =========================
  if (loading) {
    return <p>Loading appointment history...</p>;
  }

  // =========================
  // PAGE
  // =========================
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

                {/* =========================
                    BOOKED APPOINTMENT BUTTONS
                   ========================= */}

                {appointment.status === "Booked" && (
                  <button
                    className="cancel-appointment-button"
                    onClick={() =>
                      handleCancel(appointment.id)
                    }
                  >
                    Cancel Appointment
                  </button>
                )}

                {/* =========================
                    RESCHEDULE BUTTON
                    AVAILABLE FOR BOOKED
                    AND RESCHEDULED
                   ========================= */}

                {(appointment.status === "Booked" ||
                  appointment.status === "Rescheduled") && (
                  <button
                    className="reschedule-appointment-button"
                    onClick={() =>
                      handleStartReschedule(appointment)
                    }
                  >
                    Reschedule Appointment
                  </button>
                )}

                {/* =========================
                    RESCHEDULE FORM
                   ========================= */}

                {reschedulingId === appointment.id && (
                  <div className="reschedule-form">

                    <label>New Date</label>

                    <input
                      type="date"
                      value={newDate}
                      onChange={(e) =>
                        setNewDate(e.target.value)
                      }
                    />

                    <label>New Time</label>

                    <input
                      type="time"
                      value={newTime}
                      onChange={(e) =>
                        setNewTime(e.target.value)
                      }
                    />

                    <button
                      className="confirm-reschedule-button"
                      onClick={() =>
                        handleReschedule(appointment.id)
                      }
                    >
                      Confirm Reschedule
                    </button>

                    <button
                      className="cancel-reschedule-button"
                      onClick={() => {
                        setReschedulingId(null);
                        setNewDate("");
                        setNewTime("");
                      }}
                    >
                      Go Back
                    </button>

                  </div>
                )}

              </div>
            ))}

          </div>
        )}

      </div>
    </div>
  );
}

export default AppointmentHistory;