import { SelectQuery, WithClauseNode } from '@uwdata/mosaic-sql';
import { v4 as uuidv4 } from 'uuid';

export const getId = () => uuidv4();

export const hasTableData = (
  data: object
): data is {
  tableName: string;
  selectQuery: SelectQuery;
  cteQueries: WithClauseNode[];
} =>
  data && 'tableName' in data && 'selectQuery' in data && 'cteQueries' in data;
