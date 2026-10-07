import { useEffect, useState } from "react";

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [pendingDoctors, setPendingDoctors] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [message, setMessage] = useState("");

  const fetchData = async () => {
    try {
      const statsResponse = await fetch(
        "http://127.0.0.1:5000/admin-stats"
      );

      const statsData = await statsResponse.json();
      setStats(statsData);

      const doctorsResponse = await fetch(
        "http://127.0.0.1:5000/admin/pending-doctors"
      );

      const doctorsData = await doctorsResponse.json();
      setPendingDoctors(doctorsData);

      const appointmentsResponse = await fetch(
        "http://127.0.0.1:5000/admin/appointments"
      );

      const appointmentsData = await appointmentsResponse.json();
      setAppointments(appointmentsData);
    } catch (error) {
      console.error("Admin dashboard error:", error);
      setMessage("Could not load admin dashboard data.");
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleDoctorAction = async (doctorId, action) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/admin/doctors/${doctorId}/${action}`,
        {
          method: "PUT",
        }
      );

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message);
        fetchData();
      } else {
        setMessage(data.message || "Action failed.");
      }
    } catch (error) {
      console.error("Doctor action error:", error);
      setMessage("Could not connect to backend.");
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>Admin Dashboard</h1>

      {message && <p>{message}</p>}

      {/* SYSTEM OVERVIEW */}
      <section>
        <h2>System Overview</h2>

        {stats ? (
          <div>
            <p>
              <strong>Total Patients:</strong>{" "}
              {stats.total_patients}
            </p>

            <p>
              <strong>Total Doctors:</strong>{" "}
              {stats.total_doctors}
            </p>

            <p>
              <strong>Total Appointments:</strong>{" "}
              {stats.total_appointments}
            </p>

            <p>
              <strong>Total Feedback:</strong>{" "}
              {stats.total_feedback}
            </p>
          </div>
        ) : (
          <p>Loading statistics...</p>
        )}
      </section>

      <hr />

      {/* PENDING DOCTORS */}
      <section>
        <h2>Pending Doctor Approvals</h2>

        {pendingDoctors.length === 0 ? (
          <p>No pending doctor registrations.</p>
        ) : (
          <div>
            {pendingDoctors.map((doctor) => (
              <div
                key={doctor.id}
                style={{
                  border: "1px solid #ccc",
                  borderRadius: "10px",
                  padding: "20px",
                  marginBottom: "15px",
                }}
              >
                <p>
                  <strong>Doctor ID:</strong> {doctor.id}
                </p>

                <p>
                  <strong>Name:</strong> {doctor.name}
                </p>

                <p>
                  <strong>Email:</strong> {doctor.email}
                </p>

                <p>
                  <strong>Phone:</strong> {doctor.phone}
                </p>

                <p>
                  <strong>Specialization:</strong>{" "}
                  {doctor.specialization}
                </p>

                <p>
                  <strong>Experience:</strong>{" "}
                  {doctor.experience}
                </p>

                <p>
                  <strong>Degrees:</strong> {doctor.degrees}
                </p>

                <p>
                  <strong>Status:</strong> {doctor.status}
                </p>

                <button
                  onClick={() =>
                    handleDoctorAction(doctor.id, "approve")
                  }
                >
                  Approve
                </button>

                {" "}

                <button
                  onClick={() =>
                    handleDoctorAction(doctor.id, "reject")
                  }
                >
                  Reject
                </button>
              </div>
            ))}
          </div>
        )}
      </section>

      <hr />

      {/* ALL APPOINTMENTS */}
      <section>
        <h2>All Appointments</h2>

        {appointments.length === 0 ? (
          <p>No appointments found.</p>
        ) : (
          <div>
            {appointments.map((appointment, index) => (
              <div
                key={appointment.id}
                style={{
                  border: "1px solid #ccc",
                  borderRadius: "10px",
                  padding: "20px",
                  marginBottom: "15px",
                }}
              >
                <p>
                  <strong>Serial No:</strong> {index + 1}
                </p>

                <p>
                  <strong>Appointment ID:</strong>{" "}
                  {appointment.id}
                </p>

                <p>
                  <strong>Patient:</strong>{" "}
                  {appointment.patient_name}
                </p>

                <p>
                  <strong>Patient ID:</strong>{" "}
                  {appointment.patient_id}
                </p>

                <p>
                  <strong>Doctor:</strong>{" "}
                  {appointment.doctor_name}
                </p>

                <p>
                  <strong>Doctor ID:</strong>{" "}
                  {appointment.doctor_id}
                </p>

                <p>
                  <strong>Date:</strong>{" "}
                  {appointment.appointment_date}
                </p>

                <p>
                  <strong>Time:</strong>{" "}
                  {appointment.appointment_time}
                </p>

                <p>
                  <strong>Status:</strong>{" "}
                  {appointment.status}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default AdminDashboard;