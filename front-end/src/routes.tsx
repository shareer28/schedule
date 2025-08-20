import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
} from "react-router";
import MainPage from "./pages/MainPage";
import App from "./App";
import UploadPage from "./pages/UploadPage";
import InspectPage from "./pages/InspectPage";
import ReferencePage from "./pages/ReferencePage";

const router = createBrowserRouter(
  createRoutesFromElements([
    <Route element={<App />}>
      <Route index element={<MainPage />}></Route>
      <Route path="upload" element={<UploadPage />}></Route>
      <Route path="inspect" element={<InspectPage />}></Route>
      <Route path="references" element={<ReferencePage />}></Route>
    </Route>,
  ])
);
export default router;
