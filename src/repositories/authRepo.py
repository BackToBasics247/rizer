from sqlalchemy import select,or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from uuid import UUID

from src.exceptions.userExceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    DatabaseException,
)
from src.models.userModel import User


class AuthRepo:

    def __init__(self, db: Session) -> None:
        self._db = db

    def add_user(self, new_user: User) -> User:
        try:
            self._db.add(new_user)
            self._db.commit()
            self._db.refresh(new_user)
            return new_user

        except IntegrityError as e:
            self._db.rollback()
            raise UserAlreadyExistsException("User already exists") from e

        except SQLAlchemyError as e:
            self._db.rollback()
            raise DatabaseException("Database error while creating user") from e

    def exists_with_username(self, username: str) -> User|None:
        try:
            stmt = select(User).where(User.username == username)
            result = self._db.execute(stmt).scalar_one_or_none()
            return result

        except SQLAlchemyError as e:
            raise DatabaseException("Database error while checking user existence") from e

    def exists_with_userid(self, user_id: str) -> User|None:
        try:
            stmt = select(User).where(User.id == user_id)
            result = self._db.execute(stmt).scalar_one_or_none()
            return result
        
        except SQLAlchemyError as e:
            raise DatabaseException("Database error while checking user existence") from e
        
    def exists_with_identifier(self, identifier: str) -> User | None:
        try:
            is_valid_uuid = False
            uuid_obj = None
            try:
                uuid_obj = UUID(identifier)
                is_valid_uuid = True
            except ValueError:
                pass

            conditions = [User.username == identifier]
            if is_valid_uuid:
                conditions.append(User.id == uuid_obj)

            stmt = select(User).where(or_(*conditions))
            return self._db.execute(stmt).scalar_one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseException("Database error while checking user existence") from e
