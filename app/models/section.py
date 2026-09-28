from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Section(Base):
    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )

    program_id: Mapped[int | None] = mapped_column(
        ForeignKey("programs.id"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    academic_year: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    term: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    course = relationship(
        "Course",
        back_populates="sections",
    )

    program = relationship(
        "Program",
        back_populates="sections",
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="section",
    )

    teacher_assignments = relationship(
        "TeacherAssignment",
        back_populates="section",
    )