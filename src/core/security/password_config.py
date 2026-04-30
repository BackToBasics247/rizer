from functools import lru_cache

from passlib.context import CryptContext


class PasswordManager:

    def __init__(self) -> None:
        self._context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash_password(self, plain_password: str) -> str:
        return self._context.hash(plain_password)

    def verify_password(self, hashed_password: str, plain_password: str) -> bool:
        return self._context.verify(plain_password, hashed_password)


@lru_cache
def get_password_manager() -> PasswordManager:
    return PasswordManager()
