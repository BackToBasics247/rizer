from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.schemas.authSchema import (
    LoginPayload,
    RegisterPayload,
    ApiResponse,
)
from src.services.authService import AuthService
from src.util.getters import get_auth_service

authRouter = APIRouter(prefix="/auth", tags=["authentication"])


@authRouter.post(
    "/register",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with username, email, and password.",
)
async def register_user(
    register_payload: RegisterPayload,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    user = await auth_service.create_user(register_payload)
    return ApiResponse(
        success=True,
        status_code=201,
        message="User registered successfully",
        data=user,
    )


@authRouter.post(
    "/login",
    response_model=ApiResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user",
    description="Authenticate user with identifier (username or ID) and password.",
)
async def login_user(
    login_payload: LoginPayload,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    payload = await auth_service.login_user(loginPayload=login_payload)
    return ApiResponse(
        success=True,
        status_code=200,
        message="Login successful",
        data=payload,
    )


@authRouter.post(
    "/refresh",
    response_model=ApiResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="Refresh the access token using a valid refresh token.",
)
async def refresh_token(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    raise NotImplementedError("Refresh endpoint not yet implemented")


@authRouter.post(
    "/logout",
    response_model=ApiResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Logout the user and invalidate the current session.",
)
async def logout_user(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    raise NotImplementedError("Logout endpoint not yet implemented")
