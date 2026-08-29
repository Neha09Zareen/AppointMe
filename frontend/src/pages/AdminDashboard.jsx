function AdminDashboard() {
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

        <p>Total Doctors: 12</p>
        <p>Total Patients: 145</p>
        <p>Appointments Today: 28</p>
        <p>Pending Feedback: 6</p>
      </div>
    </div>
  );
}

export default AdminDashboard;