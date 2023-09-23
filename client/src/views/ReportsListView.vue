<template>
  <Suspense>
    <ReportsListComponent />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import ReportsListComponent from "@/components/routes/reports/ReportsListComponent.vue";
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";
</script>

<style scoped lang="scss"></style>
