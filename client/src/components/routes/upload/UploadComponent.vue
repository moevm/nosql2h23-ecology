<template>
  <div class="container mt-3">
    <div class="m-auto col-10 col-lg-6">
      <FormKit type="form" :actions="false" @submit="submit">
        <FormKit
          v-model="files"
          name="files"
          type="file"
          accept=".tiff, .tif"
          multiple="true"
          label="Карты"
          :validation-rules="{ checkFormat }"
          validation="required|checkFormat"
          validation-visibility="live"
          :validation-messages="{
            checkFormat: 'Требуются файлы .tif/.tiff',
          }"
        />
        <FormKitSchema :schema="namesSchema" />
        <FormKit
          outer-class="text-end"
          input-class="$reset btn btn-success"
          type="submit"
          label="Загрузить"
        />
      </FormKit>
    </div>
  </div>
</template>

<script setup lang="ts">
import { uploadMap } from "@/components/routes/upload/api";
import { FormKitGroupValue, FormKitNode } from "@formkit/core";
import { useToaster } from "@/store/toaster";
import { ToastTypes } from "@/config/toast";
import { computed, ref } from "vue";

const tiffRegExp = /.(tif|tiff)$/i;

function checkFormat(node: FormKitNode) {
  return (node.value as { name: string }[]).every((f) =>
    tiffRegExp.test(f.name)
  );
}

const toaster = useToaster();

const files = ref<{ name: string; file: File }[]>([]);

const namesSchema = computed(() =>
  files.value.map((f) => ({
    $formkit: "text",
    name: f.name,
    label: `Название карты на снимке ${f.name}`,
    validation: "required",
  }))
);

async function submit(data: FormKitGroupValue) {
  try {
    await Promise.all(
      files.value.map((f) =>
        uploadMap(f.file, (data[f.name] as string) ?? f.name)
      )
    );
    toaster.addToast({
      title: "Информация",
      body: "Карты загружены успешно",
      type: ToastTypes.success,
    });
  } catch (e) {
    toaster.addToast({
      title: "Информация",
      body: "Не удалось загрузить файлы",
      type: ToastTypes.danger,
    });
  }
}
</script>

<style scoped lang="scss"></style>
