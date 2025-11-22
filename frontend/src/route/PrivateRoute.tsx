import { useAuth } from "../store/auth";
import type React from "react";
import { Navigate } from "react-router";

interface PrivateRouteProps {
  children: React.ReactNode;
}

const PrivateRoute = ({ children }: PrivateRouteProps) => {
  const { isAuthorized } = useAuth();
  console.log("isAuthorized", isAuthorized);
  if (isAuthorized) {
    return children;
  } else {
    return <Navigate to="/" replace />;
  }
};

export default PrivateRoute;
