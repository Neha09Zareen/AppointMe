import { useEffect, useState } from "react";

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [pendingDoctors, setPendingDoctors] = useState([]);
  const [appointments, setAppointments] = useState([]);

  const [loading, setLoading] = useState(true);
  const [doctorLoading, setDoctorLoading] = useState(true);
  const [appointmentLoading, setAppointmentLoading] = useState(true);

  const [message, setMessage] = useState("");

  const fetchStats = () => {
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
  };

  const fetchPendingDoctors = () => {
    fetch("http://127.0.0.1:5000/admin/pending-doctors")
      .then((response) => response.json())
      .then((data) => {
        setPendingDoctors(data);
        setDoctorLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching pending doctors:", error);
        setDoctorLoading(false);
      });
  };

  const fetchAppointments = () => {
    fetch("http://127.0.0.1:5000/admin/appointments")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Could not fetch appointments");
        }

        return response.json();
      })
      .then((data) => {
        setAppointments(data);
        setAppointmentLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching appointments:", error);
        setAppointmentLoading(false);
      });
  };

  useEffect(() => {
    fetchStats();
    fetchPendingDoctors();
    fetchAppointments();
  }, []);

  const handleApprove = async (doctorId) => {
    setMessage("");

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/admin/doctors/${doctorId}/approve`,
        {
          method: "PUT",
        }
      );

      const data = await response.json();

      if (response.ok) {
        setMessage("Doctor approved successfully.");

        fetchPendingDoctors();
        fetchStats();
      } else {
        setMessage(data.message || "Could not approve doctor.");
      }
    } catch (error) {
      console.error("Error approving doctor:", error);
      setMessage("Could not connect to backend.");
    }
  };

  const handleReject = async (doctorId) => {
    setMessage("");

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/admin/doctors/${doctorId}/reject`,
        {
          method: "PUT",
        }
      );

      const data = await response.json();

      if (response.ok) {
        setMessage("Doctor rejected successfully.");

        fetchPendingDoctors();
      } else {
        setMessage(data.message || "Could not reject doctor.");
      }
    } catch (error) {
      console.error("Error rejecting doctor:", error);
      setMessage("Could not connect to backend.");
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>Admin Dashboard</h1>

      {/* SYSTEM OVERVIEW */}

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

            <p>
              Appointments Today: {stats.appointments_today}
            </p>

            <p>
              Pending Feedback: {stats.pending_feedback}
            </p>
          </>
        ) : (
          <p>Unable to load statistics.</p>
        )}
      </div>

      {/* PENDING DOCTOR APPROVALS */}

      <div
        style={{
          background: "#fff",
          padding: "20px",
          marginTop: "30px",
          borderRadius: "10px",
          boxShadow: "0 0 10px rgba(0,0,0,0.1)",
        }}
      >
        <h3>Pending Doctor Approvals</h3>

        {message && <p>{message}</p>}

        {doctorLoading ? (
          <p>Loading pending doctors...</p>
        ) : pendingDoctors.length === 0 ? (
          <p>No pending doctor registrations.</p>
        ) : (
          <div>
            {pendingDoctors.map((doctor) => (
              <div
                key={doctor.doctor_id}
                style={{
                  border: "1px solid #ccc",
                  borderRadius: "8px",
                  padding: "15px",
                  marginBottom: "15px",
                }}
              >
                <h4>{doctor.name}</h4>

                <p>
                  <strong>Email:</strong> {doctor.email}
                </p>

                <p>
                  <strong>Specialization:</strong>{" "}
                  {doctor.specialization}
                </p>

                <p>
                  <strong>Experience:</strong>{" "}
                  {doctor.experience} years
                </p>

                <p>
                  <strong>Degrees:</strong> {doctor.degrees}
                </p>

                <p>
                  <strong>Hospital ID:</strong>{" "}
                  {doctor.hospital_id}
                </p>

                <p>
                  <strong>Status:</strong> {doctor.status}
                </p>

                <button
                  onClick={() =>
                    handleApprove(doctor.doctor_id)
                  }
                  style={{
                    marginRight: "10px",
                  }}
                >
                  Approve
                </button>

                <button
                  onClick={() =>
                    handleReject(doctor.doctor_id)
                  }
                >
                  Reject
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ALL APPOINTMENTS */}

      <div
        style={{
          background: "#fff",
          padding: "20px",
          marginTop: "30px",
          borderRadius: "10px",
          boxShadow: "0 0 10px rgba(0,0,0,0.1)",
        }}
      >
        <h3>All Appointments</h3>

        {appointmentLoading ? (
          <p>Loading appointments...</p>
        ) : appointments.length === 0 ? (
          <p>No appointments found.</p>
        ) : (
          <div>
            {appointments.map((appointment) => (
              <div
                key={appointment.id}
                style={{
                  border: "1px solid #ccc",
                  borderRadius: "8px",
                  padding: "15px",
                  marginBottom: "15px",
                }}
              >
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
      </div>
    </div>
  );
}

export default AdminDashboard;