# api_v1/routers/sidebar_router.py
from fastapi import APIRouter, Depends
from schemas.sidebar_schema import SidebarCreateRequest, SidebarUpdateRequest, SidebarResponse
from controller.sidebar_controller import SidebarController
from typing import List

sidebar_router = APIRouter()

# Create Sidebar
@sidebar_router.post("/", response_model=SidebarResponse)
def create_sidebar(request: SidebarCreateRequest):
    return SidebarController.create_sidebar(
        title=request.title,
        path=request.path,
        icon=request.icon,
        parent_id=request.parent_id,
        role_ids=request.role_ids
    )

# List sidebars (optional: filtered by user roles)
@sidebar_router.get("/", response_model=List[SidebarResponse])
def list_sidebars(user_roles: List[int] = None):
    return SidebarController.get_sidebar(user_roles=user_roles)

# Update Sidebar
@sidebar_router.put("/{sidebar_id}", response_model=SidebarResponse)
def update_sidebar(sidebar_id: int, request: SidebarUpdateRequest):
    return SidebarController.update_sidebar(
        sidebar_id=sidebar_id,
        title=request.title,
        path=request.path,
        icon=request.icon,
        parent_id=request.parent_id,
        role_ids=request.role_ids
    )

# Delete Sidebar
@sidebar_router.delete("/{sidebar_id}", response_model=SidebarResponse)
def delete_sidebar(sidebar_id: int):
    return SidebarController.delete_sidebar(sidebar_id)
