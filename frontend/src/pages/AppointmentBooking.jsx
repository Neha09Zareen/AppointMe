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

  // Specific appointment slots
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

  // Get today's date in YYYY-MM-DD format
  const getTodayDate = () => {
    const today = new Date();

    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  };

  const todayDate = getTodayDate();

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

  const handleDateChange = (e) => {
    const selectedDate = e.target.value;

    setAppointmentDate(selectedDate);
    setAppointmentTime("");
    setMessage("");

    // Extra protection against selecting a past date
    if (selectedDate < todayDate) {
      setAppointmentDate("");
      setMessage("Please select today or a future date.");
    }
  };

  const handleBooking = async () => {
    if (!appointmentDate || !appointmentTime) {
      setMessage("Please select both date and time.");
      return;
    }

    // Prevent past dates
    if (appointmentDate < todayDate) {
      setMessage("Please select today or a future date.");
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
          min={todayDate}
          value={appointmentDate}
          onChange={handleDateChange}
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
              onClick={() => {
                setAppointmentTime(time);
                setMessage("");
              }}
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