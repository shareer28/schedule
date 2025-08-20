from fastapi import APIRouter
from app.routers.files import router as files_router
from app.routers.organizations import organization_router
from app.routers.specialisms import specialism_router
api_router = APIRouter()

api_router.include_router(files_router)
api_router.include_router(organization_router)
api_router.include_router(specialism_router)