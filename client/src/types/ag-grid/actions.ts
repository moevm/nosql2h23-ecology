export interface Action<T = any> {
  tooltip: string;
  icon: string;
  button?: string;
  onClicked?: (action: Action<T>, data: T) => void;
  hide?: boolean | ((data: T) => boolean);
}
