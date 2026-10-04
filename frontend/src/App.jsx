import AppointmentHistory from "./pages/AppointmentHistory";
import AppointmentBooking from "./pages/AppointmentBooking";
import AdminDashboard from "./pages/AdminDashboard";
import DoctorDashboard from "./pages/DoctorDashboard";
import Feedback from "./pages/Feedback";
import RoleSelection from "./pages/RoleSelection";
import DoctorLogin from "./pages/DoctorLogin";
import DoctorRegister from "./pages/DoctorRegister";
import AdminLogin from "./pages/AdminLogin";
import AdminRegister from "./pages/AdminRegister";

import {
  BrowserRouter,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";

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

  const hideNavbar =
    location.pathname === "/" ||
    location.pathname === "/login" ||
    location.pathname === "/register" ||
    location.pathname === "/doctor-login" ||
    location.pathname === "/doctor-register" ||
    location.pathname === "/admin-login" ||
    location.pathname === "/admin-register";

  return (
    <>
      {!hideNavbar && <Navbar />}

      <Routes>

        {/* ROLE SELECTION */}
        <Route
          path="/"
          element={<RoleSelection />}
        />

        {/* PATIENT */}
        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/hospitals"
          element={
            <ProtectedRoute requiredRole="patient">
              <Hospitals />
            </ProtectedRoute>
          }
        />

        <Route
          path="/doctors"
          element={
            <ProtectedRoute requiredRole="patient">
              <Doctors />
            </ProtectedRoute>
          }
        />

        <Route
          path="/doctor/:id"
          element={
            <ProtectedRoute requiredRole="patient">
              <DoctorDetails />
            </ProtectedRoute>
          }
        />

        <Route
          path="/book-appointment/:id"
          element={
            <ProtectedRoute requiredRole="patient">
              <AppointmentBooking />
            </ProtectedRoute>
          }
        />

        <Route
          path="/appointment-history"
          element={
            <ProtectedRoute requiredRole="patient">
              <AppointmentHistory />
            </ProtectedRoute>
          }
        />

        <Route
          path="/feedback"
          element={
            <ProtectedRoute requiredRole="patient">
              <Feedback />
            </ProtectedRoute>
          }
        />

        {/* DOCTOR */}
        <Route
          path="/doctor-login"
          element={<DoctorLogin />}
        />

        <Route
          path="/doctor-register"
          element={<DoctorRegister />}
        />

        <Route
          path="/doctor"
          element={
            <ProtectedRoute requiredRole="doctor">
              <DoctorDashboard />
            </ProtectedRoute>
          }
        />

        {/* ADMIN */}
        <Route
          path="/admin-login"
          element={<AdminLogin />}
        />

        <Route
          path="/admin-register"
          element={<AdminRegister />}
        />

        <Route
          path="/admin"
          element={
            <ProtectedRoute requiredRole="admin">
              <AdminDashboard />
            </ProtectedRoute>
          }
        />

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