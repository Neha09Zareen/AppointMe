
import { useEffect, useState } from "react";

const API = "http://127.0.0.1:5000";

const sampleHospitals = [
  { name: "Apollo Hospital", phone: "040-23607777", rating: 4.8 },
  { name: "Yashoda Hospital", phone: "040-45674567", rating: 4.7 },
  { name: "Sunshine Hospital", phone: "040-44550000", rating: 4.5 },
  { name: "KIMS Hospital", phone: "040-44885000", rating: 4.6 },
  { name: "Care Hospital", phone: "040-61656565", rating: 4.4 },
];

export default function Hospitals() {
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchHospitals() {
      try {
        const response = await fetch(`${API}/hospitals`);
        if (!response.ok) throw new Error("Could not fetch hospitals.");

        const data = await response.json();
        const list = Array.isArray(data)
          ? data
          : data.hospitals || data.value || [];

        setHospitals(
          list.map((hospital) => {
            const sample = sampleHospitals.find(
              (item) =>
                item.name.toLowerCase() ===
                String(hospital.name || "").toLowerCase()
            );

            return {
              ...hospital,
              phone: sample?.phone || hospital.phone || "Contact hospital",
              rating: hospital.rating ?? sample?.rating ?? "Not rated",
            };
          })
        );
      } catch (err) {
        console.error(err);
        setError("Could not load hospitals. Please check the backend.");
      } finally {
        setLoading(false);
      }
    }

    fetchHospitals();
  }, []);

  return (
    <main className="hospitals-page">
      <header className="hospitals-header">
  <h1>Hospitals</h1>
</header>

      {loading && <p>Loading hospitals...</p>}
      {error && <p role="alert">{error}</p>}

      {!loading && !error && hospitals.length === 0 && (
        <p>No hospitals are available right now.</p>
      )}

      {!loading && !error && (
        <div className="hospital-list">
          {hospitals.map((hospital) => (
            <article className="hospital-card" key={hospital.id}>
              <div className="hospital-card-top">
                <div className="hospital-icon" aria-hidden="true">🏥</div>
                <span className="hospital-rating">★ {hospital.rating}</span>
              </div>

              <h2>{hospital.name}</h2>

              <p className="hospital-address">
                <span aria-hidden="true">📍</span>{" "}
                {hospital.address || "Address not available"}
              </p>

              <p className="hospital-phone">
                <span aria-hidden="true">☎</span> {hospital.phone}
              </p>

              <button
                type="button"
                className="hospital-doctors-button"
                onClick={() => {
                  window.location.href =
                    `/doctors?hospital_id=${encodeURIComponent(hospital.id)}`;
                }}
              >
                View Doctors →
              </button>
            </article>
          ))}
        </div>
      )}
    </main>
  );
}