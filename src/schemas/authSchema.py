from datetime import datetime
from uuid import UUID

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
