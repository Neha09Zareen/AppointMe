import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Feedback.css";

function Feedback() {
  const navigate = useNavigate();

  const [rating, setRating] = useState("");
  const [comments, setComments] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const userId = localStorage.getItem("userId");

    if (!userId) {
      setMessage("Please login again before submitting feedback.");
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
            patient_id: Number(userId),
            rating: Number(rating),
            comments: comments,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setSubmitted(true);
        setMessage(data.message);
      } else {
        setMessage(
          data.message || "Failed to submit feedback"
        );
      }
    } catch (error) {
      console.error("Feedback error:", error);
      setMessage("Could not connect to backend");
    }
  };

  return (
    <div className="feedback-page">
      <div className="feedback-card">

        <h1>Feedback</h1>

        {!submitted ? (
          <form onSubmit={handleSubmit}>

            <label>Rating</label>

            <select
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

            <br />
            <br />

            <label>Comments</label>

            <textarea
              placeholder="Write your feedback..."
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              rows="5"
              required
            />

            <br />
            <br />

            <button type="submit">
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

        {!submitted && message && (
          <p>{message}</p>
        )}

      </div>
    </div>
  );
}

export default Feedback;