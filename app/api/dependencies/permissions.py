from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.core.exceptions import ForbiddenError
from app.db.session import get_db
from app.models.user import User
from app.models.role import Role


def require_role(role_name: str):

    def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:

        role = (
            db.query(Role)
            .join(Role.users)
            .filter(
                User.id == current_user.id,
                Role.name == role_name,
            )
            .first()
        )

        if role is None:
            raise ForbiddenError(
                "You do not have permission to access this resource",
                code="forbidden",
            )

        return current_user

    return role_checker