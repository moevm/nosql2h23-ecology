export interface MapInfo {
  id: string;
  name: string;
  update: string;
  location: [number, number];
  tile_map_resourse: string;
  size: number;
  location: {type: string, coordinates: number[][]};
  ready: boolean;
  sliced: boolean;
}
