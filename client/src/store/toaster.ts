import { ToastData } from "@/types/toast";
import { defineStore } from "pinia";
import { readonly, ref } from "vue";

export const useToaster = defineStore("toasts", () => {
  const id = ref(0);
  const toasts = ref<ToastData[]>([]);

  function addToast(toast: Omit<ToastData, "id">) {
    id.value++;
    toasts.value.push({ ...toast, id: id.value });
  }

  function deleteToast(id: number) {
    toasts.value = toasts.value.filter((toast) => toast.id !== id);
  }

  return { addToast, deleteToast, toasts: readonly(toasts) };
});
