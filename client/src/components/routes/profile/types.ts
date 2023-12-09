import { User } from "@/types/users";

export type UserSelfUpdate = Omit<User, "_id" | "role">;
