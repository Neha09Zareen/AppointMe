
import "./Doctors.css";
import { useState, useEffect, useMemo } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import DoctorSearch from "../components/DoctorSearch";
import DoctorFilter from "../components/DoctorFilter";

const API_URL = "http://127.0.0.1:5000";

function Doctors() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const hospitalId = searchParams.get("hospital_id");

  const [searchTerm, setSearchTerm] = useState("");
  const [selectedSpecialization, setSelectedSpecialization] =
    useState("All");
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function fetchData() {
      try {
        setLoading(true);
        setError("");

        const [doctorsResponse, hospitalsResponse] =
          await Promise.all([
            fetch(`${API_URL}/doctors`),
            fetch(`${API_URL}/hospitals`),
          ]);

        if (!doctorsResponse.ok || !hospitalsResponse.ok) {
          throw new Error("Could not load doctors or hospitals.");
        }

        const doctorsData = await doctorsResponse.json();
        const hospitalsData = await hospitalsResponse.json();

        if (!Array.isArray(doctorsData) ||
            !Array.isArray(hospitalsData)) {
          throw new Error("The server returned an unexpected response.");
        }

        const hospitalMap = Object.fromEntries(
          hospitalsData.map((hospital) => [
            String(hospital.id),
            hospital.name || "Unknown Hospital",
          ])
        );

        const cleanedDoctors = doctorsData.map((doctor) => ({
          ...doctor,
          name: doctor.name || "Doctor",
          specialization: (doctor.specialization || "").trim(),
          hospital:
            hospitalMap[String(doctor.hospital_id)] ||
            doctor.hospital ||
            "Unknown Hospital",
        }));

        if (!cancelled) {
          setDoctors(cleanedDoctors);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Unable to load doctors.");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchData();

    return () => {
      cancelled = true;
    };
  }, []);

  // Build the filter options from the doctors returned by the backend.
  
const hospitalDoctors = useMemo(() => {
  return doctors.filter(
    (doctor) =>
      !hospitalId ||
      String(doctor.hospital_id) === String(hospitalId)
  );
}, [doctors, hospitalId]);

const specializations = useMemo(() => {
  return [
    ...new Set(
      hospitalDoctors
        .map((doctor) => doctor.specialization)
        .filter(Boolean)
    ),
  ].sort((a, b) => a.localeCompare(b));
}, [hospitalDoctors]);

  // If the available doctors change, don't leave an invalid filter selected.
  useEffect(() => {
    if (
      selectedSpecialization !== "All" &&
      !specializations.some(
        (item) =>
          item.toLowerCase() === selectedSpecialization.toLowerCase()
      )
    ) {
      setSelectedSpecialization("All");
    }
  }, [specializations, selectedSpecialization]);

  const filteredDoctors = useMemo(() => {
    const search = searchTerm.trim().toLowerCase();

    return hospitalDoctors.filter((doctor) => {
      const matchesSearch =
        !search ||
        doctor.name.toLowerCase().includes(search) ||
        doctor.specialization.toLowerCase().includes(search) ||
        doctor.hospital.toLowerCase().includes(search) ||
        String(doctor.degrees || "").toLowerCase().includes(search);

      const matchesSpecialization =
        selectedSpecialization === "All" ||
        doctor.specialization.toLowerCase() ===
          selectedSpecialization.toLowerCase();

      const matchesHospital =
        !hospitalId ||
        String(doctor.hospital_id) === String(hospitalId);

      return (
        matchesSearch &&
        matchesSpecialization &&
        matchesHospital
      );
    });
  }, [hospitalDoctors, searchTerm, selectedSpecialization]);

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
        specializations={specializations}
      />

      {loading ? (
        <p>Loading doctors...</p>
      ) : error ? (
        <p role="alert">{error}</p>
      ) : filteredDoctors.length === 0 ? (
        <p>
          {doctors.length === 0
            ? "No approved doctors available yet. Please check again after a doctor is approved."
            : "No doctors match your search or selected filters."}
        </p>
      ) : (
        <div className="doctor-grid">
          {filteredDoctors.map((doctor) => (
            <div className="doctor-card" key={doctor.id}>
              <div className="doctor-icon" aria-hidden="true">
                🩺
              </div>

              <h2>{doctor.name}</h2>
              <p className="doctor-specialization">
                {doctor.specialization || "General"}
              </p>

              <div className="doctor-info">
                <p>
                  <strong>Experience:</strong>{" "}
                  {doctor.experience ?? "Not specified"}
                  {doctor.experience != null ? " years" : ""}
                </p>
                <p>
                  <strong>Degrees:</strong>{" "}
                  {doctor.degrees || "Not specified"}
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
      )}
    </div>
  );
}

export default Doctors;