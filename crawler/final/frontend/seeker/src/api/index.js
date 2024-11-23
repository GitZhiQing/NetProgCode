// src/api/index.js
import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8003", // FastAPI 后端的 URL
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
