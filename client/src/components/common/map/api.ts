import axios from "axios";
import { Ref } from "vue";
import L, { LatLngBounds, LatLngExpression, Polygon } from "leaflet";

import { baseURL, map_zoom } from "@/api";
import { MapInfo } from "@/types/maps";
import { ObjectInfo } from "@/types/objects";


export async function getMaps(
  y: number,
  x: number,
  r: number
): Promise<MapInfo[] | void> {
  return (
    await axios.get<MapInfo[]>(baseURL + "/images/near/" + y + "/" + x + "/" + r)
  ).data;
}


export async function getObjects(
  y: number,
  x: number,
  r: number
): Promise<ObjectInfo[]> {
  return (
    await axios.get<ObjectInfo[]>(baseURL + "/objects/near/" + y + "/" + x + "/" + r)
  ).data;
}

export function initMap(y: number, x: number) {
  //  OpenStreetMap.
  const osmLayer: L.Layer = L.tileLayer("https://{s}.tile.osm.org/{z}/{x}/{y}.png", {
    attribution:
      "&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors",
  });

  // Map.
  const map: L.Map = L.map("map", {
    center: [y, x],
    zoom: 10,
    minZoom: map_zoom[0],
    maxZoom: map_zoom[1],
    layers: [osmLayer],
  });

  const basemaps = { OpenStreetMap: osmLayer };

  // Add base layers
  const controlLayer: L.Control.Layers = L.control.layers(basemaps, undefined, {
    collapsed: false,
  });
  controlLayer.addTo(map);

  return { map: map, controlLayer: controlLayer, osmLayer: osmLayer};
}


export function addMaps(
  mapAndControl: { map: L.Map; controlLayer: L.Control.Layers, osmLayer: L.Layer },
  imagesList: MapInfo[]
) {
  for (let i = 0; i < imagesList.length; i++) {
    // Overlay layers (TMS).
    const lyr: L.Layer = L.tileLayer(
      baseURL + "/tiles/tile/" + imagesList[i].id + "/{z}/{x}/{y}",
      { tms: true, opacity: 1, attribution: "" }
    );

    // Add layer to map.
    mapAndControl.controlLayer.addOverlay(lyr, "Image");
    mapAndControl.map.addLayer(lyr);
  }
}


export function addObjects(
  mapAndControl: { map: L.Map; controlLayer: L.Control.Layers, osmLayer: L.Layer },
  objectsList: ObjectInfo[]
) {
  for (let i = 0; i < objectsList.length; i++) {
    // Object Polygon Layer.
    const objectPolygon: Polygon = L.polygon(
      objectsList[i].coordinates as LatLngExpression[],
      { color: objectsList[i].color, fillOpacity: 0.4 }
    );
    const objectPolygonLayer: L.LayerGroup = L.layerGroup([objectPolygon]);

    // Add layer to map.
    mapAndControl.controlLayer.addOverlay(
      objectPolygonLayer,
      "<span style='color: " +
        objectsList[i].color +
        "'> " +
        objectsList[i].name +
        " </span>"
    );
    mapAndControl.map.addLayer(objectPolygonLayer);
  }
}


export async function updateViewMapsAnsObjects(
  mapAndControl: { map: L.Map; controlLayer: L.Control.Layers, osmLayer: L.Layer },
  imagesList: MapInfo[] | void,
  objectsList: Ref<ObjectInfo[]>,
  oldPos: {center: L.LatLng, zoom: number, layersDeleted: boolean},
  emit: any
) {
  let newCenterCoords = mapAndControl.map.getBounds().getCenter();
  let newZoom = mapAndControl.map.getZoom();

  if (oldPos.layersDeleted || (oldPos.zoom > newZoom) ||
      ((oldPos.center.distanceTo(newCenterCoords) >= getMapSide(mapAndControl.map)) ||
      (oldPos.center.distanceTo(newCenterCoords) >= getMapSide(mapAndControl.map)))) {
        
    oldPos.center = newCenterCoords;
    oldPos.zoom = newZoom;
    
    // Очищаем старые карты и объекты.
    oldPos.layersDeleted = true;
    mapAndControl.map.eachLayer(function (layer) {
      if (layer !== mapAndControl.osmLayer) {
        mapAndControl.map.removeLayer(layer);
        mapAndControl.controlLayer.removeLayer(layer);
      }
    });
    // Запрашиваем новые объекты и карты в пределах видимости.
    imagesList = await getMaps(
      mapAndControl.map.getBounds().getCenter()["lat"],
      mapAndControl.map.getBounds().getCenter()["lng"], 
      getMapSide(mapAndControl.map)
    );
    objectsList.value = await getObjects(
      mapAndControl.map.getBounds().getCenter()["lat"],
      mapAndControl.map.getBounds().getCenter()["lng"], 
      getMapSide(mapAndControl.map)
    );
    emit("objects-updated");
    // Добавляем объекты и карты в пределах видимости.
    if (objectsList) {
      addObjects(mapAndControl, objectsList.value);
      oldPos.layersDeleted = false;
    }
    if (imagesList) {
      addMaps(mapAndControl, imagesList);
      oldPos.layersDeleted = false;
    }
  }
}


export function getMapSide(map: L.Map) {
  let center = map.getBounds().getCenter();
  let centerEast = L.latLng(center["lat"], map.getBounds().getEast());
  let meters = center.distanceTo(centerEast);
  return meters > 12000 ? meters : 12000;
}
