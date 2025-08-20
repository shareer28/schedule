import type { IUploadFile } from "@/types/api/hooks";
import { useMutation, type MutationFunction } from "@tanstack/react-query";
import { api } from "../client";

export const useUploadFile = () => {
  const mutationFn: MutationFunction<void, IUploadFile> = async (
    payload: IUploadFile
  ) => {
    return await api.postForm("files/upload", {
      file: payload.file,
      organisation_id: payload.organizationId,
    });
  };
  return useMutation({ mutationFn });
};
