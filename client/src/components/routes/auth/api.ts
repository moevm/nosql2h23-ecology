import { api } from "@/api";
import { User } from "@/components/routes/auth/types";

export function fetchUser() {
  return api.get<User>("/auth/login");
}

export function login(login: string, password: string) {
  return api.post<User>("/auth/login", { login, password });
}

export function logout() {
  return api.delete("/auth/login");
}

export function devLogin() {
  return api.get<User>("/auth/login/dev");
}

export const UserAPI = { fetchUser, login, logout, devLogin };
