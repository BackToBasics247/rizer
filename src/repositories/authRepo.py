from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.exceptions.userExceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.models.userModel import User


class AuthRepo:

    def __init__(self, db: Session) -> None:
        self._db = db

    async def add_user(self, new_user: User) -> User:
        try:
            self._db.add(new_user)
            self._db.commit()
            self._db.refresh(new_user)
            return new_user

        except IntegrityError as e:
            self._db.rollback()
            # likely unique constraint violation
            raise UserAlreadyExistsException("User already exists") from e

        except SQLAlchemyError as e:
            self._db.rollback()
            raise RuntimeError("Database error while creating user") from e

    async def exists_with_username(self, username: str) -> bool:
        try:
            stmt = select(User).where(User.username == username)
            result = self._db.execute(stmt).scalar_one_or_none()
            return result is not None

        except SQLAlchemyError as e:
            raise RuntimeError("Database error while checking user existence") from e
