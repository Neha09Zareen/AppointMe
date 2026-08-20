import "./Doctors.css";
import { useState } from "react";
import DoctorSearch from "../components/DoctorSearch";
import DoctorFilter from "../components/DoctorFilter";

function Doctors() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedSpecialization, setSelectedSpecialization] = useState("All");

const doctors = [
  {
    id: 1,
    name: "Dr. Rahul Sharma",
    specialization: "Cardiologist",
    experience: 8,
    degrees: "MBBS, MD",
    hospital: "Apollo Hospital",
  },
  {
    id: 2,
    name: "Dr. Ayesha Khan",
    specialization: "Neurologist",
    experience: 6,
    degrees: "MBBS, DM",
    hospital: "Yashoda Hospital",
  },
];

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

          <button className="details-button">
            View Details
          </button>
        </div>
      ))}
    </div>
  </div>
);
}

export default Doctors;