<template>
  <Suspense>
    <MapsListComponent />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";
import MapsListComponent from "@/components/routes/maps/MapsListComponent.vue";
</script>

<style scoped lang="scss"></style>
