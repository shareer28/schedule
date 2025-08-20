import { describeQuery } from "@/utils/duckdb";
import { useMutation, type MutationFunction } from "@tanstack/react-query";
import { type FieldInfo } from "@uwdata/mosaic-core";
import { Query } from "@uwdata/mosaic-sql";

interface IDescribeQuery {
  tableName: string;
  query: Query;
}
export const useDescribeQuery = () => {
  const mutationFn: MutationFunction<FieldInfo[], IDescribeQuery> = async (
    payload: IDescribeQuery
  ) => {
    return await describeQuery(payload.tableName, payload.query);
  };
  return useMutation({ mutationFn });
};
