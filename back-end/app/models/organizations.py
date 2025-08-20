
from pydantic import BaseModel
from typing import List
class Organization(BaseModel): 
    id: str
    name: str

class Organizations(BaseModel):
    organizations: List[Organization]
