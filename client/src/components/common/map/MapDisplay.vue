<template>
  <div id="map"></div>
</template>

<script setup lang="ts">
import {
  getXMLinfo,
  getAnomalies,
  initMap,
  addTileLayerMap,
  addAnomalies,
} from "@/components/common/map/api";
import { onMounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import iconRetinaUrl from "leaflet/dist/images/marker-icon-2x.png";
import iconUrl from "leaflet/dist/images/marker-icon.png";
import shadowUrl from "leaflet/dist/images/marker-shadow.png";

let mapAndControl: { map: L.Map; controlLayer: L.Control.Layers } | null = null;
defineExpose({ addMarker, removeMarker, flyToCoordinates });

const props = defineProps<{ id: string }>();
const xmlImageInfoDoc = await getXMLinfo(props.id);
let anomaliesList = await getAnomalies(props.id);

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

  mapAndControl = initMap();
  if (anomaliesList) {
    addAnomalies(mapAndControl.map, mapAndControl.controlLayer, anomaliesList);
  }

  if (xmlImageInfoDoc) {
    addTileLayerMap(
      mapAndControl.map,
      mapAndControl.controlLayer,
      props.id,
      xmlImageInfoDoc
    );
  }

  emit("map-ready");
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
