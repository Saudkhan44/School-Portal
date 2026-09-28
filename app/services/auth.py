from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError
from app.core.security import (
    create_access_token,
    verify_password,
)
from app.repositories.user import get_user_by_email


def login_user(
    db: Session,
    email: str,
    password: str,
) -> str:

    user = get_user_by_email(db, email)

    if not user:
        raise UnauthorizedError("Invalid email or password", code="invalid_credentials")

    if not verify_password(password, user.password_hash):
        raise UnauthorizedError("Invalid email or password", code="invalid_credentials")

    if not user.is_active:
        raise UnauthorizedError("User account is inactive", code="account_inactive")

    return create_access_token(user.id)