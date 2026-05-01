from src.core.security.password_config import PasswordManager
from src.exceptions.userExceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.models.userModel import User
from src.repositories.authRepo import AuthRepo
from src.schemas.authSchema import RegisterPayload,LoginPayload
from src.core.jwt.jwt_config import JwtService,get_jwt_service


class AuthService:

    def __init__(self, authRepo: AuthRepo, password_manager: PasswordManager, jwt_service: JwtService) -> None:
        self._authRepo = authRepo
        self._password_manager = password_manager
        self._jwt_service = jwt_service

    async def create_user(self, register_payload: RegisterPayload) -> User:

        if not register_payload:
            raise ValueError("Register payload is required")

        username = register_payload.username
        if self._authRepo.exists_with_username(username):
            raise UserAlreadyExistsException(f"user with {username} already exists")

        hashed_password = self._password_manager.hash_password(
            register_payload.password
        )

        new_user = User(
            **register_payload.model_dump(exclude={"password"}),
            hashed_password=hashed_password,
        )
        return self._authRepo.add_user(new_user)

    async def login_user(self, loginPayload:LoginPayload) -> dict:
        
        if not loginPayload:
            raise ValueError("Login payload is required")
        
        identifier = str(loginPayload.identifier).strip()
        user_exists = self._authRepo.exists_with_identifier(identifier=identifier)
        if not user_exists:
            raise UserNotFoundException(f"user with identifier:{identifier} dosen't exists!")
        
        is_password_correct = self._password_manager.verify_password(user_exists.hashed_password,loginPayload.password)
        if not is_password_correct:
            raise ValueError("Password entered is wrong! Please check your password")
        
        generated_access_token = self._jwt_service.create_token({"sub":str(user_exists.id)},token_type='ACCESS')
        generated_refresh_token = self._jwt_service.create_token({"sub":str(user_exists.id)},token_type='REFRESH')

        return {
            "access_token":generated_access_token,
            "refresh_token":generated_refresh_token,
            "access_token_type":"bearer",
            "refresh_token_type":"bearer"
        }