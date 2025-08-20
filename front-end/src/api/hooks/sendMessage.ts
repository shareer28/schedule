import type { IAgentOutput, ITableRequest } from "@/types/api/hooks";
import { api } from "../client";
import type { MutationFunction } from "@tanstack/react-query";
import { useMutation } from "@tanstack/react-query";

export const useSendMessage = () => {
  const mutation: MutationFunction<IAgentOutput, ITableRequest> = async (
    payload: ITableRequest
  ) => {
    const response = await api.post("api/v1/agents/prompt/aggregate", {
      ...payload,
    });
    return response.data;
  };
  return useMutation({ mutationFn: mutation });
};
