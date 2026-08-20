import "./Hospitals.css";
import { useNavigate } from "react-router-dom";

function Hospitals() {
  const navigate = useNavigate();

  const hospitals = [
    {
      id: 1,
      name: "Apollo Hospital",
      address: "Jubilee Hills, Hyderabad",
      phone: "04012345678",
      rating: 4.8,
      specialty: "Cardiology",
    },
    {
      id: 2,
      name: "Yashoda Hospital",
      address: "Somajiguda, Hyderabad",
      phone: "04087654321",
      rating: 4.7,
      specialty: "Neurology",
    },
  ];

  return (
    <div className="hospitals-page">
      <h1>Hospitals</h1>

      <div className="hospital-list">
        {hospitals.map((hospital) => (
          <div className="hospital-card" key={hospital.id}>
            <div className="hospital-icon">🏥</div>

            <h2>{hospital.name}</h2>

            <p>
              <strong>Address:</strong> {hospital.address}
            </p>

            <p>
              <strong>Phone:</strong> {hospital.phone}
            </p>

            <p>
              <strong>Rating:</strong> ⭐ {hospital.rating}
            </p>

            <p>
              <strong>Specialty:</strong> {hospital.specialty}
            </p>

            <button
              className="view-hospital-button"
              onClick={() => navigate(`/doctors?hospital_id=${hospital.id}`)}
            >
              View Hospital
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Hospitals;