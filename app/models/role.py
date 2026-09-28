from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.user_role import UserRole

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    users = relationship(
        "User",
        secondary=UserRole.__table__,
        back_populates="roles",
    )