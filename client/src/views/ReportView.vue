<template>
  <Suspense>
    <ReportComponent :id="id" />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import ReportComponent from "@/components/routes/report/ReportComponent.vue";
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";
defineProps<{ id: string }>();
</script>

<style scoped lang="scss"></style>
