from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class StaffProfile(Base):
    __tablename__ = "staff_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"),
        unique=True,
        nullable=False,
    )

    employee_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    designation: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    hire_date: Mapped[date | None] = mapped_column(
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
        back_populates="staff_profile",
    )