function DoctorDashboard() {
  return (
    <div style={{ padding: "30px" }}>
      <h1>Doctor Dashboard</h1>

      <div
        style={{
          background: "#fff",
          padding: "20px",
          marginTop: "20px",
          borderRadius: "10px",
          boxShadow: "0 0 10px rgba(0,0,0,0.1)",
        }}
      >
        <h3>Today's Appointments</h3>

        <ul>
          <li>9:00 AM - Ahmed Khan</li>
          <li>10:30 AM - Sara Ali</li>
          <li>12:00 PM - Fatima Noor</li>
          <li>2:00 PM - Mohammed Asif</li>
        </ul>
      </div>
    </div>
  );
}

export default DoctorDashboard;