import { createBrowserRouter } from "react-router";
import Landing from "@/pages/Landing";
import Authentication from "@/pages/Authentication";
import Home from "@/pages/Home";
import PrivateRoute from "./PrivateRoute";

const router = createBrowserRouter([
  {
    path: "/",
    Component: Authentication,
  },
  {
    path: "/landing",
    Component: Landing,
  },
  {
    path: "/home",
    Component: () => (
      <PrivateRoute>
        <Home />
      </PrivateRoute>
    ),
  },
]);

export default router;
