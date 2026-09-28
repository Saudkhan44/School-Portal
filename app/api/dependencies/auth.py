import jwt

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import UnauthorizedError
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import get_user_by_id


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials

    try:
        payload = decode_token(token, expected_type="access")
        user_id = payload.get("sub")
        if user_id is None:
            raise UnauthorizedError("Invalid authentication token", code="invalid_token")
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedError("Invalid authentication token", code="invalid_token") from exc

    user = get_user_by_id(
        db=db,
        user_id=int(user_id),
    )

    if user is None:
        raise UnauthorizedError("User not found", code="user_not_found")

    if not user.is_active:
        raise UnauthorizedError("User account is inactive", code="account_inactive")

    return user