import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "./AppointmentBooking.css";

function AppointmentBooking() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [doctor, setDoctor] = useState(null);
  const [hospitalName, setHospitalName] = useState("");
  const [appointmentDate, setAppointmentDate] = useState("");
  const [appointmentTime, setAppointmentTime] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [bookingSuccessful, setBookingSuccessful] = useState(false);

  const timeSlots = [
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
  ];

  useEffect(() => {
    const fetchDoctor = async () => {
      try {
        const doctorResponse = await fetch(
          `http://127.0.0.1:5000/doctors/${id}`
        );

        if (!doctorResponse.ok) {
          throw new Error("Doctor not found");
        }

        const doctorData = await doctorResponse.json();
        setDoctor(doctorData);

        const hospitalsResponse = await fetch(
          "http://127.0.0.1:5000/hospitals"
        );

        const hospitalsData = await hospitalsResponse.json();

        const hospital = hospitalsData.find(
          (hospital) => hospital.id === doctorData.hospital_id
        );

        setHospitalName(
          hospital ? hospital.name : "Unknown Hospital"
        );
      } catch (error) {
        console.error("Error fetching doctor:", error);
        setMessage("Could not load doctor information.");
      } finally {
        setLoading(false);
      }
    };

    fetchDoctor();
  }, [id]);

  const handleBooking = async () => {
    if (!appointmentDate || !appointmentTime) {
      setMessage("Please select both date and time.");
      return;
    }

    const userId = localStorage.getItem("userId");

    if (!userId) {
      setMessage("Please login again before booking an appointment.");
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
            appointment_date: appointmentDate,
            appointment_time: appointmentTime,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Booking failed");
      }

      setMessage("Appointment booked successfully!");
      setBookingSuccessful(true);
    } catch (error) {
      console.error("Booking error:", error);
      setMessage(error.message);
      setBookingSuccessful(false);
    }
  };

  if (loading) {
    return <p>Loading doctor information...</p>;
  }

  if (!doctor) {
    return <p>Doctor information not found.</p>;
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
            <strong>Hospital:</strong> {hospitalName}
          </p>

          <p>
            <strong>Experience:</strong> {doctor.experience} years
          </p>

          <p>
            <strong>Degrees:</strong> {doctor.degrees}
          </p>
        </div>

        <label>Appointment Date</label>

        <input
          type="date"
          value={appointmentDate}
          onChange={(e) => setAppointmentDate(e.target.value)}
        />

        <label>Appointment Time</label>

        <div className="time-slots">
          {timeSlots.map((time) => (
            <button
              type="button"
              key={time}
              className={
                appointmentTime === time
                  ? "time-slot selected"
                  : "time-slot"
              }
              onClick={() => setAppointmentTime(time)}
            >
              {time}
            </button>
          ))}
        </div>

        <button
          className="confirm-booking-button"
          onClick={handleBooking}
        >
          Confirm Appointment
        </button>

        {message && (
          <p className="booking-message">
            {message}
          </p>
        )}

        {bookingSuccessful && (
          <button
            type="button"
            onClick={() => navigate("/appointment-history")}
          >
            View Appointment History
          </button>
        )}

      </div>
    </div>
  );
}

export default AppointmentBooking;