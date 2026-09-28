from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies.permissions import require_role
from app.core.exceptions import AppException
from app.db.session import get_db
from app.models.user import User
from app.schemas.student import StudentMeResponse
from app.services.student import get_my_student_profile


router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.get(
    "/me",
    response_model=StudentMeResponse,
)
def get_my_profile(
    current_user: User = Depends(
        require_role("student")
    ),
    db: Session = Depends(get_db),
):

    try:
        student = get_my_student_profile(
            db=db,
            user_id=current_user.id,
        )

        person = student.person

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

            "student_profile": student,
        }

    except AppException as exc:
        raise exc