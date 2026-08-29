import { useState } from "react";
import "./Feedback.css";

function Feedback() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="feedback-container">
      <div className="feedback-card">
        <h2>Patient Feedback</h2>
        <p>We value your feedback. Please share your experience.</p>

        {submitted ? (
          <div className="success-message">
            ✅ Thank you for your feedback!
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <label>Rating</label>
            <select required>
              <option value="">Select Rating</option>
              <option>⭐⭐⭐⭐⭐ Excellent</option>
              <option>⭐⭐⭐⭐ Good</option>
              <option>⭐⭐⭐ Average</option>
              <option>⭐⭐ Poor</option>
              <option>⭐ Very Poor</option>
            </select>

            <label>Your Feedback</label>
            <textarea
              rows="5"
              placeholder="Write your feedback here..."
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