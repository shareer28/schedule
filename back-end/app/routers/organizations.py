from fastapi import APIRouter
from app.models.organizations import Organizations
from app.google.sheets.service import get_organizations

organization_router = APIRouter()

@organization_router.get("/organizations", tags=["organizations"])
def query_organizations() -> Organizations:
    result = get_organizations()

    return result
