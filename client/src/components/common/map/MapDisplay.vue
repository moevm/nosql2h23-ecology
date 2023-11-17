<template>
  <div id="map"></div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import iconRetinaUrl from "leaflet/dist/images/marker-icon-2x.png";
import iconUrl from "leaflet/dist/images/marker-icon.png";
import shadowUrl from "leaflet/dist/images/marker-shadow.png";

import {
  getMaps,
  getObjects,
  initMap,
  addMaps,
  addObjects,
  updateViewMapsAnsObjects,
  getMapSide
} from "@/components/common/map/api";
import { ObjectsMapData } from "@/types/objects";
import { MapInfo } from "@/types/maps";


let mapAndControl: { map: L.Map; controlLayer: L.Control.Layers, osmLayer: L.Layer };
defineExpose({ addMarker, removeMarker, flyToCoordinates });

const props = defineProps<{ y?: number; x?: number }>();
let x = 30.308611;
let y = 59.9375;
if (props.x && props.y) {
  x = props.x;
  y = props.y;
}

let imagesList: MapInfo[];
let objectsList: ObjectsMapData[];

let timer: number;
let oldPos = {
  center: [0.0, 0.0] as unknown as L.LatLng, 
  zoom: 10, 
  layersDeleted: true
};

const emit = defineEmits<{ (e: "map-ready"): void }>();

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

  mapAndControl = initMap(y, x);
  oldPos.center = mapAndControl.map.getBounds().getCenter();
  oldPos.zoom = mapAndControl.map.getZoom();

  // Задаем интервал на обновление отображаемых объектов.
  timer = setInterval(() => {
    updateViewMapsAnsObjects(mapAndControl, imagesList, objectsList, oldPos);
  }, 1000);

  emit("map-ready");

});

onBeforeUnmount(() => {
  clearInterval(timer);
});

// Создаем насколько функций для использования родительскими элементами для управления картой.
function addMarker(markerPosition: [number, number]) {
  let marker = new L.Marker(markerPosition);
  if (mapAndControl) return marker.addTo(mapAndControl.map);
}

function removeMarker(marker: L.Marker) {
  if (mapAndControl) mapAndControl.map.removeLayer(marker);
}

function flyToCoordinates(coordinates: [number, number]) {
  if (mapAndControl) mapAndControl.map.panTo(coordinates);
}
</script>

<style scoped lang="scss">
#map {
  width: 90%;
  height: 600px;
  overflow: hidden;
}
</style>
