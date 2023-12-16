<template>
  <div id="map"></div>
  <div v-if="userStore.isAuthed" class="container col-4 col-md-4">
    <div class="card m-auto mt-2">
      <div class="card-body m-auto">
        <h2 class="text-center">Создаваемый объект: </h2>
        <FormKit
          v-model="chosenObjType"
          type="select"
          label="Тип"
          placeholder="Backbone.js"
          :options="objectTypes"
        />
        <FormKit v-model="chosenObjName" type="text" label="Имя" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { onMounted, onBeforeUnmount } from "vue";
import L from "leaflet";
import iconRetinaUrl from "leaflet/dist/images/marker-icon-2x.png";
import iconUrl from "leaflet/dist/images/marker-icon.png";
import shadowUrl from "leaflet/dist/images/marker-shadow.png";

import {
  initMap,
  initDrawTools,
  getMapSide,
  prepareUpdateViewMapsAnsObjects,
} from "@/components/common/map/api";
import { ObjectInfo } from "@/types/objects";
import { MapInfo } from "@/types/maps";
import { objectTypesColors } from "@/api";
import { useUserStore } from "@/store/user";
import { useToaster } from "@/store/toaster";


// Загружаем тостер, для отображения сообщений пользователю.
const toaster = useToaster();

// Данные текущего пользователя.
const userStore = useUserStore();
const userId = userStore.user ? userStore.user._id.$oid : "undefined";

// Для выбора имени и типа объекта.
const objectTypes = Array.from(objectTypesColors.keys());
const chosenObjType = ref<string>("Лес");
const chosenObjName = ref<string>("Лес");

// Для карты.
let map: L.Map;
let controlLayer: L.Control.Layers;
let osmLayer: L.Layer;

const props = defineProps<{ y?: number; x?: number }>();
let x = 30.308611;
let y = 59.9375;
if (props.x && props.y) {
  x = props.x;
  y = props.y;
}

let imagesList = ref<MapInfo[]>([]);
let objectsList = ref<ObjectInfo[]>([]);
let drawLayersList = {
    edited: [] as L.Layer[],
    created: [] as L.Layer[],
    deleted: [] as L.Layer[]
  }

let timer: number;
let oldPos = {
  center: [0.0, 0.0] as unknown as L.LatLng, 
  zoom: 10, 
  layersDeleted: true
};

const emit = defineEmits<{ (e: "map-ready"): void, (e: "objects-updated"): void }>();

onMounted(() => {
  // Загружаем картинки и параметры маркера в leaflet
  L.Marker.prototype.options.icon = L.icon({
    iconRetinaUrl: iconRetinaUrl,
    iconUrl: iconUrl,
    shadowUrl: shadowUrl,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    tooltipAnchor: [16, -28],
    shadowSize: [41, 41],
  });

  // Создаем карту.
  ({map, controlLayer, osmLayer} = initMap(y, x));

  // Создаем функцию обновления карты.
  oldPos.center = map.getBounds().getCenter();
  oldPos.zoom = map.getZoom();
  let updateViewMapsAnsObjects = prepareUpdateViewMapsAnsObjects(
    map, controlLayer, osmLayer, 
    imagesList, objectsList, drawLayersList,
    userId, oldPos, emit
  );

  // Создаем возможность для редактирования, если пользователь вошел в систему.
  if (userStore.isAuthed) {
    initDrawTools(
      map, controlLayer, osmLayer, imagesList, objectsList, drawLayersList,
      chosenObjType, chosenObjName, userId, toaster, updateViewMapsAnsObjects
    );
  }
  
  updateViewMapsAnsObjects();

  // Задаем интервал на обновление отображаемых объектов.
  timer = setInterval(() => {
    let newCenterCoords = map.getBounds().getCenter();
    let newZoom = map.getZoom();

    if (!map.pm.globalDrawModeEnabled() &&
        !map.pm.globalEditModeEnabled() &&
        !map.pm.globalRotateModeEnabled() &&
        ((oldPos.zoom > newZoom) ||
        ((oldPos.center.distanceTo(newCenterCoords) >= getMapSide(map)) ||
        (oldPos.center.distanceTo(newCenterCoords) >= getMapSide(map))))) {
      updateViewMapsAnsObjects();
    }
  }, 1000);


  // Испускаем сигнал о готовкности карты.
  emit("map-ready");
});

onBeforeUnmount(() => {
  clearInterval(timer);
});

// Создаем насколько функций для использования родительскими элементами для управления картой.
defineExpose({ addMarker, removeMarker, flyToCoordinates, getObjects });
function addMarker(markerPosition: [number, number]) {
  let marker = new L.Marker(markerPosition);
  if (map) return marker.addTo(map);
}

function removeMarker(marker: L.Marker) {
  if (map) map.removeLayer(marker);
}

function flyToCoordinates(coordinates: [number, number]) {
  if (map) {
    map.setZoom(14);
    map.panTo(coordinates);
  }
}

function getObjects() {
  return objectsList.value;
}
</script>

<style scoped lang="scss">
#map {
  width: 90%;
  height: 600px;
  overflow: hidden;
}
</style>
