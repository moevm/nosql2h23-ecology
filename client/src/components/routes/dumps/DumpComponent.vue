<template>
  <div class="container mt-3">
    <ul id="myTab" class="nav nav-tabs" role="tablist">
      <li class="nav-item" role="presentation">
        <button
          id="home-tab"
          class="nav-link active"
          data-bs-toggle="tab"
          data-bs-target="#maps"
        >
          Экспорт
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button
          id="profile-tab"
          class="nav-link"
          data-bs-toggle="tab"
          data-bs-target="#import"
        >
          Импорт
        </button>
      </li>
    </ul>
    <div class="tab-content mt-3">
      <div id="maps" class="tab-pane fade show active">
        <div class="m-auto col-10 col-lg-6 text-center">
          <button class="btn btn-primary fs-3" @click="download">
            Загрузить
            <i class="bi bi-file-earmark-arrow-down fw-bold" />
          </button>
        </div>
      </div>
      <div id="import" class="tab-pane fade">
        <div class="m-auto col-10 col-lg-6">
          <FormKit type="form" :actions="false" @submit="upload">
            <FormKit
              name="files"
              type="file"
              accept=".json"
              multiple="false"
              label="Дамп"
              validation="required"
              validation-visibility="live"
            />
            <FormKit
              outer-class="text-end"
              input-class="$reset btn btn-success"
              type="submit"
              label="Загрузить"
            />
          </FormKit>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FormKitGroupValue } from "@formkit/core";
import { useToaster } from "@/store/toaster";
import { ToastTypes } from "@/config/toast";
import { ref } from "vue";
import { saveAs } from "file-saver";
import { DumpsApi } from "@/components/routes/dumps/api";

const toaster = useToaster();

const files = ref<{ name: string; file: File }[]>([]);

async function download() {
  const data = (await DumpsApi.downloadDump()).data;
  const blob = new Blob([JSON.stringify(data)], {
    type: "text/plain;charset=utf-8",
  });
  saveAs(blob, "dump.json");
}

async function upload(data: FormKitGroupValue) {
  try {
    await DumpsApi.uploadDump((data.files as { file: File }[])[0].file);

    toaster.addToast({
      title: "Информация",
      body: "Дамп загружен успешно",
      type: ToastTypes.success,
    });
  } catch (e) {
    toaster.addToast({
      title: "Информация",
      body: "Не удалось загрузить Дамп",
      type: ToastTypes.danger,
    });
  }
}
</script>

<style scoped lang="scss"></style>
