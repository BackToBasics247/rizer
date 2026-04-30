from typing import Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    email: str


class UserCreate(BaseUser):
    password: str


class UserResponse(BaseUser):
    id: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
