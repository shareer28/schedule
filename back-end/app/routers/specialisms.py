from fastapi import APIRouter
from app.models.specialims import Specialisms
from app.google.sheets.service import get_specialisms

specialism_router = APIRouter()

@specialism_router.get("/specialisms", tags=["specialisms"])
def query_organizations() -> Specialisms:
    result = get_specialisms()

    return result
