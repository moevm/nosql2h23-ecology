<template>
  <div class="loading-spinner__div">
    <i class="bi bi-arrow-repeat fs-2 spinner-logo" />
    <b class="ms-2">
      Загрузка...
      {{ enqueued > 1 ? `[${processed}/${enqueued}]` : "" }}
    </b>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  processed: number;
  enqueued: number;
}>();
</script>

<style lang="scss">
.loading-spinner__div {
  position: fixed;
  z-index: 100000000;
  bottom: 16px;
  left: 16px;
  height: 50px;

  background-color: rgba(1, 1, 1, 0.75);
  color: white;
  border-radius: 16px;
  padding: 16px;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;

  .spinner-logo {
    animation: rotation 2s infinite linear;

    @keyframes rotation {
      from {
        transform: rotate(0deg);
      }
      to {
        transform: rotate(359deg);
      }
    }
  }
}
</style>
