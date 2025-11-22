import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router";
import router from "./route/route";
import "./styling/base.css";
import { ToastContainer } from "react-toastify";

createRoot(document.getElementById("root")!).render(
  <>
    <RouterProvider router={router} />
    <ToastContainer
      position="top-center"
      autoClose={5000}
      pauseOnFocusLoss
      pauseOnHover
      theme="colored"
    />
  </>
);
