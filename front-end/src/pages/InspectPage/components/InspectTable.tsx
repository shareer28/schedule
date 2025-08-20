import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";
import { Table as DuckTable } from "@uwdata/flechette";
import {
  type ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { useMemo } from "react";
import type { Row } from "@/types/mosaic";

const InspectTable = ({
  queryResult,
}: {
  queryResult: DuckTable | undefined;
}) => {
  const data = useMemo<Row[]>(() => {
    if (!queryResult) return [];

    return queryResult.toArray();
  }, [queryResult]);

  const columns = useMemo<ColumnDef<Row>[]>(() => {
    if (!queryResult) return [];

    return queryResult.schema.fields.map((v) => ({
      accessorKey: v.name,
      cell: (info) => {
        const value = info.getValue();
        if (value instanceof Date) {
          return (value as Date).toLocaleString();
        }
        return value;
      },
    }));
  }, [queryResult]);

  const table = useReactTable<Row>({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    // TODO: try with cursor to fix the styling
    <Table wrapperClassName="flex h-10 grow overflow-y-scroll" className="">
      <TableHeader className="sticky top-0 bg-secondary">
        {table.getHeaderGroups().map((headerGroup) => (
          <TableRow key={headerGroup.id}>
            {headerGroup.headers.map((header) => {
              return (
                <TableHead key={header.id}>
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </TableHead>
              );
            })}
          </TableRow>
        ))}
      </TableHeader>
      <TableBody>
        {table.getRowModel().rows?.length ? (
          table.getRowModel().rows.map((row) => (
            <TableRow
              key={row.id}
              data-state={row.getIsSelected() && "selected"}
            >
              {row.getVisibleCells().map((cell) => (
                <TableCell key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </TableCell>
              ))}
            </TableRow>
          ))
        ) : (
          <TableRow>
            <TableCell colSpan={columns.length} className="h-24 text-center">
              No results.
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  );
};
export default InspectTable;
