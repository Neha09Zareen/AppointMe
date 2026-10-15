
import { useCallback, useEffect, useState } from "react";
import "./AdminDashboard.css";

const API = "http://127.0.0.1:5000";

function getList(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.value)) return data.value;
  if (Array.isArray(data?.doctors)) return data.doctors;
  if (Array.isArray(data?.appointments)) return data.appointments;
  return [];
}

export default function AdminDashboard() {
  const [stats, setStats] = useState({
    total_patients: 0,
    total_doctors: 0,
    appointments_today: 0,
    pending_feedback: 0,
  });

  const [doctors, setDoctors] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const responses = await Promise.all([
        fetch(`${API}/admin-stats`),
        fetch(`${API}/admin/pending-doctors`),
        fetch(`${API}/admin/appointments`),
      ]);

      const failedResponse = responses.find((response) => !response.ok);

      if (failedResponse) {
        throw new Error(
          `Request failed with status ${failedResponse.status}.`
        );
      }

      const [statsData, doctorsData, appointmentsData] = await Promise.all(
        responses.map((response) => response.json())
      );

      setStats((previous) => ({ ...previous, ...statsData }));
      setDoctors(getList(doctorsData));
      setAppointments(getList(appointmentsData));
    } catch (err) {
      console.error("Admin dashboard error:", err);
      setError(
        "Could not load dashboard data. Check that the Flask backend is running and the admin API routes exist."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  async function updateDoctorStatus(doctorId, action) {
    if (!doctorId) {
      setError("Doctor ID is missing. Cannot update this application.");
      return;
    }

    setMessage("");
    setError("");

    try {
      const response = await fetch(
        `${API}/admin/doctors/${doctorId}/${action}`,
        { method: "PUT" }
      );

      const result = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(result.message || `Failed to ${action} doctor.`);
      }

      setMessage(
        result.message ||
          `Doctor ${action === "approve" ? "approved" : "rejected"} successfully.`
      );

      await loadDashboard();
    } catch (err) {
      setError(err.message || "Could not update doctor status.");
    }
  }

  return (
    <div className="admin-dashboard">
      <aside className="admin-sidebar">
        <h2>AppointMe</h2>
        <p>Admin Panel</p>

        
<nav>
  <button
    type="button"
    onClick={() => {
      document.getElementById("overview")?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }}
  >
    Overview
  </button>

  <button
    type="button"
    onClick={() => {
      document.getElementById("doctor-applications")?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }}
  >
    Doctor Approvals
  </button>

  <button
    type="button"
    onClick={() => {
      document.getElementById("appointments-section")?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }}
  >
    Appointments
  </button>
</nav>

        <button
          type="button"
          onClick={loadDashboard}
          disabled={loading}
        >
          {loading ? "Loading..." : "Refresh Data"}
        </button>
      </aside>

      <main className="admin-main">
        <header id="overview">
          <h1>Admin Dashboard</h1>
        </header>

        {message && <p role="status">{message}</p>}
        {error && <p role="alert">{error}</p>}

        <section className="admin-stats">
          <article>
            <h3>Total Patients</h3>
            <p>{stats.total_patients ?? 0}</p>
          </article>

          <article>
            <h3>Total Doctors</h3>
            <p>{stats.total_doctors ?? 0}</p>
          </article>

          <article>
            <h3>Appointments Today</h3>
            <p>{stats.appointments_today ?? 0}</p>
          </article>

          <article>
            <h3>Pending Feedback</h3>
            <p>{stats.pending_feedback ?? 0}</p>
          </article>
        </section>

        <section
          id="doctor-applications"
          className="admin-section"
        >
          <h2>Pending Doctor Applications</h2>

          {loading ? (
            <p>Loading doctor applications...</p>
          ) : doctors.length === 0 ? (
            <p>No pending doctor applications.</p>
          ) : (
            <div className="admin-table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Login ID</th>
                    <th>Specialization</th>
                    <th>Experience</th>
                    <th>Degrees</th>
                    <th>Actions</th>
                  </tr>
                </thead>

                <tbody>
                  {doctors.map((doctor) => (
                    <tr key={doctor.account_id ?? doctor.doctor_id}>
                      <td>{doctor.name || "—"}</td>
                      <td>{doctor.email || doctor.login_id || "—"}</td>
                      <td>{doctor.specialization || "—"}</td>
                      <td>{doctor.experience ?? "—"}</td>
                      <td>{doctor.degrees || "—"}</td>
                      <td>
                        <button
                          type="button"
                          onClick={() =>
                            updateDoctorStatus(doctor.doctor_id, "approve")
                          }
                          disabled={!doctor.doctor_id}
                        >
                          Approve
                        </button>

                        <button
                          type="button"
                          onClick={() =>
                            updateDoctorStatus(doctor.doctor_id, "reject")
                          }
                          disabled={!doctor.doctor_id}
                        >
                          Reject
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <section
          id="appointments-section"
          className="admin-section"
        >
          <h2>Appointments</h2>

          {loading ? (
            <p>Loading appointments...</p>
          ) : appointments.length === 0 ? (
            <p>No appointments found.</p>
          ) : (
            <div className="admin-table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Appointment ID</th>
                    <th>Patient</th>
                    <th>Doctor</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Status</th>
                  </tr>
                </thead>

                <tbody>
                  {appointments.map((appointment, index) => (
                    <tr key={appointment.id ?? index}>
                      <td>{appointment.id ?? "—"}</td>
                      <td>
                        {appointment.patient_name ||
                          appointment.patient ||
                          "—"}
                      </td>
                      <td>
                        {appointment.doctor_name ||
                          appointment.doctor ||
                          "—"}
                      </td>
                      <td>
                        {appointment.date ||
                          appointment.appointment_date ||
                          "—"}
                      </td>
                      <td>
                        {appointment.time ||
                          appointment.appointment_time ||
                          "—"}
                      </td>
                      <td>{appointment.status || "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}