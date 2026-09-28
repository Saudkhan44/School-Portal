from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies.permissions import require_role
from app.core.exceptions import AppException
from app.db.session import get_db
from app.models.user import User
from app.schemas.student import (
    StudentCreateRequest,
    StudentMeResponse,
)
from app.services.student import create_student


from app.schemas.teacher import (
    TeacherCreateRequest,
    TeacherMeResponse,
)
from app.services.teacher import create_teacher


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post(
    "/students",
    response_model=StudentMeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student_account(
    data: StudentCreateRequest,
    current_user: User = Depends(
        require_role("admin")
    ),
    db: Session = Depends(get_db),
):
    try:
        student = create_student(
            db=db,
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            date_of_birth=data.date_of_birth,
            gender=data.gender,
            phone=data.phone,
            address=data.address,
            student_number=data.student_number,
            admission_date=data.admission_date,
            status=data.status,
        )

        person = student.person
        user = person.user

        return {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,

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


@router.post(
    "/teachers",
    response_model=TeacherMeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_teacher_account(
    data: TeacherCreateRequest,
    current_user: User = Depends(
        require_role("admin")
    ),
    db: Session = Depends(get_db),
):
    try:
        teacher = create_teacher(
            db=db,
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            date_of_birth=data.date_of_birth,
            gender=data.gender,
            phone=data.phone,
            address=data.address,
            employee_number=data.employee_number,
            designation=data.designation,
            hire_date=data.hire_date,
            status=data.status,
        )

        person = teacher.person
        user = person.user

        return {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,

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