<template>
  <Suspense>
    <ObjectComponent :id="id" :name="name" :object-index="objectIndex" />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import ObjectComponent from "@/components/routes/object/ObjectComponent.vue";
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";
defineProps<{ id: string; name: string; objectIndex: string }>();
</script>

<style scoped lang="scss"></style>
