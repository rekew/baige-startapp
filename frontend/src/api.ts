import axios from "axios";

interface User {
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string;
  date_of_birth: string; // Format: YYYY-MM-DD
  city: string;
  password: string;
}

interface UserLogin {
  email: string;
  password: string;
}

const api = axios.create({
  baseURL: "http://localhost:8008",
  withCredentials: true,
});

export const Api = {
  register: async (user: User) => {
    return api.post("/api/auth/register", user);
  },
  login: async (user: UserLogin) => {
    return api.post("/api/auth/login", user);
  },
};
