import { User } from "@/types/users";

export type UserCreation = Omit<User, "_id">;
