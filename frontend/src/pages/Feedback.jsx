
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Feedback.css";

function Feedback() {
  const navigate = useNavigate();

  const [rating, setRating] = useState("");
  const [comments, setComments] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [message, setMessage] = useState("");
  const [appointments, setAppointments] = useState([]);
  const [doctorId, setDoctorId] = useState("");
  const [loading, setLoading] = useState(true);

  const userId = localStorage.getItem("userId");

  useEffect(() => {
    const loadAppointments = async () => {
      if (!userId) {
        setMessage("Please log in again before submitting feedback.");
        setLoading(false);
        return;
      }

      try {
        const response = await fetch(
          `http://127.0.0.1:5000/appointments/${userId}`
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "Could not load appointments.");
        }

        const validAppointments = Array.isArray(data)
          ? data.filter(
              (appointment) =>
                appointment.doctor_id &&
                appointment.status !== "Cancelled"
            )
          : [];

        setAppointments(validAppointments);

        if (validAppointments.length > 0) {
          setDoctorId(String(validAppointments[0].doctor_id));
        } else {
          setMessage(
            "No active appointments found. Book an appointment before submitting feedback."
          );
        }
      } catch (error) {
        console.error("Error loading appointments:", error);
        setMessage(error.message || "Could not load appointments.");
      } finally {
        setLoading(false);
      }
    };

    loadAppointments();
  }, [userId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    if (!userId) {
      setMessage("Please log in again before submitting feedback.");
      return;
    }

    if (!doctorId) {
      setMessage("Please select a doctor from your appointments.");
      return;
    }

    if (!rating || !comments.trim()) {
      setMessage("Please provide both a rating and comments.");
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/feedback",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id: Number(userId),
            patient_id: Number(userId),
            doctor_id: Number(doctorId),
            rating: Number(rating),
            comment: comments.trim(),
            comments: comments.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Failed to submit feedback.");
      }

      setSubmitted(true);
      setMessage(data.message || "Feedback submitted successfully.");
    } catch (error) {
      console.error("Feedback error:", error);
      setMessage(error.message || "Could not submit feedback.");
    }
  };

  if (loading) {
    return <p>Loading your appointments...</p>;
  }

  return (
    <div className="feedback-page">
      <div className="feedback-card">
        <h1>Feedback</h1>

        {!submitted ? (
          <form onSubmit={handleSubmit}>
            <label htmlFor="doctor">Doctor</label>

            <select
              id="doctor"
              value={doctorId}
              onChange={(e) => setDoctorId(e.target.value)}
              required
              disabled={appointments.length === 0}
            >
              {appointments.length === 0 && (
                <option value="">No active appointments</option>
              )}

              {appointments.map((appointment) => (
                <option
                  key={appointment.id}
                  value={appointment.doctor_id}
                >
                  {appointment.doctor_name ||
                    appointment.doctor ||
                    `Doctor ID: ${appointment.doctor_id}`}
                  {" — Appointment #"}
                  {appointment.id}
                </option>
              ))}
            </select>

            <label htmlFor="rating">Rating</label>

            <select
              id="rating"
              value={rating}
              onChange={(e) => setRating(e.target.value)}
              required
            >
              <option value="">Select a rating</option>
              <option value="1">⭐ 1 - Poor</option>
              <option value="2">⭐⭐ 2 - Fair</option>
              <option value="3">⭐⭐⭐ 3 - Good</option>
              <option value="4">⭐⭐⭐⭐ 4 - Very Good</option>
              <option value="5">⭐⭐⭐⭐⭐ 5 - Excellent</option>
            </select>

            <label htmlFor="comments">Comments</label>

            <textarea
              id="comments"
              placeholder="Write your feedback..."
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              rows="5"
              required
            />

            <button
              type="submit"
              disabled={appointments.length === 0}
            >
              Submit Feedback
            </button>
          </form>
        ) : (
          <div>
            <p>{message}</p>

            <button
              onClick={() => navigate("/appointment-history")}
            >
              Back to Appointment History
            </button>

            <button
              onClick={() => navigate("/hospitals")}
              style={{ marginLeft: "10px" }}
            >
              Back to Hospitals
            </button>
          </div>
        )}

        {!submitted && message && <p>{message}</p>}
      </div>
    </div>
  );
}

export default Feedback;
