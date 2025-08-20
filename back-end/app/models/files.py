from pydantic import BaseModel

class FileExistQuery(BaseModel):
    exists: bool