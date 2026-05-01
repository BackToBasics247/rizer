from datetime import datetime, timedelta, timezone
from typing import Literal

from jose import JWTError
from jose.jwt import decode, encode


class JwtService:

    def __init__(self) -> None:
        self._ACCESS_TOKEN_SECRET: str = (
            "f821da0e7e6cb50a51b130fb85a7c7599ba6de2518eb5498e33b0b8caec70081"
        )
        self._REFRESH_TOKEN_SECRET: str = (
            "52f426c3e3eff3c0bacd3217249fb4d9300cb19da94fdb3f6af979c94450d5b8"
        )
        self._ACCESS_TOKEN_EXPIRY_MIN: timedelta = timedelta(minutes=15)
        self._REFRESH_TOKEN_EXPIRY_DAY: timedelta = timedelta(days=2)
        self._ALGORITHM: str = "HS256"

    def create_token(
        self,
        claims: dict,
        token_type: Literal["ACCESS", "REFRESH"] = "ACCESS",
    ) -> str:
        now = datetime.now(timezone.utc)
        if token_type == "ACCESS":
            payload = {
                "sub": claims["sub"],
                "iat": now,
                "type": token_type,
                "exp": now+self._ACCESS_TOKEN_EXPIRY_MIN,
            }
            return encode(
                claims=payload, key=self._ACCESS_TOKEN_SECRET, algorithm=self._ALGORITHM
            )
        else:
            payload = {
                "sub": claims["sub"],
                "iat": now,
                "type": token_type,
                "exp": now+self._REFRESH_TOKEN_EXPIRY_DAY,
            }
            return encode(
                claims=payload,
                key=self._REFRESH_TOKEN_SECRET,
                algorithm=self._ALGORITHM,
            )

    def decode_token(
        self, token: str, token_type: Literal["ACCESS", "REFRESH"] = "ACCESS"
    ):
        try:
            if token_type == "ACCESS":
                return decode(
                    token=token,
                    key=self._ACCESS_TOKEN_SECRET,
                    algorithms=self._ALGORITHM,
                )
            else:
                return decode(
                    token=token,
                    key=self._REFRESH_TOKEN_SECRET,
                    algorithms=self._ALGORITHM,
                )
        except JWTError as jwte:
            raise ValueError(f"Invalid or expired token!")

    def verify_token(
        self, token: str, token_type: Literal["ACCESS", "REFRESH"] = "ACCESS"
    ) -> dict:
        payload = self.decode_token(token=token, token_type=token_type)
        if str(payload.get("type")).lower() == token_type.lower():
            return payload
        raise ValueError(f"Invalid token type!")


def get_jwt_service() -> JwtService:
    return JwtService()