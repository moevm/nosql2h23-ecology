import { ColDef, ColumnApi, GridOptions } from "ag-grid-community";
import { agGridLocalization } from "@/ag-grid/localization";
import { Action } from "@/types/ag-grid/actions";
import ActionsRenderer from "@/components/renderers/ActionsRenderer.vue";

export function getDefaultColDef(): ColDef {
  return {
    filter: true,
    sortable: true,
    editable: false,
    resizable: true,
  };
}

export function getDefaultGridOptions(): GridOptions {
  return {
    defaultColDef: getDefaultColDef(),
    localeText: agGridLocalization,
    suppressMenuHide: true,
    enableCellTextSelection: true,
    suppressDragLeaveHidesColumns: true,
  };
}

export function getActionsColDef<T>(actions: Action<T>[]): ColDef<T> {
  return {
    colId: "actions",
    headerName: "Действия",
    cellRenderer: ActionsRenderer,
    cellRendererParams: {
      actions,
    },
    sortable: false,
    filter: false,
    resizable: false,
    pinned: "right",
    suppressMovable: true,
  };
}

export function fitActionsColumn({ columnApi }: { columnApi: ColumnApi }) {
  columnApi.autoSizeColumn("actions", true);
}
