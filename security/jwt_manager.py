from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from core.config import settings


class JWTManager:
    def __init__(self) -> None:
        self.secret_key = settings.SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, subject: str, extra_claims: dict[str, Any] | None = None) -> str:
        expire_at = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_token_expire_minutes
        )

        payload: dict[str, Any] = {
            "sub": subject,
            "exp": expire_at,
            "type": "access",
        }

        if extra_claims:
            payload.update(extra_claims)

        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

        return token

    def decode_access_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            token_type = payload.get("type")

            if token_type != "access":
                raise JWTError("Invalid token type.")

            return payload

        except JWTError as error:
            raise ValueError("Invalid or expired access token.") from error