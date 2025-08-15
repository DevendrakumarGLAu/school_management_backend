# api_v1/routers/registration_router.py
from fastapi import APIRouter
from schemas.registration_schema import RegisterRequest, RegisterResponse, UpdateRegisterRequest
from controller.registration_controller import RegistrationController

registration_router = APIRouter()

@registration_router.post("/", response_model=RegisterResponse)
def register_user(request: RegisterRequest):
    user = RegistrationController.register_user(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        role_id=request.role_id,
        created_by=request.created_by
    )
    return user


@registration_router.post("/{user_id}", response_model=RegisterResponse)
def update_user(user_id: int, request: UpdateRegisterRequest):
    user = RegistrationController.update_user(
        user_id=user_id,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        role_id=request.role_id,
        updated_by=request.updated_by
    )
    return user
