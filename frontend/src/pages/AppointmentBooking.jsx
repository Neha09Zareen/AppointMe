import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "./AppointmentBooking.css";

export default function AppointmentBooking() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [doctor, setDoctor] = useState(null);
  const [hospital, setHospital] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [summary, setSummary] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [booked, setBooked] = useState(false);

  const today = new Date();
  const minDate = [
    today.getFullYear(),
    String(today.getMonth() + 1).padStart(2, "0"),
    String(today.getDate()).padStart(2, "0"),
  ].join("-");

  const timeSlots = [
    "09:00",
    "10:00",
    "11:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
  ];

  useEffect(() => {
    async function loadDoctor() {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/doctors/${id}`
        );

        if (!response.ok) {
          throw new Error("Doctor not found");
        }

        const doctorData = await response.json();
        setDoctor(doctorData);

        const hospitalResponse = await fetch(
          "http://127.0.0.1:5000/hospitals"
        );

        if (!hospitalResponse.ok) {
          throw new Error("Could not load hospitals");
        }

        const hospitals = await hospitalResponse.json();

        const found = hospitals.find(
          (item) =>
            String(item.id) === String(doctorData.hospital_id)
        );

        setHospital(found?.name || "Unknown Hospital");
      } catch (error) {
        setMessage(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadDoctor();
  }, [id]);

  
  const [summaryLoading, setSummaryLoading] = useState(false);

  
async function generateSummary() {
  if (!symptoms.trim()) {
    setMessage("Please enter your symptoms first.");
    return;
  }

  setSummaryLoading(true);
  setSummary("");
  setMessage("");

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/symptom-summary",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: symptoms.trim() }),
      }
    );

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Could not generate AI summary.");
    }

    setSummary(result.summary);
  } catch (error) {
    setMessage(error.message || "Could not generate AI summary.");
  } finally {
    setSummaryLoading(false);
  }
}

  async function handleBooking() {
    if (!date || !time || !symptoms.trim()) {
      setMessage(
        "Please select a date and time and enter your symptoms."
      );
      return;
    }

    if (date < minDate) {
      setMessage("Please select today or a future date.");
      return;
    }

    if (!summary.trim()) {
      setMessage("Please preview the symptom summary first.");
      return;
    }

    const userId = localStorage.getItem("userId");

    if (!userId) {
      setMessage("Please login again before booking.");
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/appointments",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            patient_id: Number(userId),
            doctor_id: Number(id),
            appointment_date: date,
            appointment_time: time,
            symptoms: symptoms.trim(),
            symptom_summary: summary,
          }),
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message || "Booking failed"
        );
      }

      setBooked(true);
      setMessage("Appointment booked successfully!");
    } catch (error) {
      setMessage(
        error.message || "Could not book appointment."
      );
    }
  }

  if (loading) {
    return <p>Loading doctor information...</p>;
  }

  if (!doctor) {
    return <p>{message || "Doctor not found."}</p>;
  }

  return (
    <div className="appointment-booking-page">
      <div className="appointment-booking-card">
        <h1>Book Appointment</h1>

        <div className="booking-doctor">
          <div className="booking-doctor-icon">👨‍⚕️</div>
          <h2>{doctor.name}</h2>
          <p>{doctor.specialization}</p>
        </div>

        <div className="booking-info">
          <p>
            <strong>Hospital:</strong> {hospital}
          </p>
          <p>
            <strong>Experience:</strong>{" "}
            {doctor.experience} years
          </p>
          <p>
            <strong>Degrees:</strong> {doctor.degrees}
          </p>
        </div>

        <label htmlFor="booking-date">
          Appointment Date
        </label>
        <input
          id="booking-date"
          type="date"
          min={minDate}
          value={date}
          disabled={booked}
          onChange={(e) => {
            setDate(e.target.value);
            setMessage("");
          }}
        />

        <label>Appointment Time</label>
        <div className="time-slots">
          {timeSlots.map((slot) => (
            <button
              type="button"
              key={slot}
              disabled={booked}
              className={
                time === slot
                  ? "time-slot selected"
                  : "time-slot"
              }
              onClick={() => {
                setTime(slot);
                setMessage("");
              }}
            >
              {slot}
            </button>
          ))}
        </div>

        <label htmlFor="symptoms">
          Describe Your Symptoms
        </label>
        <textarea
          id="symptoms"
          rows={5}
          value={symptoms}
          disabled={booked}
          placeholder="Describe your symptoms and when they started..."
          onChange={(e) => {
            setSymptoms(e.target.value);
            setSummary("");
            setMessage("");
          }}
        />

        
<button
  type="button"
  className="summary-button"
  disabled={booked || summaryLoading}
  onClick={generateSummary}
>
  {summaryLoading ? "Generating AI Summary..." : "Preview Symptom Summary"}
</button>


        {summary && (
  <div className="symptom-summary">
    <h3>Gemini AI Symptom Summary</h3>
    <p style={{ whiteSpace: "pre-line" }}>{summary}</p>
  </div>
)}

        <button
          type="button"
          className="confirm-booking-button"
          onClick={handleBooking}
          disabled={booked}
        >
          {booked ? "Appointment Confirmed" : "Confirm Appointment"}
        </button>

        {message && (
          <p className="booking-message">{message}</p>
        )}
      </div>
    </div>
  );
}