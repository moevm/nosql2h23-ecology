<template>
  <div class="fs-4">
    <i v-if="params.value" class="bi bi-check-circle text-success" />
    <i v-else class="bi bi-x-circle text-danger" />
  </div>
</template>

<script setup lang="ts">
import { ICellRendererParams } from "ag-grid-community";

defineProps<{
  params: ICellRendererParams<any, boolean>;
}>();
</script>

<style scoped lang="scss"></style>
