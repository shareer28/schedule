import { type ITableStore } from "@/types/store";
import { create } from "zustand";
import { combine } from "zustand/middleware";
export const useTableStore = create<ITableStore>(
  combine(
    {
      tableName: undefined,
    } as ITableStore,
    (set, get) => ({
      setTableName: (tableName: string) => {
        set(() => ({
          tableName,
        }));
      },
    })
  )
);
