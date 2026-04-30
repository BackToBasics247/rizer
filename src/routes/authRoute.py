from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.schemas.authSchema import RegisterPayload,LoginPayload
from src.util.getters import get_auth_service
from src.services.authService import AuthService
from typing import Annotated

authRouter = APIRouter(prefix="/auth", tags=["authentication_routes"])

@authRouter.post("/login")
async def login_user(login_payload:LoginPayload,auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    try:
        if not login_payload:
            raise ValueError(f"Login payload is req in routes!")
        pass
    except:
        pass

@authRouter.post("/register")
async def register_user(register_payload:RegisterPayload,auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    try:
        if not register_payload:
            raise ValueError(f"Register payload is req in routes!")
        response = await auth_service.create_user(register_payload)
        if response:
            return JSONResponse(content=response,status_code=201)
        raise HTTPException(500,detail={"something went wrong"})
    except:
        pass