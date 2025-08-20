import { type Connector } from "@uwdata/mosaic-core";
import { AsyncDuckDB } from "@duckdb/duckdb-wasm";
import { type DataType } from "@uwdata/flechette";

export interface DuckDBWASMConnector extends Connector {
  getDuckDB(): Promise<AsyncDuckDB>;
}

export type Row = {
  [key: string]: DataType;
};
