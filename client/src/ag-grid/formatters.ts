import { ValueFormatterParams } from "ag-grid-community";
import moment from "moment";

export const dateFormatter = <T>(params: ValueFormatterParams<T>) =>
  moment(params.value).format("DD.MM.YYYY HH:mm:ss");
