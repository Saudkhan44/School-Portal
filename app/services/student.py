from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.student import get_student_profile_by_user_id


def get_my_student_profile(
    db: Session,
    user_id: int,
):
    student = get_student_profile_by_user_id(
        db=db,
        user_id=user_id,
    )

    if student is None:
        raise NotFoundError("Student profile not found", code="student_profile_not_found")

    return student


from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.repositories.student import (
    create_person,
    create_student_profile,
)
from app.repositories.user import get_user_by_email


def create_student(
    db: Session,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    date_of_birth,
    gender: str | None,
    phone: str | None,
    address: str | None,
    student_number: str,
    admission_date,
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

        # 3. Get student role
        student_role = (
            db.query(Role)
            .filter(Role.name == "student")
            .first()
        )

        if student_role is None:
            raise ValidationError("Student role does not exist", code="student_role_missing")

        # 4. Assign role
        user_role = UserRole(
            user_id=user.id,
            role_id=student_role.id,
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

        # 6. Create StudentProfile
        student = create_student_profile(
            db=db,
            person_id=person.id,
            student_number=student_number,
            admission_date=admission_date,
            status=status,
        )

        # 7. Commit everything together
        db.commit()

        # 8. Refresh objects
        db.refresh(user)
        db.refresh(person)
        db.refresh(student)

        return student

    except (ValidationError, NotFoundError):
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise