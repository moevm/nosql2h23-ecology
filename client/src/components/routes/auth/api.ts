import { api } from "@/api";
import { User } from "@/types/users";

function fetchUser() {
  return api.get<User>("/auth/login");
}

function login(login: string, password: string) {
  return api.post<User>("/auth/login", { login, password });
}

function logout() {
  return api.delete("/auth/login");
}

function devLogin() {
  return api.get<User>("/auth/login/dev");
}

export const UserAPI = { fetchUser, login, logout, devLogin };
