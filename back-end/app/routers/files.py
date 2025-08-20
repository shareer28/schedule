import logging
from typing import Annotated
from app.services.file_service import transform_file
from fastapi import BackgroundTasks, APIRouter, status, UploadFile, Form, File, Query
from app.google.sheets.service import file_exists
from app.models.files import FileExistQuery
from app.google.sheets.service import get_organizations


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/files")

@router.post("/upload", tags=["files"])
def create_upload_file(
    organisation_id: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
    background_tasks: BackgroundTasks
):
    query = get_organizations()
    if not any((organisation_id == organization.id for organization in query.organizations)):
        return {"message": "Organization is not known"}

    if not file:
        return {"message": "No upload file sent"}
    
    transform_file(file, organisation_id, background_tasks)
    return {"filename": file.filename}


@router.get("/exists", status_code=status.HTTP_200_OK, tags=["files"])
def check_file_exists(
    filename: str = Query(..., description="Name of the file to check"),
    organisation_id: str = Query(..., description="Organization ID to check for")
) -> FileExistQuery:
    if not filename or not organisation_id: 
        return { "message": "organisation_id or filename is not filled in"}
    exists = file_exists(filename, organisation_id)
    return FileExistQuery(exists=exists)