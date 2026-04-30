from pydantic import BaseModel


class LoginPayload(BaseModel):

    identifier: str
    password: str


class RegisterPayload(BaseModel):

    username: str
    email: str
    password: str
