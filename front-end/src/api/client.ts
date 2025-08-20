import axios from "axios";
import { toast } from "sonner";
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});
api.interceptors.response.use(
  (config) => config,
  (error) => {
    if (error?.response?.data?.detail || error?.message) {
      toast.error(error?.response?.data?.detail || error.message);
    }
    return Promise.reject(error);
  }
);
export const API_METHODS = {
  GET: "GET",
  POST: "POST",
  PUT: "PUT",
  PATCH: "PATCH",
  DELETE: "DELETE",
  OPTIONS: "OPTIONS",
} as const;
