from fastapi import APIRouter
from api_v1.login_router import login_router  # import the APIRouter instance, not module

api_router = APIRouter()

# Include all routers here
api_router.include_router(login_router, prefix="/login", tags=["Login"])
