import { Ref } from "vue";
import L, { LatLngExpression } from "leaflet";
import "leaflet/dist/leaflet.css";
import "@/components/common/map/customIcon.css";
import "@geoman-io/leaflet-geoman-free";
import "@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css";

import { baseURL, api, map_zoom } from "@/api";
import { MapInfo } from "@/types/maps";
import { ObjectInfo } from "@/types/objects";
import { objectTypesColors } from "@/api";
import { ToastTypes } from "@/config/toast";

export async function getMaps(
  y: number,
  x: number,
  r: number
): Promise<MapInfo[] | void> {
  return (await api.get<MapInfo[]>("/images/near/" + y + "/" + x + "/" + r))
    .data;
}

export async function getObjects(
  y: number,
  x: number,
  r: number
): Promise<ObjectInfo[]> {
  return (await api.get<ObjectInfo[]>("/objects/near/" + y + "/" + x + "/" + r))
    .data;
}

export function initMap(y: number, x: number) {
  //  OpenStreetMap.
  const osmLayer: L.Layer = L.tileLayer(
    "https://{s}.tile.osm.org/{z}/{x}/{y}.png",
    {
      attribution:
        "&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors",
    }
  );

  // Создание объекта карты.
  const map: L.Map = L.map("map", {
    center: [y, x],
    zoom: 10,
    minZoom: map_zoom[0],
    maxZoom: map_zoom[1],
    layers: [osmLayer],
  });

  const basemaps = { OpenStreetMap: osmLayer };

  // Добавление базовых слоев.
  const controlLayer: L.Control.Layers = L.control.layers(basemaps, undefined, {
    collapsed: false,
  });
  controlLayer.addTo(map);

  return { map: map, controlLayer: controlLayer, osmLayer: osmLayer };
}

export async function initDrawTools(
  map: L.Map,
  controlLayer: L.Control.Layers,
  osmLayer: L.Layer,
  imagesList: Ref<MapInfo[]>,
  objectsList: Ref<ObjectInfo[]>,
  drawLayersList: {
    edited: L.Layer[];
    created: L.Layer[];
    deleted: L.Layer[];
  },
  chosenObjType: Ref<string>,
  chosenObjName: Ref<string>,
  userId: string,
  toaster: any,
  updateViewMapsAnsObjects: () => Promise<void>
) {
  // Задаем язык клавиш.
  map.pm.setLang("ru");

  // Задаем используемые функции.
  map.pm.addControls({
    position: "topleft",
    drawMarker: false,
    drawCircleMarker: false,
    drawPolyline: false,
    drawRectangle: false,
    drawCircle: false,
    drawText: false,
    cutPolygon: false,
  });

  // Создаем свои собственные функции.
  map.pm.Toolbar.createCustomControl({
    name: "endEditing",
    block: "custom",
    className: "bi bi-check icon-geoman",
    title: "Закончить редактирование объектов",
    onClick: () => {
      // Посылаем изменения на запись в бд.
      sendObjects(drawLayersList, toaster, updateViewMapsAnsObjects);

      // Убираем изменения.
      drawLayersList.created = [];
      drawLayersList.edited = [];
      drawLayersList.deleted = [];

      // Убираем объекты, ждем ответа сервера.
      removeObjectsMaps(map, controlLayer, osmLayer);
    },
    toggle: false,
  });

  map.pm.Toolbar.createCustomControl({
    name: "closeEditing",
    block: "custom",
    className: "bi bi-x icon-geoman",
    title: "Поностью отменить редактирование объектов",
    onClick: () => {
      // Убираем изменения.
      drawLayersList.created = [];
      drawLayersList.edited = [];
      drawLayersList.deleted = [];

      // Призываем перезагрузку объектов.
      removeObjectsMaps(map, controlLayer, osmLayer);
      addObjects(map, controlLayer, objectsList.value, drawLayersList, userId);
      addMaps(map, controlLayer, imagesList.value);
    },
    toggle: false,
  });

  // Добавляем слушателей событий с созданием, удалением и поворотом объектов.
  map.on("pm:create", ({ shape, layer }) => {
    // Сохраняем тип, имя и цвет объекта в метаданных.
    (layer as any).type = chosenObjType.value;
    (layer as any).name = chosenObjName.value;
    (layer as any).color = objectTypesColors.get(chosenObjType.value);
    (layer as any).updateUserId = userId;
    (layer as any).updateDatetime = new Date().toISOString();

    (layer as any).setStyle({ color: (layer as any).color, fillOpacity: 0.4 });

    // Добавляем слушателей на изменение слоя.
    addLayerListeners(layer, drawLayersList);

    // Добавляем в массив созданных пользователем слоев.
    let inCreated = drawLayersList.created.findIndex((oldLayer) =>
      checkLId(oldLayer, layer)
    );

    if (inCreated !== -1) {
      drawLayersList.created[inCreated] = layer;
    } else {
      drawLayersList.created.push(layer);
    }
    controlLayer.addOverlay(
      layer,
      "<span style='color: " +
        (layer as any).color +
        "'> " +
        (layer as any).name +
        " </span>"
    );
  });

  map.on("pm:remove", ({ shape, layer }) => {
    // Добавляем в массив удаленных пользователем слоев (если он из тех, что уже были в бд).
    let inCreated = drawLayersList.created.findIndex((oldLayer) =>
      checkLId(oldLayer, layer)
    );
    let inEdited = drawLayersList.edited.findIndex((oldLayer) =>
      checkLId(oldLayer, layer)
    );

    if (inCreated !== -1) {
      drawLayersList.created.splice(inCreated, 1);
    } else if (inEdited !== -1) {
      drawLayersList.edited.splice(inEdited, 1);
    } else {
      drawLayersList.deleted.push(layer);
    }

    controlLayer.removeLayer(layer);
  });

  map.on("pm:rotateend", ({ layer }) => {
    // Добавляем поворот полигона в список созданных или изменных в зависимости
    // от того, сами мы создали полигон или нет.
    let inCreated = drawLayersList.created.findIndex((oldLayer) =>
      checkLId(oldLayer, layer)
    );
    let inEdited = drawLayersList.edited.findIndex((oldLayer) =>
      checkLId(oldLayer, layer)
    );

    if (inCreated !== -1) {
      drawLayersList.created[inCreated] = layer;
    } else if (inEdited !== -1) {
      drawLayersList.edited[inEdited] = layer;
    } else {
      drawLayersList.edited.push(layer);
    }
  });
}

function addLayerListeners(
  layer: L.Layer,
  drawLayersList: {
    edited: L.Layer[];
    created: L.Layer[];
    deleted: L.Layer[];
  }
) {
  layer.on("pm:update", ({ shape, layer }) => {
    // Добавляем изменение полигона в список созданных или изменных в зависимости
    // от того, сами мы создали полигон или нет.
    let inCreated = drawLayersList.created.findIndex((oldLayer) =>
      checkLId(oldLayer, layer)
    );
    let inEdited = drawLayersList.edited.findIndex((oldLayer) =>
      checkLId(oldLayer, layer)
    );

    if (inCreated !== -1) {
      drawLayersList.created[inCreated] = layer;
    } else if (inEdited !== -1) {
      drawLayersList.edited[inEdited] = layer;
    } else {
      drawLayersList.edited.push(layer);
    }
  });

  layer.on("pm:dragend", ({ shape, layer }) => {
    // Добавляем изменение полигона в список созданных или изменных в зависимости
    // от того, сами мы создали полигон или нет.
    let inCreated = drawLayersList.created.findIndex((oldLayer) =>
      checkLId(oldLayer, layer)
    );
    let inEdited = drawLayersList.edited.findIndex((oldLayer) =>
      checkLId(oldLayer, layer)
    );

    if (inCreated !== -1) {
      drawLayersList.created[inCreated] = layer;
    } else if (inEdited !== -1) {
      drawLayersList.edited[inEdited] = layer;
    } else {
      drawLayersList.edited.push(layer);
    }
  });
}

export function addMaps(
  map: L.Map,
  controlLayer: L.Control.Layers,
  imagesList: MapInfo[]
) {
  for (let i = 0; i < imagesList.length; i++) {
    // Слой наложения (TMS).
    const lyr: L.Layer = L.tileLayer(
      baseURL + "/tiles/tile/" + imagesList[i].id + "/{z}/{x}/{y}",
      { tms: true, opacity: 1, attribution: "" }
    );

    // Добавляем слой на карту.
    controlLayer.addOverlay(lyr, "Image");
    map.addLayer(lyr);
  }
}

export function addObjects(
  map: L.Map,
  controlLayer: L.Control.Layers,
  objectsList: ObjectInfo[],
  drawLayersList: {
    edited: L.Layer[];
    created: L.Layer[];
    deleted: L.Layer[];
  },
  userId: string
) {
  // Добавляем объекты, присланные сервером.
  for (let i = 0; i < objectsList.length; i++) {
    // Проверяем, изменял ли уже этот слой пользователь или нет.
    // Если изменял, то добавляем измененный, если он его удалил, то не добавляем вообще.
    let inEdited = drawLayersList.edited.findIndex(
      (edLayer: any) => edLayer.id && edLayer.id === objectsList[i].id
    );
    let inDeleted = drawLayersList.deleted.findIndex(
      (delLayer: any) => delLayer.id && delLayer.id === objectsList[i].id
    );
    if (inDeleted === -1) {
      let objectPolygon: L.Layer = L.polygon(
        objectsList[i].coordinates as LatLngExpression[],
        { color: objectsList[i].color, fillOpacity: 0.4 }
      );

      if (inEdited !== -1) {
        objectPolygon = drawLayersList.edited[inEdited];
      }

      // Добавляем метаданные для перезаписи в случае изменения пользователем.
      (objectPolygon as any).id = objectsList[i].id;
      (objectPolygon as any).type = objectsList[i].type;
      (objectPolygon as any).name = objectsList[i].name;
      (objectPolygon as any).color = objectsList[i].color;
      (objectPolygon as any).updateUserId = userId;
      (objectPolygon as any).updateDatetime = new Date().toISOString();

      // Добавляем слушателей на изменение полигона на него.
      addLayerListeners(objectPolygon, drawLayersList);

      // Добавляем слой на карту.
      controlLayer.addOverlay(
        objectPolygon,
        "<span style='color: " +
          objectsList[i].color +
          "'> " +
          objectsList[i].name +
          " </span>"
      );
      map.addLayer(objectPolygon);
    }
  }

  // Добавляем объекты, созданные пользователем, если они в области видимости карты:
  drawLayersList.created.forEach((layer: any) => {
    if (map.getBounds().contains(layer.getBounds().getCenter())) {
      controlLayer.addOverlay(layer, layer.name);
      map.addLayer(layer);
    }
  });
}

function removeObjectsMaps(
  map: L.Map,
  controlLayer: L.Control.Layers,
  osmLayer: L.Layer
) {
  map.eachLayer(function (layer) {
    if (layer !== osmLayer) {
      map.removeLayer(layer);
      controlLayer.removeLayer(layer);
    }
  });
}

export function prepareUpdateViewMapsAnsObjects(
  map: L.Map,
  controlLayer: L.Control.Layers,
  osmLayer: L.Layer,
  imagesList: Ref<MapInfo[]>,
  objectsList: Ref<ObjectInfo[]>,
  drawLayersList: {
    edited: L.Layer[];
    created: L.Layer[];
    deleted: L.Layer[];
  },
  userId: string,
  oldPos: { center: L.LatLng; zoom: number; layersDeleted: boolean },
  emit: any
) {
  let updateViewMapsAnsObjects =
    (
      map: L.Map,
      controlLayer: L.Control.Layers,
      osmLayer: L.Layer,
      imagesList: Ref<MapInfo[]>,
      objectsList: Ref<ObjectInfo[]>,
      drawLayersList: {
        edited: L.Layer[];
        created: L.Layer[];
        deleted: L.Layer[];
      },
      userId: string,
      oldPos: { center: L.LatLng; zoom: number; layersDeleted: boolean },
      emit: any
    ) =>
    async () => {
      let newCenterCoords = map.getBounds().getCenter();
      let newZoom = map.getZoom();

      oldPos.center = newCenterCoords;
      oldPos.zoom = newZoom;

      // Очищаем старые карты и объекты.
      removeObjectsMaps(map, controlLayer, osmLayer);
      // Запрашиваем новые объекты и карты в пределах видимости.
      imagesList.value = (await getMaps(
        map.getBounds().getCenter()["lat"],
        map.getBounds().getCenter()["lng"],
        getMapSide(map)
      )) as MapInfo[];
      objectsList.value = await getObjects(
        map.getBounds().getCenter()["lat"],
        map.getBounds().getCenter()["lng"],
        getMapSide(map)
      );
      emit("objects-updated");
      // Добавляем объекты и карты в пределах видимости.
      if (objectsList) {
        addObjects(
          map,
          controlLayer,
          objectsList.value,
          drawLayersList,
          userId
        );
      }
      if (imagesList) {
        addMaps(map, controlLayer, imagesList.value);
      }
    };

  return updateViewMapsAnsObjects(
    map,
    controlLayer,
    osmLayer,
    imagesList,
    objectsList,
    drawLayersList,
    userId,
    oldPos,
    emit
  );
}

export function getMapSide(map: L.Map) {
  let center = map.getBounds().getCenter();
  let centerEast = L.latLng(center["lat"], map.getBounds().getEast());
  let meters = center.distanceTo(centerEast);
  return meters > 12000 ? meters : 12000;
}

function checkLId(oneLayer: L.Layer, secondLayer: L.Layer) {
  return (oneLayer as any)._leaflet_id === (secondLayer as any)._leaflet_id;
}

function sendObjects(
  drawLayersList: {
    edited: L.Layer[];
    created: L.Layer[];
    deleted: L.Layer[];
  },
  toaster: any,
  updateViewMapsAnsObjects: () => Promise<void>
) {
  // Сформируем списки ObjectInfo для отправки.
  let edited: ObjectInfo[] = [];
  let created: ObjectInfo[] = [];
  let deleted: ObjectInfo[] = [];

  let listFormation = (objList: ObjectInfo[]) => (layer: any) => {
    let coordinates = [];

    for (let i = 0; i < layer._latlngs[0]; i++) {
      coordinates.push([layer._latlngs[0][i].lat, layer._latlngs[0][i].lng]);
    }

    objList.push({
      id: layer.id,
      type: layer.type,
      name: layer.name,
      color: layer.color,
      updateUserId: layer.updateUserId,
      updateDatetime: layer.updateDatetime,
      center: [
        layer.getBounds().getCenter()["lng"],
        layer.getBounds().getCenter()["lat"],
      ],
      coordinates: coordinates,
    });
  };

  drawLayersList.created.forEach(listFormation(created));
  drawLayersList.edited.forEach(listFormation(edited));
  drawLayersList.deleted.forEach(listFormation(deleted));

  // Отправляем на сервер.
  api
    .post("/objects/update", {
      edited: edited,
      created: created,
      deleted: deleted,
    })
    .then(() => {
      toaster.addToast({
        title: "Информация",
        body: "Изменения сохранены успешно",
        type: ToastTypes.success,
      });
      updateViewMapsAnsObjects();
    })
    .catch(() => {
      toaster.addToast({
        title: "Информация",
        body: "Не удалось сохранить изменения",
        type: ToastTypes.danger,
      });
    });
}
