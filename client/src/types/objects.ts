export interface ObjectInfo {
  id: string;
  name: string;
  objectIndex: string;
  area: number;
  uploadDate: string;
  detectDate: string;
}

export interface ObjectData {
  id: string;
  name: string;
  objectIndex: string;
  area: number;
  coordinates: [number, number];
  uploadDate: string;
  detectDate: string;
}

export interface ObjectsMapData {
  name: string;
  color: string;
  polygons: number[][];
}
