export interface MapInfo {
  id: string;
  name: string;
  updateUserId: string;
  updateDatetime: string;
  center: [number, number];
  coordinates: number[][];
  ready: boolean;
  sliced: boolean;
}
