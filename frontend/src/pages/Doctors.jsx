import "./Doctors.css";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import DoctorSearch from "../components/DoctorSearch";
import DoctorFilter from "../components/DoctorFilter";

function Doctors() {
const navigate = useNavigate();

  const [searchTerm, setSearchTerm] = useState("");
  const [selectedSpecialization, setSelectedSpecialization] = useState("All");

  const [doctors, setDoctors] = useState([]);

  useEffect(() => {
  const fetchData = async () => {
    try {
      const doctorsResponse = await fetch("http://127.0.0.1:5000/doctors");
      const hospitalsResponse = await fetch("http://127.0.0.1:5000/hospitals");

      const doctorsData = await doctorsResponse.json();
      const hospitalsData = await hospitalsResponse.json();

      const hospitalMap = {};

      hospitalsData.forEach((hospital) => {
        hospitalMap[hospital.id] = hospital.name;
      });

      const doctorsWithHospitalNames = doctorsData.map((doctor) => ({
        ...doctor,
        hospital: hospitalMap[doctor.hospital_id] || "Unknown Hospital",
      }));

      setDoctors(doctorsWithHospitalNames);
      
    } catch (error) {
      console.error("Error fetching doctors and hospitals:", error);
    }
  };

  fetchData();
  }, []);

const filteredDoctors = doctors.filter((doctor) => {
  const search = searchTerm.toLowerCase();

  const matchesSearch =
    doctor.name.toLowerCase().includes(search) ||
    doctor.specialization.toLowerCase().includes(search) ||
    doctor.hospital.toLowerCase().includes(search);

  const matchesSpecialization =
    selectedSpecialization === "All" ||
    doctor.specialization === selectedSpecialization;

  return matchesSearch && matchesSpecialization;
});

return (
  <div className="doctors-page">
    <div className="doctors-header">
      <h1>Our Doctors</h1>
      <p>Find the right doctor for your healthcare needs.</p>
    </div>

    <DoctorSearch
      searchTerm={searchTerm}
      onSearchChange={setSearchTerm}
    />

    <DoctorFilter
      selectedSpecialization={selectedSpecialization}
      onSpecializationChange={setSelectedSpecialization}
    />

    <div className="doctor-grid">
      {filteredDoctors.map((doctor) => (
        <div className="doctor-card" key={doctor.id}>
          <div className="doctor-icon">👨‍⚕️</div>

          <h2>{doctor.name}</h2>

          <p className="doctor-specialization">
            {doctor.specialization}
          </p>

          <div className="doctor-info">
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

          <button
            className="details-button"
            onClick={() => navigate(`/doctor/${doctor.id}`)}
          >
            View Details
          </button>
        </div>
      ))}
    </div>
  </div>
);
}

export default Doctors;