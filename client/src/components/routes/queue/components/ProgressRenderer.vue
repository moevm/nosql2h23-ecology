<template>
  <div v-bs-tooltip="`${rounded}%`" class="progress col" role="progressbar">
    <div
      class="progress-bar progress-bar-striped progress-bar-animated"
      :style="`width: ${rounded}%`"
    >
      {{ rounded }}%
    </div>
  </div>
</template>

<script setup lang="ts">
import { ICellRendererParams } from "ag-grid-community";
import { computed } from "vue";
import { QueueItemInfo } from "@/types/queue";

const props = defineProps<{
  params: ICellRendererParams<QueueItemInfo, number>;
}>();

const rounded = computed(() => Math.round(props.params.value));
</script>

<style scoped lang="scss"></style>
