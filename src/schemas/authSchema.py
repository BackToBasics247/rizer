from datetime import datetime
from uuid import UUID
from typing import Any, Optional

from pydantic import BaseModel


class LoginPayload(BaseModel):

    identifier: str
    password: str


class RegisterPayload(BaseModel):

    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ErrorDetail(BaseModel):
    error_type: str
    error_message: str


class ApiResponse(BaseModel):
    success: bool
    status_code: int
    message: str
    data: Optional[Any] = None
    error: Optional[ErrorDetail] = None

    class Config:
        json_schema_extra = {
            "example_success": {
                "success": True,
                "status_code": 200,
                "message": "User registered successfully",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "john_doe",
                    "email": "john@example.com",
                    "is_admin": False,
                    "created_at": "2026-05-01T10:00:00",
                    "updated_at": "2026-05-01T10:00:00"
                }
            },
            "example_error": {
                "success": False,
                "status_code": 400,
                "message": "Invalid input provided",
                "error": {
                    "error_type": "InvalidPayloadException",
                    "error_message": "Login payload is required"
                }
            }
        }
