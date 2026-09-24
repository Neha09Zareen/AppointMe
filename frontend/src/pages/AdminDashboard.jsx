import { useEffect, useState } from "react";

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/admin-stats")
      .then((response) => response.json())
      .then((data) => {
        setStats(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching admin statistics:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: "30px" }}>
      <h1>Admin Dashboard</h1>

      <div
        style={{
          background: "#fff",
          padding: "20px",
          marginTop: "20px",
          borderRadius: "10px",
          boxShadow: "0 0 10px rgba(0,0,0,0.1)",
        }}
      >
        <h3>System Overview</h3>

        {loading ? (
          <p>Loading statistics...</p>
        ) : stats ? (
          <>
            <p>Total Doctors: {stats.total_doctors}</p>
            <p>Total Patients: {stats.total_patients}</p>
            <p>Appointments Today: {stats.appointments_today}</p>
            <p>Pending Feedback: {stats.pending_feedback}</p>
          </>
        ) : (
          <p>Unable to load statistics.</p>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;