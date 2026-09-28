import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import settings


password_hash = PasswordHash.recommended()


def validate_password_policy(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(ch.isupper() for ch in password):
        return False
    if not any(ch.islower() for ch in password):
        return False
    if not any(ch.isdigit() for ch in password):
        return False
    return True


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return password_hash.verify(password, hashed_password)
    except ValueError:
        return False


def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.jwt_access_token_expire_minutes)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
        "jti": uuid.uuid4().hex,
        "type": "access",
        "iss": "school-portal",
        "aud": "school-portal-api",
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=7)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
        "jti": uuid.uuid4().hex,
        "type": "refresh",
        "iss": "school-portal",
        "aud": "school-portal-api",
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_token(token: str, expected_type: str | None = None) -> dict[str, Any]:
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
        issuer="school-portal",
        audience="school-portal-api",
        options={
            "require": ["sub", "exp", "iat", "type", "iss", "aud"],
        },
    )

    if expected_type and payload.get("type") != expected_type:
        raise jwt.InvalidTokenError("Token type mismatch")

    return payload
