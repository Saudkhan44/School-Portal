from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "roles": [
            role.name
            for role in current_user.roles
        ],
    }