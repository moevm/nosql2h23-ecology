<template>
  <div ref="modalEl" class="modal fade" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <slot name="header" :close="close"></slot>
        </div>
        <div class="modal-body">
          <slot name="body" :close="close"></slot>
        </div>
        <div class="modal-footer">
          <slot name="footer" :close="close"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import * as bootstrap from "bootstrap";
import { onMounted, readonly, ref } from "vue";

const props = withDefaults(
  defineProps<{
    backdrop: boolean | "static";
  }>(),
  { backdrop: true }
);

const modalEl = ref<HTMLDivElement | null>(null),
  modal = ref<bootstrap.Modal | null>(null);

onMounted(() => {
  if (modalEl.value)
    modal.value = new bootstrap.Modal(modalEl.value, {
      backdrop: props.backdrop,
    });
});

function open() {
  modal.value?.show();
}

function close() {
  modal.value?.hide();
}

defineExpose({ open, close, modal: readonly(modal) });
</script>

<style scoped lang="scss"></style>
