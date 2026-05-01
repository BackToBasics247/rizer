from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.routes.authRoute import authRouter
from src.schemas.authSchema import ApiResponse, ErrorDetail
from src.exceptions.userExceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidPayloadException,
    InvalidPasswordException,
    DatabaseException,
)


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        print("Fastapi app is starting")
        yield
        print("Fastapi app is closing!")
    except Exception as e:
        raise e


app = FastAPI(root_path="/app", version="1.0.0.0", lifespan=app_lifespan)


@app.exception_handler(InvalidPayloadException)
async def invalid_payload_exception_handler(request: Request, exc: InvalidPayloadException):
    response = ApiResponse(
        success=False,
        status_code=400,
        message="Invalid request",
        error=ErrorDetail(
            error_type="InvalidPayloadException",
            error_message=str(exc),
        ),
    )
    return JSONResponse(
        status_code=400,
        content=response.model_dump(),
    )


@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_exception_handler(request: Request, exc: UserAlreadyExistsException):
    response = ApiResponse(
        success=False,
        status_code=409,
        message="User already exists",
        error=ErrorDetail(
            error_type="UserAlreadyExistsException",
            error_message=str(exc),
        ),
    )
    return JSONResponse(
        status_code=409,
        content=response.model_dump(),
    )


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    response = ApiResponse(
        success=False,
        status_code=401,
        message="Invalid credentials",
        error=ErrorDetail(
            error_type="UserNotFoundException",
            error_message="User not found",
        ),
    )
    return JSONResponse(
        status_code=401,
        content=response.model_dump(),
    )


@app.exception_handler(InvalidPasswordException)
async def invalid_password_exception_handler(request: Request, exc: InvalidPasswordException):
    response = ApiResponse(
        success=False,
        status_code=401,
        message="Authentication failed",
        error=ErrorDetail(
            error_type="InvalidPasswordException",
            error_message=str(exc),
        ),
    )
    return JSONResponse(
        status_code=401,
        content=response.model_dump(),
    )


@app.exception_handler(DatabaseException)
async def database_exception_handler(request: Request, exc: DatabaseException):
    response = ApiResponse(
        success=False,
        status_code=500,
        message="Database error occurred",
        error=ErrorDetail(
            error_type="DatabaseException",
            error_message="A database error occurred. Please try again later.",
        ),
    )
    return JSONResponse(
        status_code=500,
        content=response.model_dump(),
    )


app.include_router(authRouter)
