<template>
  <div class="row ps-3 gap-1">
    <button
      v-for="action of params.actions"
      v-show="show(action)"
      :key="action.icon + action.tooltip"
      v-bs-tooltip.top="action.tooltip"
      class="btn col-auto rounded-circle"
      :class="action.button"
      @click="action.onClicked?.(action, params.data)"
    >
      <i :class="action.icon"></i>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ICellRendererParams } from "ag-grid-community";
import { Action } from "@/types/ag-grid/actions";

const props = defineProps<{
  params: ICellRendererParams & { actions: Action[] };
}>();

function show(action: Action) {
  switch (typeof action.hide) {
    case "boolean":
      return !action.hide;
    case "function":
      return !action.hide(props.params.data);
  }
  return true;
}
</script>

<style scoped lang="scss"></style>
