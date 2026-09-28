from sqlalchemy.orm import Session

from app.models.person import Person
from app.models.teacher_profile import TeacherProfile


def create_person(
    db: Session,
    user_id: int,
    first_name: str,
    last_name: str,
    date_of_birth,
    gender: str | None,
    phone: str | None,
    address: str | None,
) -> Person:

    person = Person(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=gender,
        phone=phone,
        address=address,
    )

    db.add(person)
    db.flush()

    return person


def create_teacher_profile(
    db: Session,
    person_id: int,
    employee_number: str,
    designation: str | None,
    hire_date,
    status: str,
) -> TeacherProfile:

    teacher = TeacherProfile(
        person_id=person_id,
        employee_number=employee_number,
        designation=designation,
        hire_date=hire_date,
        status=status,
    )

    db.add(teacher)
    db.flush()

    return teacher


def get_teacher_profile_by_user_id(
    db: Session,
    user_id: int,
) -> TeacherProfile | None:

    return (
        db.query(TeacherProfile)
        .join(TeacherProfile.person)
        .filter(
            TeacherProfile.person.has(user_id=user_id)
        )
        .first()
    )