<template>
  <span class="badge" :class="`bg-${bgClass}`">
    {{ QueueStatusTranslation[params.value] }}
  </span>
</template>

<script setup lang="ts">
import { ICellRendererParams } from "ag-grid-community";
import { QueueStatus, QueueStatusTranslation } from "@/config/queue";

const props = defineProps<{
  params: ICellRendererParams<any, QueueStatus>;
}>();

const bgClass = ["success", "info", "warning"][
  [QueueStatus.processing, QueueStatus.enqueued, QueueStatus.stopped].indexOf(
    props.params.value
  )
];
</script>

<style scoped lang="scss"></style>
