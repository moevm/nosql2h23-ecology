<template>
  <Suspense>
    <QueueComponent />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import QueueComponent from "@/components/routes/queue/QueueComponent.vue";
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";
</script>

<style scoped lang="scss"></style>
