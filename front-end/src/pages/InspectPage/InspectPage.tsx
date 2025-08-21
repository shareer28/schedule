import {
  coordinator,
  makeClient,
  MosaicClient,
} from "@uwdata/mosaic-core";
import { useEffect, useState } from "react";
import { Table as DuckTable } from "@uwdata/flechette";
import { Query, row_number } from "@uwdata/mosaic-sql";
import { isQueryTable } from "@/utils/duckdb";
import { useTableStore } from "@/local/tableStore";
import { unquote } from "@/utils/duckdb";
import InspectTable from "./components/InspectTable";
import ChatInput from "./components/ChatInput";
import { useSendMessage } from "@/api/hooks/sendMessage";
import { useDescribeQuery } from "@/api/hooks/describeQuery";


const InspectPage = () => {
  const [queryResult, setQueryResult] = useState<DuckTable>();
  // the passed handler has to be memoized, otherwise the hook will not work correctly
  const [client] = useState<MosaicClient>(
    makeClient({
      coordinator: coordinator(),
      queryResult: (r) => {
        if (!isQueryTable(r)) return;
        setQueryResult(r);
        // setColumns(table.names);
      },
    })
  );
  const { tableName } = useTableStore();
  const { mutate: sendMessage } = useSendMessage();
  const {
    mutate: getQueryDescription,
    data: schema,
  } = useDescribeQuery();

  useEffect(() => {
    if (tableName) {
      const query = Query.from(unquote(tableName))
        .select({ index: row_number() }, "*")
        .limit(100);
      client.requestQuery(query);
      getQueryDescription({ tableName, query });
    }

    return () => {
      console.log("destroyed");
    };
  }, [tableName, getQueryDescription, client]);

  const onSubmit = (prompt: string) => {
    if (!schema || !tableName) return;
    sendMessage({
      prompt,
      table_name: tableName,
      fields: schema.map(({ column, sqlType, nullable }) => ({
        column,
        sql_type: sqlType,
        nullable,
      })),
    });
  };
  return (
    <div className="@container h-full flex flex-col">
      <ChatInput onSubmit={onSubmit} />
      <InspectTable queryResult={queryResult} />
    </div>
  );
};

export default InspectPage;
