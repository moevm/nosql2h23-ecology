<template>
  <Suspense>
    <ObjectsListComponent />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import ObjectsListComponent from "@/components/routes/objects/ObjectsListComponent.vue";
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";
</script>

<style scoped lang="scss"></style>
