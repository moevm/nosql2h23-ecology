import { defineStore } from "pinia";
import { computed, readonly, ref } from "vue";
import { User } from "@/components/routes/auth/types";
import { UserAPI } from "@/components/routes/auth/api";

export const useUserStore = defineStore("user", () => {
  const user = ref<User | null>(null);

  async function fetchUser() {
    try {
      user.value = (await UserAPI.fetchUser()).data;
    } catch (err) {
      user.value = null;
    }
  }

  async function login(login: string, password: string) {
    user.value = (await UserAPI.login(login, password)).data;
  }

  async function devLogin() {
    user.value = (await UserAPI.devLogin()).data;
  }

  async function logout() {
    user.value = null;
    await UserAPI.logout();
  }

  const isAuthed = computed(() => user.value !== null);
  const role = computed(() => user.value?.role || null);

  return {
    user: readonly(user),
    fetchUser,
    login,
    logout,
    devLogin,
    isAuthed,
    role,
  };
});
