from pydantic import BaseModel
from typing import List

class Specialism(BaseModel):
    name : str
    dutch_translation: str

class Specialisms(BaseModel):
    specialisms: List[Specialism]