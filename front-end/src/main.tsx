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
await coordinator.databaseConnector(wasmConnector());

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
