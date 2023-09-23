<template>
  <div ref="toastElement" class="toast" role="alert">
    <div class="toast-header">
      <slot name="title"></slot>
    </div>
    <div class="toast-body">
      <slot name="body"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, readonly, withDefaults } from "vue";
import { useEventListener } from "@vueuse/core";
import { Toast } from "bootstrap";

const toastElement = ref<HTMLElement | null>(null);
const toast = ref<Toast | null>(null);

const props = withDefaults(
  defineProps<{
    animation?: boolean;
    autohide?: boolean;
    delay?: number;
  }>(),
  { animation: true, autohide: true, delay: 5000 }
);
const emit = defineEmits(["hide", "hidden", "show", "shown", "mounted"]);

onMounted(() => {
  if (toastElement.value)
    toast.value = new Toast(toastElement.value, {
      delay: props.delay,
      animation: props.animation,
      autohide: props.autohide,
    });

  useEventListener(toastElement, "hide.bs.toast", () => {
    emit("hide");
  });
  useEventListener(toastElement, "hidden.bs.toast", () => {
    emit("hidden");
  });
  useEventListener(toastElement, "show.bs.toast", () => {
    emit("show");
  });
  useEventListener(toastElement, "shown.bs.toast", () => {
    emit("shown");
  });

  emit("mounted", toast.value);
});

defineExpose({
  toast: readonly(toast),
});
</script>

<style scoped lang="scss"></style>
