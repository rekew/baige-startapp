import axios from "axios";

interface User {
  username: string;
  password: string;
  firstName: string;
  surname: string;
  email: string;
  phoneNumber: string;
}

interface userLogin {
  username: string;
  password: string;
}

const api = axios.create({
  baseURL: "http://localhost:4000",
  withCredentials: true,
});

export const Api = {
  register: async (user: User) => {
    return api.post("/register", user);
  },
  login: async (user: userLogin) => {
    return api.post("/login", user);
  },
};
