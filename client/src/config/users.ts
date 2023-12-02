export enum UserRole {
  user = "user",
  admin = "admin",
}

export const UserRoleTranslations = {
  [UserRole.admin]: "Администратор",
  [UserRole.user]: "Пользователь",
};
