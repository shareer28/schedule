
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import gspread

from pandas import DataFrame
import pickle 
import os
import pandas as pd

from app.models.organizations import Organizations, Organization
from app.models.specialims import Specialism, Specialisms

from logging import getLogger, WARNING
from functools import lru_cache
import time
import functools
from app.core.config import settings

logger = getLogger(__name__)

def ttl_lru_cache(ttl_seconds=60, maxsize=128):
    """LRU cache with time-to-live (TTL) support."""
    def decorator(fn):
        @lru_cache(maxsize=maxsize)
        def cached(*args, **kwargs):
            return fn(*args, **kwargs)
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Check if cache is expired
            if not hasattr(wrapper, "_cache_expiry") or now > wrapper._cache_expiry:
                cached.cache_clear()
                wrapper._cache_expiry = now + ttl_seconds
            return cached(*args, **kwargs)
        wrapper._cache_expiry = 0
        wrapper.cache_clear = cached.cache_clear
        return wrapper
    return decorator

def get_service() -> gspread.Client:
    """Formats specified credentials for Google clients."""

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = None
    # Load existing credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
            creds = flow.run_local_server()
        # Save the credentials
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    assert creds is not None
    client = gspread.Client(creds)
    return client

@ttl_lru_cache(ttl_seconds=60)
def get_organizations() -> Organizations:
    client = get_service()

    # HARDCODED REFERENCE TO THE SHEET WITH THE ORGANIZATION NAMES
    sheet_id = "1tPmUzIE97vw4PKO4OaHE26LC1nbF1nuvAfCE-UOLb30"
    workbook = client.open_by_key(sheet_id)

    sheet_name = "Organizations"
    worksheet = workbook.worksheet(sheet_name)
    
    values = worksheet.get_all_values()
    headers = values.pop(0)
    if not values or not headers:
        return Organizations(organizations=[])

    df = pd.DataFrame(values, columns=headers)    
    df =  (
        df
            .loc[lambda r: r["is_template"] == "0"]
            .loc[lambda r: ~(r["name"].str.upper().str.contains("XX") | r["name"].str.upper().str.contains("ZZ"))]
            .loc[lambda r: ~(r["name"].str.lower().str.contains("test") | r["name"].str.lower().str.contains("demo"))]
    )
    organizations = list(map(lambda r: Organization(id=r["id"], name=r["name"]), df.to_dict(orient="records")))
    
    return Organizations(organizations=organizations)

@ttl_lru_cache(ttl_seconds=60)
def get_specialisms() -> Specialisms:
    client = get_service()

    # HARDCODED REFERENCE TO THE SHEET WITH THE SPECIALISM NAMES
    sheet_id = "1tPmUzIE97vw4PKO4OaHE26LC1nbF1nuvAfCE-UOLb30"
    workbook = client.open_by_key(sheet_id)

    sheet_name = "Specialties"
    worksheet = workbook.worksheet(sheet_name)

    specialisms_raw = worksheet.get_all_values()
    specialisms = [Specialism(name=row[0], dutch_translation=row[-1]) for row in specialisms_raw]
    return Specialisms(specialisms=specialisms)



def file_exists(filename: str, organisation_id: str):
    client = get_service()
    sheet_id = settings.GOOGLE_SHEET
    workbook = client.open_by_key(sheet_id)

    worksheets = workbook.worksheets()
    worksheet_name = "Turnovertime_NL"
    if not any([w.title == worksheet_name for w in worksheets]):
        return False
    worksheet = workbook.worksheet(worksheet_name)

    # Get header row    
    headers = worksheet.row_values(1)
    if "organisation_id" not in headers or "filename" not in headers:
        return False

    org_id_col_index = headers.index("organisation_id") + 1  # 1-based index
    filename_col_index = headers.index("filename") + 1  # 1-based index

    # Find first cell matching organisation_id in org_id_col_index
    org_id_cells = worksheet.col_values(col=org_id_col_index)
    filename_cells = worksheet.col_values(col=filename_col_index)
    if not org_id_cells or not filename_cells:
        return False

    unique_pairs = set([(org_cell, file_cell) for (org_cell, file_cell) in zip(org_id_cells, filename_cells) if org_cell and file_cell and org_cell not in headers and file_cell not in headers ])
    return (organisation_id, filename) in unique_pairs
    # Check if both cells are in the same row
    # for cell in filename_cells:
    #     index = bisect.bisect(org_id_cells, cell.row, key=lambda c: c.row) - 1 # binary search
    #     if index != -1 and org_id_cells[index].row == cell.row:
    #         return True


def remove_rows_by_org_and_filename(sheet_name, organisation_id, filename):
    """
    Remove all rows in the sheet where both organisation_id and filename match.
    Also removes empty rows (rows where all cells are empty).
    """
    client = get_service()
    sheet_id = settings.GOOGLE_SHEET
    workbook = client.open_by_key(sheet_id)

    worksheet_list = map(lambda x: x.title, workbook.worksheets())

    if sheet_name not in worksheet_list:
        logger.log(WARNING, "The sheet does not exists!")
        return
    sheet = workbook.worksheet(sheet_name)
        

    all_values = sheet.get_all_values()
    if not all_values:
        logger.log(WARNING, "The sheet is empty!")
        return

    headers = all_values[0]
    org_id_idx = headers.index("organisation_id") if "organisation_id" in headers else None
    filename_idx = headers.index("filename") if "filename" in headers else None

    if org_id_idx is None or filename_idx is None:
        logger.log(WARNING, "organisation and filenames are not found in the sheets")
        return

    row_to_delete = []
    for i, row in enumerate(all_values, start=1):  # 1-based, skip header
        # Remove if all cells are empty
        if (row[org_id_idx].strip() == "" or (row[org_id_idx] == organisation_id and row[filename_idx] == filename)):
            row_to_delete.append(i)

def append_values(
    sheet_name: str, 
    df : DataFrame
    ):
    """
    sheet_name: the name of the sheet in the workbook you want to add
    df: the necessary dataframe for saving to the sheets
    """
    client = get_service()

    # Add the moment hard coded
    sheet_id = settings.GOOGLE_SHEET
    workbook = client.open_by_key(sheet_id)

    worksheet_list = map(lambda x: x.title, workbook.worksheets())

    if sheet_name in worksheet_list:
        sheet = workbook.worksheet(sheet_name)
    else:
        sheet = workbook.add_worksheet(sheet_name, rows=10, cols=10)

    # sheet.clear()
    column_names = sheet.get_values(f"A1:{chr(int(ord('A')) + len(df.columns))}1")[0]
    if len(column_names) == 0:
        sheet.append_row(df.columns.tolist())

    # Convert all values to string to avoid JSON serialization issues with Timestamp
    str_values = df.astype(str).values.tolist()

    # Upload data in chunks
    total_rows = len(df)
    chunk_size = 10000
    for start in range(0, total_rows, chunk_size):
        end = min(start + chunk_size, total_rows)
        chunk_df = df.iloc[start:end]
        str_values = chunk_df.astype(str).values.tolist()
        sheet.append_rows(
            values=str_values
        )
