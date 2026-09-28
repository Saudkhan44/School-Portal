from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TeacherAssignment(Base):
    __tablename__ = "teacher_assignments"

    __table_args__ = (
        UniqueConstraint(
            "teacher_profile_id",
            "section_id",
            name="uq_teacher_section",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    teacher_profile_id: Mapped[int] = mapped_column(
        ForeignKey("teacher_profiles.id"),
        nullable=False,
        index=True,
    )

    section_id: Mapped[int] = mapped_column(
        ForeignKey("sections.id"),
        nullable=False,
        index=True,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    teacher = relationship(
        "TeacherProfile",
        back_populates="assignments",
    )

    section = relationship(
        "Section",
        back_populates="teacher_assignments",
    )