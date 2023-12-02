export enum UserRole {
  user = "user",
  admin = "admin",
}

export const UserRoleTranslations = {
  [UserRole.admin]: "Администратор",
  [UserRole.user]: "Пользователь",
};

export function getEmptyUser() {
  return {
    _id: { $oid: "" },
    login: "",
    name: "",
    password: "",
    role: UserRole.user,
  };
}
