from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies.permissions import require_role
from app.core.exceptions import AppException
from app.db.session import get_db
from app.models.user import User
from app.schemas.teacher import TeacherMeResponse
from app.services.teacher import get_my_teacher_profile


router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"],
)


@router.get(
    "/me",
    response_model=TeacherMeResponse,
)
def get_my_profile(
    current_user: User = Depends(
        require_role("teacher")
    ),
    db: Session = Depends(get_db),
):
    try:
        teacher = get_my_teacher_profile(
            db=db,
            user_id=current_user.id,
        )

        person = teacher.person

        return {
            "id": current_user.id,
            "email": current_user.email,
            "is_active": current_user.is_active,

            "first_name": person.first_name,
            "last_name": person.last_name,
            "date_of_birth": person.date_of_birth,
            "gender": person.gender,
            "phone": person.phone,
            "address": person.address,

            "teacher_profile": teacher,
        }

    except AppException as exc:
        raise exc