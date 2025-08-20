import { useQuery } from "@tanstack/react-query";
import { api } from "../client";
import type { IFileExistRequest } from "@/types/api/hooks";

export const useFileExistsQuery = (request: IFileExistRequest) => {
  const queryFn = () =>
    api
      .get<{ exists: boolean }>("files/exists", {
        params: {
          filename: request.filename,
          organisation_id: request.organizationId,
        },
        paramsSerializer: (params) => {
          // Sample implementation of query string building
          let result = "";
          Object.keys(params).forEach((key) => {
            result += `${key}=${encodeURIComponent(params[key])}&`;
          });
          return result.substring(0, result.length - 1);
        },
      })
      .then((res) => res.data?.exists ?? false);

  return useQuery<boolean>({
    queryKey: ["fileExists", request.filename, request.organizationId],
    queryFn,
    enabled: !!(request?.filename && request?.organizationId),
  });
};
