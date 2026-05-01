from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.schemas.authSchema import LoginPayload, RegisterPayload, UserResponse
from src.services.authService import AuthService
from src.util.getters import get_auth_service

authRouter = APIRouter(prefix="/auth", tags=["authentication_routes"])


@authRouter.post("/login")
async def login_user(
    login_payload: LoginPayload,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        if not login_payload:
            raise ValueError(f"Login payload is req in routes!")
        payload = await auth_service.login_user(loginPayload=login_payload)
        return payload
    except:
        raise


@authRouter.post("/register", response_model=UserResponse)
async def register_user(
    register_payload: RegisterPayload,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        if not register_payload:
            raise ValueError("Register payload is required in routes!")
        user = await auth_service.create_user(register_payload)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
