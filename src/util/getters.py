from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database.db_config import get_db
from src.core.security.password_config import PasswordManager, get_password_manager
from src.repositories.authRepo import AuthRepo
from src.services.authService import AuthService


def get_auth_repo(db: Annotated[Session, Depends(get_db)]) -> AuthRepo:
    return AuthRepo(db)


def get_auth_service(
    auth_repo: Annotated[AuthRepo, Depends(get_auth_repo)],
    password_manager: Annotated[PasswordManager, Depends(get_password_manager)],
) -> AuthService:
    return AuthService(auth_repo, password_manager)
