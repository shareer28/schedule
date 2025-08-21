import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";

import {
  coordinator as _coordinator,
  wasmConnector,
} from "@uwdata/mosaic-core";

import { RouterProvider } from "react-router";
import router from "./routes.tsx";

// Coordinator is a singleton
const coordinator = _coordinator();

// Initialize the database connector
const initApp = async () => {
  await coordinator.databaseConnector(wasmConnector());
  
  createRoot(document.getElementById("root")!).render(
    <StrictMode>
      <RouterProvider router={router} />
    </StrictMode>
  );
};

initApp().catch(console.error);
