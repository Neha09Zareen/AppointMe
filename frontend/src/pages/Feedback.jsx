import { useState } from "react";
import "./Feedback.css";

function Feedback() {
  const [rating, setRating] = useState("");
  const [comments, setComments] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          patient_id: 1,
          rating: Number(rating),
          comments: comments,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSubmitted(true);
        setMessage(data.message);
      } else {
        setMessage(data.message || "Failed to submit feedback");
      }
    } catch (error) {
      console.error("Feedback error:", error);
      setMessage("Could not connect to backend");
    }
  };

  return (
    <div className="feedback-container">
      <div className="feedback-card">
        <h2>Patient Feedback</h2>
        <p>We value your feedback. Please share your experience.</p>

        {submitted ? (
          <div className="success-message">
            ✅ {message}
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <label>Rating</label>

            <select
              value={rating}
              onChange={(e) => setRating(e.target.value)}
              required
            >
              <option value="">Select Rating</option>
              <option value="5">⭐⭐⭐⭐⭐ Excellent</option>
              <option value="4">⭐⭐⭐⭐ Good</option>
              <option value="3">⭐⭐⭐ Average</option>
              <option value="2">⭐⭐ Poor</option>
              <option value="1">⭐ Very Poor</option>
            </select>

            <label>Your Feedback</label>

            <textarea
              rows="5"
              placeholder="Write your feedback here..."
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              required
            ></textarea>

            <button type="submit">Submit Feedback</button>
          </form>
        )}
      </div>
    </div>
  );
}

export default Feedback;