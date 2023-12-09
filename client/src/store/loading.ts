import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useLoadingStore = defineStore("loading", () => {
  const isLoading = ref(true),
    enqueued = ref(0),
    processed = ref(0),
    errors = ref(0);

  const showProgress = computed(() => enqueued.value !== processed.value);

  function disableLoading() {
    isLoading.value = false;
  }

  function enableLoading() {
    isLoading.value = true;
  }

  function setLoading(state: boolean) {
    isLoading.value = state;
  }

  function enqueue() {
    enqueued.value++;
  }

  function dequeue(ok = true) {
    processed.value++;
    if (!ok) {
      errors.value++;
    }
    if (enqueued.value <= processed.value) {
      enqueued.value = processed.value = errors.value = 0;
    }
  }

  return {
    isLoading,
    enqueued,
    processed,
    errors,
    showProgress,
    disableLoading,
    enableLoading,
    setLoading,
    enqueue,
    dequeue,
  };
});
