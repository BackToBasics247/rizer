from src.core.security.password_config import PasswordManager
from src.exceptions.userExceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.models.userModel import User
from src.repositories.authRepo import AuthRepo
from src.schemas.authSchema import RegisterPayload


class AuthService:

    def __init__(self, authRepo: AuthRepo, password_manager: PasswordManager) -> None:
        self._authRepo = authRepo
        self._password_manager = password_manager

    async def create_user(self, register_payload: RegisterPayload) -> User:

        if not register_payload:
            raise ValueError("Register payload is required")

        username = register_payload.username

        if await self._authRepo.exists_with_username(username):
            raise UserAlreadyExistsException(f"user with {username} already exists")

        hashed_password = self._password_manager.hash_password(
            register_payload.password
        )

        new_user = User(
            **register_payload.model_dump(exclude={"password"}),
            hashed_password=hashed_password,
        )

        return await self._authRepo.add_user(new_user)
