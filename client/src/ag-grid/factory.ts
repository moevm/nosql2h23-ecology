import { ColDef, ColumnApi, GridOptions, GridReadyEvent } from "ag-grid-community";
import { agGridLocalization } from "@/ag-grid/localization";
import { Action } from "@/types/ag-grid/actions";
import ActionsRenderer from "@/components/renderers/ActionsRenderer.vue";


export function getDefaultColDef(): ColDef {
  return {
    sortable: true,
    editable: false,
    resizable: true,
  };
}

export function getColDefFilterText(): ColDef {
  return {
    filter: 'agTextColumnFilter',
    filterParams: {
      filterOptions: ['contains', 'notContains'],
      debounce: 1000,
      maxNumConditions: 1
    }
  };
}

export function getColDefFilterId(): ColDef {
  return {
    filter: 'agTextColumnFilter',
    filterParams: {
      filterOptions: ['equal'],
      debounce: 1000,
      maxNumConditions: 1
    }
  };
}

export function getColDefFilterDate(): ColDef {
  return {
    filter: 'agDateColumnFilter',
    filterParams: {
      filterOptions: ['equal', 'lessThan', 'greaterThan'],
      debounce: 1000,
      maxNumConditions: 1
    }
  };
}

export function getDefaultGridOptions(): GridOptions {
  return {
    defaultColDef: getDefaultColDef(),
    localeText: agGridLocalization,
    suppressMenuHide: true,
    enableCellTextSelection: true,
    suppressDragLeaveHidesColumns: true
  };
}

export function getGridOptionsForSSDM(): GridOptions {
  return {
    ...getDefaultGridOptions(),
    domLayout: "autoHeight",
    animateRows: true,
    rowModelType: 'infinite',
    cacheBlockSize: defaultPageSize,
    pagination: true,
    paginationPageSize: defaultPageSize,
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
    resizable: true,
    pinned: "right",
    suppressMovable: true,
  };
}

export let defaultPageSize = 10;

export function fitActionsColumn({ columnApi }: { columnApi: ColumnApi }) {
  columnApi.autoSizeColumn("actions", false);
}
