from fastapi import Depends, HTTPException
from http import HTTPStatus
from typing import Annotated
from src.core.jwt.jwt_config import JwtService, get_jwt_service
from src.core.database.db_config import get_db,Session
from src.models.userModel import User
from sqlalchemy.sql import select
from fastapi.security import OAuth2PasswordBearer

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(_oauth2_scheme),
    db: Session = Depends(get_db),
    jwt_service: JwtService = Depends(get_jwt_service)
) -> User:

    payload = jwt_service.decode_token(token=token)
    user_id: str | None = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user