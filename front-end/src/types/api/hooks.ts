export interface ITableRequest {
  prompt: string;
  table_name: string;
  fields: {
    column: string;
    nullable: boolean;
    sql_type: string;
  }[];
}

export interface IAgentOutput {
  chain_of_thought: string;
  query: string;
}

export interface IUploadFile {
  file: File;
  organizationId: string;
}

export interface Organization {
  id: string;
  name: string;
}

export interface IFileExistRequest {
  filename: string;
  organizationId: string;
}
