from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"),
        unique=True,
        nullable=False,
    )

    student_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    admission_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        nullable=False,
    )

    person = relationship(
        "Person",
        back_populates="student_profile",
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="student",
    )