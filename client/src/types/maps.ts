export interface MapInfo {
  id: string;
  name: string;
  date: string;
  size: number;
  location: {type: string, coordinates: number[][]};
  ready: boolean;
  sliced: boolean;
}
