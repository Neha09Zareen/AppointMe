import "./DoctorDetails.css";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function DoctorDetails() {
  const { id } = useParams();

  const [doctor, setDoctor] = useState(null);
  const [hospitalName, setHospitalName] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDoctor = async () => {
      try {
        const doctorResponse = await fetch(
          `http://127.0.0.1:5000/doctors/${id}`
        );

        const doctorData = await doctorResponse.json();

        if (!doctorResponse.ok) {
          throw new Error("Doctor not found");
        }

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
      } finally {
        setLoading(false);
      }
    };

    fetchDoctor();
  }, [id]);

  if (loading) {
    return <p>Loading doctor details...</p>;
  }

  if (!doctor) {
    return <p>Doctor not found.</p>;
  }

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
            <strong>Hospital:</strong> {hospitalName}
          </p>
        </div>

        <button
          className="book-button"
          onClick={() => window.location.href = `/book-appointment/${doctor.id}`}
        >
          Book Appointment
        </button>
      </div>
    </div>
  );
}

export default DoctorDetails;