import { api } from "@/api";
import { UserSelfUpdate } from "@/components/routes/profile/types";

function updateSelf(data: UserSelfUpdate) {
  return api.put("/users/user/self", { ...data });
}

export const ProfileAPI = { updateSelf };
