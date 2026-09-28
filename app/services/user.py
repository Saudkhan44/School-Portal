from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.repositories.user import create_user


def create_user_service(
    db: Session,
    email: str,
    password: str,
):
    password_hash = hash_password(password)

    user = create_user(
        db=db,
        email=email,
        password_hash=password_hash,
    )

    return user