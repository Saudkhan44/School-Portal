from sqlalchemy.orm import Session
from app.models.student_profile import StudentProfile
from sqlalchemy.orm import Session
from app.models.person import Person
from app.models.student_profile import StudentProfile



def get_student_profile_by_user_id(
    db: Session,
    user_id: int,
) -> StudentProfile | None:

    return (
        db.query(StudentProfile)
        .join(StudentProfile.person)
        .filter(
            StudentProfile.person.has(user_id=user_id)
        )
        .first()
    )



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


def create_student_profile(
    db: Session,
    person_id: int,
    student_number: str,
    admission_date,
    status: str,
) -> StudentProfile:

    student = StudentProfile(
        person_id=person_id,
        student_number=student_number,
        admission_date=admission_date,
        status=status,
    )

    db.add(student)
    db.flush()

    return student