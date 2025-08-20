import { useQuery } from "@tanstack/react-query";
import { api } from "../client";
import type { Organization } from "@/types/api/hooks";

export const useGetOrganizationsQuery = () => {
  const queryFn = () =>
    api
      .get<{ organizations: Organization[] }>("/organizations")
      .then((res) => res.data?.organizations ?? []);
  return useQuery<Organization[]>({
    queryKey: ["organizations"],
    queryFn,
  });
};
