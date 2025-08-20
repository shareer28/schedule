import { Table } from "@uwdata/flechette";
import {
  type ColumnDescription,
  coordinator,
  type FieldInfo,
  jsType,
} from "@uwdata/mosaic-core";
import { Query } from "@uwdata/mosaic-sql";

export function isDoubleQuoted(s: string) {
  return s && s[0] === '"' && s[s.length - 1] === '"';
}
export function unquote(s: string) {
  return s && isDoubleQuoted(s) ? s.slice(1, -1) : s;
}

export const isQueryTable = (value: unknown): value is Table =>
  !!value &&
  typeof value === "object" &&
  "getChild" in value &&
  typeof value?.getChild === "function";

export const describeQuery = async (
  table: string,
  query: Query
): Promise<FieldInfo[]> => {
  const _coordinator = coordinator();
  const result: ColumnDescription[] = Array.from(
    await _coordinator.query(Query.describe(query))
  );
  return result.map((desc) => ({
    table,
    column: desc.column_name,
    sqlType: desc.column_type,
    type: jsType(desc.column_type),
    nullable: desc.null === "YES",
  }));
};
