import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, requiredRole }) {
  const isLoggedIn = localStorage.getItem("isLoggedIn");
  const userRole = localStorage.getItem("userRole");

  // Not logged in → go to role selection
  if (!isLoggedIn) {
    return <Navigate to="/" replace />;
  }

  // Logged in with the wrong role → block access
  if (userRole !== requiredRole) {
    return <Navigate to="/" replace />;
  }

  return children;
}

export default ProtectedRoute;