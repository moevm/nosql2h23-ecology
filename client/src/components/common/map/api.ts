import axios, { AxiosError } from "axios";
import L, { LatLngExpression, Polygon } from "leaflet";

import { baseURL, map_zoom } from "@/api";
import { ObjectsMapData } from "@/types/objects";


export async function getXMLinfo(id: string): Promise<Document | void> {
  return axios
    .get<string>(baseURL + "/images/tile_map_resource/" + id)
    .then((response) => {
      const parser: DOMParser = new DOMParser();
      return parser.parseFromString(response.data, "text/xml");
    })
    .catch((err: AxiosError) => {
      if (!err.response || (err.response && err.response.status !== 404)) {
        throw err;
      }
    });
}

export async function getObjects(
  id: string
): Promise<ObjectsMapData[] | void> {
  return (
    await axios.get<ObjectsMapData[]>(baseURL + "/images/objects/" + id)
  ).data;
}

export function initMap() {
  //  OpenStreetMap.
  const osm: L.Layer = L.tileLayer("https://{s}.tile.osm.org/{z}/{x}/{y}.png", {
    attribution:
      "&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors",
  });

  // Map.
  const map: L.Map = L.map("map", {
    center: [59.9375, 30.308611],
    zoom: 10,
    minZoom: map_zoom[0],
    maxZoom: map_zoom[1],
    layers: [osm],
  });

  const basemaps = { OpenStreetMap: osm };

  // Add base layers
  const controlLayer: L.Control.Layers = L.control.layers(basemaps, undefined, {
    collapsed: false,
  });
  controlLayer.addTo(map);

  return { map: map, controlLayer: controlLayer };
}

export function addTileLayerMap(
  map: L.Map,
  controlLayer: L.Control.Layers,
  id: string,
  xmlImageInfoDoc: Document
) {
  // Overlay layers (TMS).
  const lyr: L.Layer = L.tileLayer(
    baseURL + "/images/tile/" + id + "/{z}/{x}/{y}",
    { tms: true, opacity: 1, attribution: "" }
  );

  // Add layer to map.
  controlLayer.addOverlay(lyr, "Image");

  // Fit to overlay bounds (SW and NE points with (lat, lon))
  map.fitBounds([
    [
      parseFloat(
        xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[1]
          .nodeValue as string
      ), // miny
      parseFloat(
        xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[2]
          .nodeValue as string
      ), // maxx
    ],
    [
      parseFloat(
        xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[3]
          .nodeValue as string
      ), // maxy
      parseFloat(
        xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[0]
          .nodeValue as string
      ), // minx
    ],
  ]);
}

export function addObjects(
  map: L.Map,
  controlLayer: L.Control.Layers,
  objectsList: ObjectsMapData[]
) {
  for (let i = 0; i < objectsList.length; i++) {
    // Object Polygon Layer.
    const objectPolygon: Polygon = L.polygon(
      objectsList[i].polygons as LatLngExpression[][],
      { color: objectsList[i].color, fillOpacity: 0.4 }
    );
    const objectPolygonLayer: L.LayerGroup = L.layerGroup([objectPolygon]);

    // Add layer to map.
    controlLayer.addOverlay(
      objectPolygonLayer,
      "<span style='color: " +
        objectsList[i].color +
        "'> " +
        objectsList[i].name +
        " </span>"
    );

    // Fit to overlay bounds (SW and NE points with (lat, lon))
    map.fitBounds([
      [
        objectsList[i].polygons[0][0][0], // miny
        objectsList[i].polygons[0][0][1], // maxx
      ],
      [
        objectsList[i].polygons[0][0][0], // maxy
        objectsList[i].polygons[0][0][1], // minx
      ],
    ]);
  }
}
