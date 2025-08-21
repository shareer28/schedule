import { SelectQuery, WithClauseNode } from "@uwdata/mosaic-sql";

export const getNodeQuery = (
  selectQuery: SelectQuery,
  cteQueries: WithClauseNode[]
): SelectQuery => selectQuery.clone().with(cteQueries);
