<template>
  <Suspense>
    <AnomaliesListComponent />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import AnomaliesListComponent from "@/components/routes/anomalies/AnomaliesListComponent.vue";
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";
</script>

<style scoped lang="scss"></style>
