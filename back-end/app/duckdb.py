from fastapi import UploadFile
from duckdb import DuckDBPyConnection
import pandas as pd
import fastexcel 
def read_file(file : UploadFile, conn : DuckDBPyConnection):
    table_name, file_extension = file.filename.split('.') if "." in file.filename else (None, None)
    match file_extension:
        case "csv":
            conn.read_csv(file.file, ignore_errors=True).create(table_name)
        case "xlsx":
            excel_file = fastexcel.read_excel(file.file.read())
            sheet = excel_file.load_sheet(excel_file.sheet_names[0])
            conn.from_arrow(sheet.to_arrow()).create(table_name)
    return table_name


        
