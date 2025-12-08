import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000", // FastAPI backend URL
});

export const signupUser = async (data) => {
  return await API.post("/signup", data);
};

export const loginUser = async (data) => {
  return await API.post("/login", data);
};

export const getProfile = async (token) => {
  return await API.get("/profile", {
    headers: { Authorization: `Bearer ${token}` },
  });
};
