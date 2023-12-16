import { api } from "@/api";
import { UserCreation } from "@/components/routes/users/types";


function createUser(user: UserCreation) {
  return api.post<string>("/users/", user);
}

function deleteUser(id: string) {
  return api.delete(`/users/user/${id}`);
}

function updateUser(id: string, user: UserCreation) {
  return api.put(`/users/user/${id}`, user);
}

export const UserAdminAPI = { createUser, deleteUser, updateUser };
