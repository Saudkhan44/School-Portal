from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.core.security import hash_password
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.repositories.teacher import (
    create_person,
    create_teacher_profile,
    get_teacher_profile_by_user_id,
)
from app.repositories.user import get_user_by_email


def create_teacher(
    db: Session,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    date_of_birth,
    gender: str | None,
    phone: str | None,
    address: str | None,
    employee_number: str,
    designation: str | None,
    hire_date,
    status: str,
):
    try:
        # 1. Check email
        existing_user = get_user_by_email(
            db=db,
            email=email,
        )

        if existing_user:
            raise ValidationError("Email already exists", code="email_already_exists")

        # 2. Create User
        user = User(
            email=email,
            password_hash=hash_password(password),
            is_active=True,
        )

        db.add(user)
        db.flush()

        # 3. Find teacher role
        teacher_role = (
            db.query(Role)
            .filter(Role.name == "teacher")
            .first()
        )

        if teacher_role is None:
            raise ValidationError("Teacher role does not exist", code="teacher_role_missing")

        # 4. Assign teacher role
        user_role = UserRole(
            user_id=user.id,
            role_id=teacher_role.id,
        )

        db.add(user_role)
        db.flush()

        # 5. Create Person
        person = create_person(
            db=db,
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            phone=phone,
            address=address,
        )

        # 6. Create TeacherProfile
        teacher = create_teacher_profile(
            db=db,
            person_id=person.id,
            employee_number=employee_number,
            designation=designation,
            hire_date=hire_date,
            status=status,
        )

        # 7. Commit complete transaction
        db.commit()

        # 8. Refresh
        db.refresh(user)
        db.refresh(person)
        db.refresh(teacher)

        return teacher

    except (ValidationError, NotFoundError):
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise


def get_my_teacher_profile(
    db: Session,
    user_id: int,
):
    teacher = get_teacher_profile_by_user_id(
        db=db,
        user_id=user_id,
    )

    if teacher is None:
        raise NotFoundError("Teacher profile not found", code="teacher_profile_not_found")

    return teacher