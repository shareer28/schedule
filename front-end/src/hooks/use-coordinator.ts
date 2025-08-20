import { coordinator as _coordinator } from "@uwdata/mosaic-core";
import { AsyncDuckDB } from "@duckdb/duckdb-wasm";
import { loadCSV } from "@uwdata/mosaic-sql";
import { useMemo, useState } from "react";
import { useTableStore } from "@/local/tableStore";

const useCoordinator = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState<string | undefined>();
  const isError = useMemo(() => !error, [error]);
  const { setTableName } = useTableStore();
  const uploadFile = async (file: File) => {
    try {
      setIsLoading(true);
      setIsSuccess(false);

      const coordinator = _coordinator();

      const connector = coordinator.databaseConnector() as any; // eslint-disable-line

      if (!connector?.getDuckDB) return;

      // Load the file into DuckDB
      const [db, text] = await Promise.all([
        connector.getDuckDB() as Promise<AsyncDuckDB>,
        file.text(),
      ]);
      await db.registerFileText(file.name, text);
      const tableName = `"${file.name.split(".")[0]}"`;
      await coordinator.exec(loadCSV(tableName, file.name, {}));

      setIsLoading(false);
      setIsSuccess(true);
      setTableName(tableName);
    } catch (e) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError(String(e));
      }
    }
  };

  return { isLoading, isSuccess, isError, uploadFile };
};

export { useCoordinator };
