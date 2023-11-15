<template>
  <Suspense>
    <MapComponent :id="id" :name="name" :object-index="objectIndex" />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import MapComponent from "@/components/routes/map/MapComponent.vue";
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";

defineProps<{ id: string; name?: string; objectIndex?: string }>();
</script>

<style scoped lang="scss"></style>
