import { ObjectInfo } from "@/types/objects";
import { User } from "@/types/users";

export interface Dump {
  objects: ObjectInfo[];
  users: User[];
}
