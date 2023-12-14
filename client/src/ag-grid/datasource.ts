import { api } from '@/api';
import { IDatasource, IGetRowsParams } from 'ag-grid-community'
import { MapInfo } from "@/types/maps";


export class DataSource implements IDatasource {
    dataFetchURL: string;

    constructor(dataFetchURL: string) {
        this.dataFetchURL = dataFetchURL;
    }

    getRows(params: IGetRowsParams) {
        console.log(JSON.stringify(params));

        let getParams = {
            start: params.startRow,
            end: params.endRow,
            sort: JSON.stringify(params.sortModel),
            filter: JSON.stringify(params.filterModel)
        }

        api.get<{ rowData: MapInfo[], end: number }>(this.dataFetchURL, {
            params: getParams,
        }).then((response) => {
            let data = response.data;
            console.log(data);
            if (data.end === params.endRow) data.end = -1;
            params.successCallback(data.rowData, data.end);
        }).catch(() => {
            params.failCallback();
        });
    }
};