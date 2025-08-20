import { useGetOrganizationsQuery } from "@/api/hooks/getOrganizationsQuery";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../../components/ui/select";
import { useMemo } from "react";
import { Skeleton } from "../../../components/ui/skeleton";

export interface OrganizationDropDownProps {
  value: string;
  onChange?: (value: string) => void;
}
export function OrganizationDropDown({
  value,
  onChange,
}: OrganizationDropDownProps) {
  const { data = [], isLoading } = useGetOrganizationsQuery();

  const getOrganizationName = useMemo(
    () => data.find(({ id }) => id === value)?.name,
    [data, value]
  );

  return (
    <Select
      value={value}
      onValueChange={(val) => {
        onChange?.(val);
      }}
    >
      {isLoading ? (
        <Skeleton className="h-10 mb-2 w-1/5" data-size="default" />
      ) : (
        <SelectTrigger>
          <SelectValue placeholder="Select an organization">
            {getOrganizationName}
          </SelectValue>
        </SelectTrigger>
      )}
      <SelectContent align="center">
        {data
          .sort((a, b) => a.name.trim().localeCompare(b.name.trim()))
          .map((option) => (
            <SelectItem key={option.id} value={option.id}>
              {option.name}
            </SelectItem>
          ))}
      </SelectContent>
    </Select>
  );
}
