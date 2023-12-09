import { api } from "@/api";
import { User } from "@/types/users";
import { UserCreation } from "@/components/routes/users/types";

function getUsers() {
  return api.get<User[]>("/users/");
}

function createUser(user: UserCreation) {
  return api.post<string>("/users/", user);
}

function deleteUser(id: string) {
  return api.delete(`/users/user/${id}`);
}

function updateUser(id: string, user: UserCreation) {
  return api.put(`/users/user/${id}`, user);
}

export const UserAdminAPI = { getUsers, createUser, deleteUser, updateUser };
