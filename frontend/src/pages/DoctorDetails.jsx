import "./DoctorDetails.css";

function DoctorDetails() {
  const doctor = {
    name: "Dr. Rahul Sharma",
    specialization: "Cardiologist",
    experience: 8,
    degrees: "MBBS, MD",
    hospital: "Apollo Hospital",
  };

  return (
    <div className="doctor-details-page">
        <div className="doctor-details-card">
        <div className="doctor-details-icon">👨‍⚕️</div>

        <h1>{doctor.name}</h1>

        <p className="doctor-details-specialization">
            {doctor.specialization}
        </p>

        <div className="doctor-details-info">
            <p>
            <strong>Experience:</strong> {doctor.experience} years
            </p>

            <p>
            <strong>Degrees:</strong> {doctor.degrees}
            </p>

            <p>
            <strong>Hospital:</strong> {doctor.hospital}
            </p>
        </div>

        <button className="book-button">
            Book Appointment
        </button>
        </div>
    </div>
    );
}

export default DoctorDetails;