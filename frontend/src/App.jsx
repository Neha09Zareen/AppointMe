import AppointmentHistory from "./pages/AppointmentHistory";
import AppointmentBooking from "./pages/AppointmentBooking";
import AdminDashboard from "./pages/AdminDashboard";
import DoctorDashboard from "./pages/DoctorDashboard";
import Feedback from "./pages/Feedback";

import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Login from "./pages/Login";
import Register from "./pages/Register";

import Hospitals from "./pages/Hospitals";
import Doctors from "./pages/Doctors";
import DoctorDetails from "./pages/DoctorDetails";

import ProtectedRoute from "./ProtectedRoute";

function AppContent() {
  const location = useLocation();

  return (
    <>
      {/* Hide Navbar on the starting/register page */}
      {location.pathname !== "/" && <Navbar />}

      <Routes>
        {/* AppointMe Starting Page */}
        <Route path="/" element={<Register />} />

        {/* Registration and Login */}
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        {/* Protected Patient Flow */}
        <Route
          path="/hospitals"
          element={
            <ProtectedRoute>
              <Hospitals />
            </ProtectedRoute>
          }
        />

        <Route
          path="/doctors"
          element={
            <ProtectedRoute>
              <Doctors />
            </ProtectedRoute>
          }
        />

        <Route
          path="/doctor/:id"
          element={
            <ProtectedRoute>
              <DoctorDetails />
            </ProtectedRoute>
          }
        />

        <Route
          path="/book-appointment/:id"
          element={
            <ProtectedRoute>
              <AppointmentBooking />
            </ProtectedRoute>
          }
        />

        <Route
          path="/appointment-history"
          element={
            <ProtectedRoute>
              <AppointmentHistory />
            </ProtectedRoute>
          }
        />

        <Route
          path="/feedback"
          element={
            <ProtectedRoute>
              <Feedback />
            </ProtectedRoute>
          }
        />

        {/* Doctor Dashboard */}
        <Route path="/doctor" element={<DoctorDashboard />} />

        {/* Admin Dashboard */}
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>

      <Footer />
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;